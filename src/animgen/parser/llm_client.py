import json, re
from pydantic import ValidationError
from google import genai
from google.genai import types
from .schema import Storyboard
from .prompts import SYSTEM_PROMPT, FEW_SHOT

def _clean(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    return text

def parse_storyboard(idea: str, api_key: str, model: str = "gemini-2.5-flash",
                     max_retries: int = 3) -> Storyboard:
    client = genai.Client(api_key=api_key)
    contents = []
    for user_ex, json_ex in FEW_SHOT:
        contents.append(types.Content(role="user", parts=[types.Part(text=user_ex)]))
        contents.append(types.Content(role="model", parts=[types.Part(text=json_ex)]))
    contents.append(types.Content(role="user", parts=[types.Part(text=idea)]))

    last_err = None
    for attempt in range(1, max_retries + 1):
        resp = client.models.generate_content(
            model=model, contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.4))
        raw = _clean(resp.text)
        try:
            sb = Storyboard(**json.loads(raw))
            print(f"Parsed OK on attempt {attempt}")
            return sb
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            last_err = e
            print(f"Attempt {attempt} failed: {str(e)[:150]}")
            contents.append(types.Content(role="model", parts=[types.Part(text=raw)]))
            contents.append(types.Content(role="user", parts=[types.Part(
                text=f"That JSON was invalid: {e}\nFix it and return only the corrected JSON.")]))
    raise RuntimeError(f"Parsing failed after {max_retries} attempts: {last_err}")

# Experiments log\n\n| Date | Who | What changed | Result | Run ID |\n|---|---|---|---|---|\n
## 2026-10-30 | Ilyas | Step 3: storyboard parser
- Added schema.py (Pydantic), prompts.py (system prompt + 1 few-shot), llm_client.py (Gemini 2.5 Flash, validate + retry)
- Generated 11 storyboards, all parsed on attempt 1. sb02 to sb11 frozen as the official test set in eval/test_storyboards/
- Known gap: shots with no characters (e.g. POV shots) need a rule at the keyframe stage

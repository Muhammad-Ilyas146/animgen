from transformers import CLIPTokenizer

NEGATIVE_PROMPT = "blurry, low quality, deformed, extra limbs, text, watermark"
MAX_TOKENS = 75   # CLIP context is 77 including start and end tokens

_tok = None

def n_tokens(text: str) -> int:
    global _tok
    if _tok is None:
        _tok = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
    return len(_tok(text, add_special_tokens=False).input_ids)

def build_shot_prompt(sb, scene, shot) -> str:
    """Shared prompt rule for every method. Order: style, characters, action, setting.
    If over the CLIP limit, trim words from setting, then style, then action."""
    chars = {c.id: c for c in sb.characters}
    parts = {
        "style": sb.style,
        "chars": ", ".join(chars[c].appearance for c in shot.characters),
        "desc": shot.description,
        "setting": scene.setting,
    }
    def join():
        return ", ".join(parts[k] for k in ["style", "chars", "desc", "setting"] if parts[k])
    for key in ["setting", "style", "desc"]:
        while n_tokens(join()) > MAX_TOKENS and parts[key].split():
            parts[key] = " ".join(parts[key].split()[:-1])
    return join()

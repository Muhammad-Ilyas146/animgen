NEGATIVE_PROMPT = "blurry, low quality, deformed, extra limbs, text, watermark"

def build_shot_prompt(sb, scene, shot) -> str:
    """Prompt-only description of one shot (used by the plain SD baseline)."""
    chars = {c.id: c for c in sb.characters}
    char_text = ", ".join(chars[c].appearance for c in shot.characters)
    parts = [sb.style, char_text, shot.description, scene.setting]
    return ", ".join(p for p in parts if p)

import json

SYSTEM_PROMPT = """You convert a short story idea into a storyboard JSON for an animation pipeline.

Rules:
- Output ONLY valid JSON. No markdown fences, no commentary.
- 1 to 2 characters. Character ids are lowercase letters, digits, underscores.
- 1 to 6 scenes, each with 1 to 4 shots.
- Each shot lasts 1 to 8 seconds. Total video length must be between 5 and 40 seconds.
- camera must be one of: wide, medium, close_up, over_shoulder, top_down.
- Shot descriptions must be purely visual (what the viewer sees), no inner thoughts.
- Every character id used in a shot must be defined in "characters".
- "appearance" must describe fixed visual traits (hair, clothes, colors) so the character looks the same every time.
- "dialogue" is optional; use null if none.

JSON shape:
{
  "title": str,
  "style": str,
  "characters": [{"id": str, "name": str, "appearance": str}],
  "scenes": [{"id": str, "setting": str,
              "shots": [{"id": str, "description": str, "characters": [str],
                         "camera": str, "duration_sec": number, "dialogue": str|null}]}]
}
"""

_EXAMPLE = {
    "title": "Rainy Rescue",
    "style": "soft 2D storybook illustration",
    "characters": [{
        "id": "mia", "name": "Mia",
        "appearance": "girl with short black hair, bright yellow raincoat, red boots"}],
    "scenes": [
        {"id": "s1", "setting": "city street, rainy evening", "shots": [
            {"id": "s1_shot1", "description": "Mia walks down a wet street, rain falling",
             "characters": ["mia"], "camera": "wide", "duration_sec": 4, "dialogue": None},
            {"id": "s1_shot2", "description": "Mia stops and looks down at a small kitten under a bench",
             "characters": ["mia"], "camera": "medium", "duration_sec": 4,
             "dialogue": "Oh, you poor thing."}]},
        {"id": "s2", "setting": "cozy living room, night", "shots": [
            {"id": "s2_shot1", "description": "Mia sits on a rug drying the kitten with a towel",
             "characters": ["mia"], "camera": "close_up", "duration_sec": 5, "dialogue": None}]},
    ],
}

FEW_SHOT = [
    ("A girl with a yellow raincoat finds a lost kitten in the rain and takes it home.",
     json.dumps(_EXAMPLE)),
]

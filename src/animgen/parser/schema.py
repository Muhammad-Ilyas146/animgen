from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator


class Character(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_]+$")          # e.g. "kai"
    name: str
    appearance: str                                    # visual description, used in prompts


class Shot(BaseModel):
    id: str                                            # e.g. "s1_shot1"
    description: str                                   # what is visible, in plain visual language
    characters: List[str] = []                         # character ids present in the shot
    camera: Literal["wide", "medium", "close_up", "over_shoulder", "top_down"] = "medium"
    duration_sec: float = Field(ge=1.0, le=8.0)
    dialogue: Optional[str] = None                     # optional, for TTS later


class Scene(BaseModel):
    id: str
    setting: str                                       # location and time of day
    shots: List[Shot] = Field(min_length=1, max_length=4)


class Storyboard(BaseModel):
    title: str
    style: str                                         # e.g. "flat 2D cartoon, bold outlines"
    characters: List[Character] = Field(min_length=1, max_length=2)
    scenes: List[Scene] = Field(min_length=1, max_length=6)

    @model_validator(mode="after")
    def check_references_and_length(self):
        known = {c.id for c in self.characters}
        for scene in self.scenes:
            for shot in scene.shots:
                missing = set(shot.characters) - known
                if missing:
                    raise ValueError(f"Shot {shot.id} uses unknown characters: {missing}")
        total = sum(s.duration_sec for sc in self.scenes for s in sc.shots)
        if not (5 <= total <= 40):
            raise ValueError(f"Total duration {total}s outside the 5 to 40 s range")
        return self

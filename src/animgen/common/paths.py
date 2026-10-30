from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    drive_root: str = "/content/drive/MyDrive/animgen_data"
    local_root: str = "/content/work"

    @property
    def root(self) -> Path:
        return Path(self.drive_root)

    @property
    def storyboards(self) -> Path:
        return self.root / "storyboards"

    @property
    def characters(self) -> Path:
        return self.root / "characters"

    @property
    def lora_weights(self) -> Path:
        return self.root / "lora_weights"

    @property
    def runs(self) -> Path:
        return self.root / "runs"

    @property
    def eval(self) -> Path:
        return self.root / "eval"

    @property
    def local(self) -> Path:
        return Path(self.local_root)

    def run_dir(self, run_id: str) -> Path:
        d = self.runs / run_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def make_all(self) -> None:
        for p in [self.storyboards, self.characters, self.lora_weights,
                  self.runs, self.eval, self.local]:
            p.mkdir(parents=True, exist_ok=True)

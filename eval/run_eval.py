import json, pathlib
import pandas as pd
from PIL import Image
from animgen.parser.schema import Storyboard
from eval.metrics import clip_scores, identity_sim

ROOT = pathlib.Path("/content/drive/MyDrive/animgen_data")

def evaluate_run(run_id, sb_dir="eval/test_storyboards"):
    shot_rows, id_rows = [], []
    for run_dir in sorted((ROOT / "runs" / run_id).glob("sb*")):
        sb = Storyboard(**json.load(open(pathlib.Path(sb_dir) / f"{run_dir.name}.json")))
        cfg = json.load(open(run_dir / "config.json"))
        shots = [s for sc in sb.scenes for s in sc.shots]
        imgs = {s.id: Image.open(run_dir / f"{s.id}.png").convert("RGB") for s in shots}
        cs = clip_scores([imgs[s.id] for s in shots],
                         [cfg["shots"][s.id]["prompt"] for s in shots])
        for s, c in zip(shots, cs):
            shot_rows.append({"run_id": run_id, "storyboard": run_dir.name,
                              "shot": s.id, "clip_score": c})
        for ch in sb.characters:
            ims = [imgs[s.id] for s in shots if ch.id in s.characters]
            id_rows.append({"run_id": run_id, "storyboard": run_dir.name, "character": ch.id,
                            "n_shots": len(ims), "identity_dino": identity_sim(ims)})
    shots_df, id_df = pd.DataFrame(shot_rows), pd.DataFrame(id_rows)
    out = ROOT / "eval"
    out.mkdir(exist_ok=True)
    shots_df.to_csv(out / f"{run_id}_shots.csv", index=False)
    id_df.to_csv(out / f"{run_id}_identity.csv", index=False)
    return shots_df, id_df

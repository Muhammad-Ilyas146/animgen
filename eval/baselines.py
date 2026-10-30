import json, pathlib, platform
from importlib.metadata import version
import torch
from animgen.parser.schema import Storyboard
from animgen.parser.prompts import build_shot_prompt, NEGATIVE_PROMPT

RUNS = pathlib.Path("/content/drive/MyDrive/animgen_data/runs")

def run_plain_sd(pipe, sb_path, run_id, base_seed=42, steps=25, cfg=7.5):
    """Plain SD 1.5, prompt only. One image per shot, fixed seed per shot."""
    sb_path = pathlib.Path(sb_path)
    sb = Storyboard(**json.load(open(sb_path)))
    out = RUNS / run_id / sb_path.stem
    out.mkdir(parents=True, exist_ok=True)

    log = {"storyboard": sb_path.name, "variant": "plain_sd15", "steps": steps,
           "cfg": cfg, "base_seed": base_seed, "resolution": 512,
           "versions": {k: version(k) for k in ["torch", "diffusers", "transformers"]},
           "shots": {}}
    i = 0
    for scene in sb.scenes:
        for shot in scene.shots:
            seed = base_seed + i
            prompt = build_shot_prompt(sb, scene, shot)
            log["shots"][shot.id] = {"seed": seed, "prompt": prompt}
            path = out / f"{shot.id}.png"
            i += 1
            if path.exists():
                continue
            g = torch.Generator("cuda").manual_seed(seed)
            img = pipe(prompt, negative_prompt=NEGATIVE_PROMPT, num_inference_steps=steps,
                       guidance_scale=cfg, height=512, width=512, generator=g).images[0]
            img.save(path)
    (out / "config.json").write_text(json.dumps(log, indent=2))
    return out

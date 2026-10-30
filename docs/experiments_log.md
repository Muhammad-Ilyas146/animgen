# Experiments log\n\n| Date | Who | What changed | Result | Run ID |\n|---|---|---|---|---|\n
## 2026-10-30 | Ilyas | Step 3: storyboard parser
- Added schema.py (Pydantic), prompts.py (system prompt + 1 few-shot), llm_client.py (Gemini 2.5 Flash, validate + retry)
- Generated 11 storyboards, all parsed on attempt 1. sb02 to sb11 frozen as the official test set in eval/test_storyboards/
- Known gap: shots with no characters (e.g. POV shots) need a rule at the keyframe stage

## 2026-10-30 | Ilyas | Step 4: plain SD 1.5 baseline
- Added keyframes/prompting.py (build_shot_prompt) and eval/baselines.py (run_plain_sd)
- Run ID 2026-10-30_all_plainsd: 10 storyboards, 61 images, seed = 42 + shot index, 25 steps, cfg 7.5, 512x512
- Result: style consistent, character identity not (fox scarf missing, wrong color, body shape drifts)
- Known issue: 2 prompts (sb07, sb08) exceed CLIP's 77 tokens and were truncated. Fix in build_shot_prompt before Step 5

## 2026-10-30 | Ilyas | Step 4e: baseline metrics
- Added eval/metrics.py (CLIPScore, DINOv2 identity) and eval/run_eval.py
- Baseline 2026-10-30_all_plainsd: CLIP 33.83 (61 shots), DINO identity 0.52 (per character rows; leo/maya and farmer/dog share shots, so double-counted)
- Repo fix: parser/prompts.py had been overwritten with prompt-builder code in the Step 4 commit; restored from 0be9132 and recreated keyframes/prompting.py

## 2026-10-30 | Ilyas | Step 4h/4i: metric calibration
- Floor (different storyboards): 0.112. Within-storyboard, all shots: 0.472. Per-storyboard character identity: 0.527 (baseline number to report)
- Same prompt, 4 seeds (sb02, sb03, sb10): mean 0.631, a reference level for prompt-only SD
- Caveat: whole-image DINO mixes character and scene similarity. Consider character crops later
- Values saved in eval/baseline_calibration.json

## 2026-10-30 | Ilyas | Step 4k to 4r: 77-token fix
- build_shot_prompt now trims to 75 content tokens (setting, then style, then action). 59 of 61 prompts unchanged
- Bug found: eval/baselines.py imported build_shot_prompt from parser.prompts (wrong module). Fixed to keyframes.prompting
- Regenerated 2 sb08_race images: identical in effect (CLIP had already truncated them). Final baseline: CLIP 33.83, DINO identity 0.527
- Lesson: after editing modules, verify in a fresh process (!python -c ...), not with importlib.reload

## 2026-10-30 | Ilyas | Step 5: ControlNet keyframes (no LoRA), blob templates
- ControlNet canny and depth (SD 1.5, lllyasviel) run on T4: peak VRAM 5.08 GB, about 6 s per image
- keyframes/templates.py: v1 humanoid blobs + gradient ground (blob foxes, striped ground, worse than baseline);
  v2 neutral ellipses + flat ground
- Sweep on sb02_fox: s=0.4 is the only usable scale; s>=0.5 distorts the fox; close_up fails at all scales (tail only or toy-like)
- Conclusion: text-only blob layouts give weak framing control and do not improve identity. Parked.
- Next: character data + LoRA (Step 6, 7). Revisit ControlNet with depth/lineart derived from character reference images

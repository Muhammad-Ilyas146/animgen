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

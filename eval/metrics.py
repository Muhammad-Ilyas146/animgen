import itertools
import torch, torch.nn.functional as F
from transformers import CLIPModel, CLIPProcessor, AutoImageProcessor, AutoModel

DEV = "cuda" if torch.cuda.is_available() else "cpu"
_cache = {}

def _tensor(x):
    # some transformers versions return an output object instead of a tensor
    return x if torch.is_tensor(x) else x.pooler_output

def _clip():
    if "clip" not in _cache:
        n = "openai/clip-vit-base-patch32"
        _cache["clip"] = (CLIPModel.from_pretrained(n).to(DEV).eval(),
                          CLIPProcessor.from_pretrained(n))
    return _cache["clip"]

def _dino():
    if "dino" not in _cache:
        n = "facebook/dinov2-small"
        _cache["dino"] = (AutoModel.from_pretrained(n).to(DEV).eval(),
                          AutoImageProcessor.from_pretrained(n))
    return _cache["dino"]

@torch.no_grad()
def clip_scores(images, prompts):
    """CLIP cosine similarity x100 between each image and its prompt (higher is better)."""
    model, proc = _clip()
    inp = proc(text=prompts, images=images, return_tensors="pt",
               padding=True, truncation=True, max_length=77).to(DEV)
    ie = F.normalize(_tensor(model.get_image_features(pixel_values=inp["pixel_values"])), dim=-1)
    te = F.normalize(_tensor(model.get_text_features(input_ids=inp["input_ids"],
                                                     attention_mask=inp["attention_mask"])), dim=-1)
    return (100 * (ie * te).sum(-1)).tolist()

@torch.no_grad()
def identity_sim(images):
    """Mean pairwise DINOv2 cosine similarity across images of one character (higher = more consistent)."""
    if len(images) < 2:
        return None
    model, proc = _dino()
    inp = proc(images=images, return_tensors="pt").to(DEV)
    emb = F.normalize(model(**inp).last_hidden_state[:, 0], dim=-1)
    sims = [float(emb[i] @ emb[j]) for i, j in itertools.combinations(range(len(images)), 2)]
    return sum(sims) / len(sims)

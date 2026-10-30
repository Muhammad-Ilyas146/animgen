import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# h = figure height, base = foot/bottom y, horizon = horizon y (all as fractions of image size)
CAMERA = {
    "wide":          dict(h=0.28, base=0.78, horizon=0.55),
    "medium":        dict(h=0.62, base=0.97, horizon=0.45),
    "close_up":      dict(h=1.50, base=1.70, horizon=0.35),
    "over_shoulder": dict(h=0.35, base=0.80, horizon=0.45),
    "top_down":      dict(h=0.20, base=0.60, horizon=None),
}

def _figure(draw, cx, base_y, h, val=235):
    r = 0.11 * h
    head_cy = base_y - h + r
    draw.ellipse([cx - r, head_cy - r, cx + r, head_cy + r], fill=val)
    bw = 0.22 * h
    top = head_cy + 0.9 * r
    draw.ellipse([cx - bw, top, cx + bw, base_y], fill=val)

def make_template(camera: str, n_chars: int = 1, size: int = 512) -> Image.Image:
    """Depth-style layout map (bright = near). n_chars = 0 gives background only."""
    S = size
    p = CAMERA[camera]
    arr = np.full((S, S), 25, dtype=np.uint8)
    if p["horizon"] is None:
        arr[:] = 90
    else:
        hy = int(p["horizon"] * S)
        arr[hy:] = np.linspace(60, 150, S - hy).astype(np.uint8)[:, None]
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)

    if n_chars > 0:
        if camera == "over_shoulder":
            _figure(d, 0.12 * S, 1.20 * S, 1.10 * S, val=250)      # foreground shoulder
            _figure(d, 0.65 * S, p["base"] * S, p["h"] * S, val=190)  # subject
        else:
            scale = 1.0 if n_chars == 1 else 0.85
            xs = [0.5] if n_chars == 1 else [0.35, 0.65]
            for x in xs[:n_chars]:
                _figure(d, x * S, p["base"] * S, p["h"] * S * scale)
    img = img.filter(ImageFilter.GaussianBlur(5))
    return img.convert("RGB")


# ---- v2: shape-neutral ellipse blobs, flat ground ----
# (cx, cy, w, h) as fractions of the image; horizon as fraction of height (None = no horizon)
CAMERA_V2 = {
    "wide":          dict(blob=(0.50, 0.72, 0.22, 0.14), horizon=0.55),
    "medium":        dict(blob=(0.50, 0.68, 0.45, 0.35), horizon=0.45),
    "close_up":      dict(blob=(0.50, 0.58, 0.70, 0.60), horizon=0.35),
    "over_shoulder": dict(blob=(0.65, 0.62, 0.25, 0.20), horizon=0.45),
    "top_down":      dict(blob=(0.50, 0.50, 0.25, 0.25), horizon=None),
}

def make_template_v2(camera: str, n_chars: int = 1, size: int = 512) -> Image.Image:
    S = size
    p = CAMERA_V2[camera]
    arr = np.full((S, S), 25, dtype=np.uint8)
    if p["horizon"] is None:
        arr[:] = 100
    else:
        arr[int(p["horizon"] * S):] = 100
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)

    def blob(cx, cy, w, h, val=200):
        d.ellipse([(cx - w / 2) * S, (cy - h / 2) * S, (cx + w / 2) * S, (cy + h / 2) * S], fill=val)

    if n_chars > 0:
        cx, cy, w, h = p["blob"]
        if camera == "over_shoulder":
            blob(0.15, 0.95, 0.40, 0.50, val=240)        # foreground shoulder
            blob(cx, cy, w, h, val=190)
        elif n_chars == 1:
            blob(cx, cy, w, h)
        else:
            for x in (0.35, 0.65):
                blob(x, cy, w * 0.8, h * 0.9)
    return img.filter(ImageFilter.GaussianBlur(10)).convert("RGB")

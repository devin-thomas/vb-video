"""Derive the XTRA-17 editorial frame and 720p proofs from source/original.png.

The editorial frame is a pixel-exact crop of the top 1920x1080 of the original
(Wayback banner + petition heading + objectives). No resampling, no stretching,
no overlays. source/original.png is opened read-only and never written.
Run from the repository root: python assets/historical/XTRA-17/evidence/frame.py
"""
import hashlib
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.png"
FRAME = BASE / "exports" / "editorial-frame.png"
PROOF_FRAME = BASE / "proofs" / "editorial-frame-720.png"
PROOF_ORIGINAL = BASE / "proofs" / "original-720h.png"
CROP_BOX = (0, 0, 1920, 1080)

before = hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()
with Image.open(ORIGINAL) as im:
    src = im.convert("RGB")
    assert src.size[0] == 1920, src.size

frame = src.crop(CROP_BOX)
assert frame.size == (1920, 1080)
FRAME.parent.mkdir(exist_ok=True)
frame.save(FRAME, optimize=True)

PROOF_FRAME.parent.mkdir(exist_ok=True)
frame.resize((1280, 720), Image.LANCZOS).save(PROOF_FRAME, optimize=True)

# Whole uncropped page at 720 px tall, uniform scale (aspect preserved).
w, h = src.size
scale = 720 / h
src.resize((round(w * scale), 720), Image.LANCZOS).save(PROOF_ORIGINAL, optimize=True)

after = hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()
assert before == after, "original changed"
print("original", src.size, before)
print("frame", frame.size, "crop", CROP_BOX)
print("proofs", Image.open(PROOF_FRAME).size, Image.open(PROOF_ORIGINAL).size)

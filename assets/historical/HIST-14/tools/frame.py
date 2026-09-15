"""HIST-14 editorial framing: fit the untouched original inside 1920x1080 without cropping or stretching.

Usage: python assets/historical/HIST-14/tools/frame.py <original> <out_dir_root>

The original is never modified. The transform is a uniform scale plus centred pillarbox/letterbox,
recorded in evidence/framing.json so it can be reversed exactly (up to resampling).
"""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps, ImageStat, __version__ as PIL_VERSION

W, H = 1920, 1080


def border_fill(img: Image.Image) -> tuple[int, int, int]:
    """Median colour of a 2 px outer border, so the matte continues the photo's own backdrop."""
    w, h = img.size
    strips = [img.crop((0, 0, w, 2)), img.crop((0, h - 2, w, h)),
              img.crop((0, 0, 2, h)), img.crop((w - 2, 0, w, h))]
    meds = [ImageStat.Stat(s).median for s in strips]
    return tuple(int(sorted(m[c] for m in meds)[len(meds) // 2]) for c in range(3))


def main() -> None:
    src = Path(sys.argv[1])
    root = Path(sys.argv[2])
    raw = Image.open(src)
    exif_orientation = raw.getexif().get(0x0112)
    img = ImageOps.exif_transpose(raw).convert("RGB")  # identity when orientation is absent or 1
    ow, oh = img.size
    scale = min(W / ow, H / oh)
    sw, sh = round(ow * scale), round(oh * scale)
    ox, oy = (W - sw) // 2, (H - sh) // 2
    fill = border_fill(img)

    canvas = Image.new("RGB", (W, H), fill)
    canvas.paste(img.resize((sw, sh), Image.Resampling.LANCZOS), (ox, oy))

    exports = root / "exports"
    proofs = root / "proofs"
    evidence = root / "evidence"
    for d in (exports, proofs, evidence):
        d.mkdir(parents=True, exist_ok=True)
    frame_path = exports / "editorial-frame.png"
    canvas.save(frame_path, optimize=True)
    proof_path = proofs / "editorial-frame-720.png"
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proof_path, optimize=True)

    record = {
        "input": src.as_posix(),
        "input_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "input_dimensions": [ow, oh],
        "exif_orientation_tag": exif_orientation,
        "output": "exports/editorial-frame.png",
        "output_dimensions": [W, H],
        "operation": "uniform scale to fit, centred on a solid matte; no crop, no stretch, no retouching",
        "scale": scale,
        "scaled_dimensions": [sw, sh],
        "offset": [ox, oy],
        "matte_rgb": list(fill),
        "matte_rule": "median of the four 2 px outer border strips of the original",
        "resampling": "Pillow LANCZOS",
        "reverse": f"crop exports/editorial-frame.png to box ({ox},{oy},{ox + sw},{oy + sh}) and resize by 1/scale to {ow}x{oh}",
        "proof_720": "proofs/editorial-frame-720.png",
        "pillow": PIL_VERSION,
    }
    (evidence / "framing.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()

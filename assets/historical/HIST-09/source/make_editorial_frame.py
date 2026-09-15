"""HIST-09 editorial framing: reversible crop + uniform scale, no stretching, no overlays."""
import json, sys
from pathlib import Path
from PIL import Image
base = Path(sys.argv[1])
src = Image.open(base / "source/original.png").convert("RGB")
assert src.size == (854, 480), src.size
# 4:3 camcorder picture inside the 16:9 pillarboxed upload: 640x480 at x=107 (measured content bbox x=111..743)
crop = (107, 0, 747, 480)
scale = 2.25
pic = src.crop(crop)
out_w, out_h = round(pic.width * scale), round(pic.height * scale)   # 1440x1080, uniform
pic = pic.resize((out_w, out_h), Image.Resampling.LANCZOS)
canvas = Image.new("RGB", (1920, 1080), (0, 0, 0))
offset = ((1920 - out_w) // 2, (1080 - out_h) // 2)                   # (240, 0)
canvas.paste(pic, offset)
(base / "exports").mkdir(exist_ok=True); (base / "proofs").mkdir(exist_ok=True)
canvas.save(base / "exports/editorial-frame.png", optimize=False)
canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(base / "proofs/editorial-frame-720.png")
framing = {
    "source": "source/original.png", "source_size": list(src.size),
    "crop_box_xyxy": list(crop), "crop_size": [crop[2]-crop[0], crop[3]-crop[1]],
    "uniform_scale": scale, "resample": "Pillow LANCZOS", "scaled_size": [out_w, out_h],
    "canvas": [1920, 1080], "canvas_fill_rgb": [0, 0, 0], "paste_offset": list(offset),
    "inverse": "crop exports/editorial-frame.png to (240,0,1680,1080), downscale by 1/2.25 to 640x480, place at x=107 on an 854x480 black canvas (lossy only through resampling); the untouched original is source/original.png",
    "removed_content": "Only the upload's black pillarbox columns x<107 and x>=747 (max luma <= 5; measured picture bbox x=111..743). No picture content removed.",
    "overlays_added": [], "watermarks_removed": False,
    "camcorder_date_stamp": "Retained exactly as recorded (AUG. 24 1995); it is part of the original picture.",
    "proof_720": "proofs/editorial-frame-720.png",
}
(base / "evidence/framing.json").write_text(json.dumps(framing, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(framing, indent=1))

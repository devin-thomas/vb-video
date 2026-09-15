"""Check the editorial frame reverses exactly to the chosen original frame, and the canvas outside it is untouched."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageSequence

asset = Path(sys.argv[1])
rec = json.loads((asset / "evidence/framing.json").read_text(encoding="utf-8"))
export = Image.open(asset / "exports/editorial-frame.png").convert("RGB")
src = Image.open(asset / "source/original.gif")
frame = [f.copy() for f in ImageSequence.Iterator(src)][rec["frame_used"]].convert("RGB")

x, y = rec["placement"]["x"], rec["placement"]["y"]
sw, sh = rec["scaled_size"]
s = rec["scale"]
region = export.crop((x, y, x + sw, y + sh))
recovered = region.resize((sw // s, sh // s), Image.NEAREST)
exact = list(recovered.getdata()) == list(frame.getdata())
# every scaled block must be uniform (true nearest-neighbour, no blending)
uniform = all(
    len({region.getpixel((bx * s + dx, by * s + dy)) for dx in range(s) for dy in range(s)}) == 1
    for by in range(sh // s) for bx in range(sw // s)
)
bg = tuple(int(rec["background"][i:i + 2], 16) for i in (1, 3, 5))
outside = [export.getpixel((px, py)) for py in range(export.height) for px in range(export.width)
           if not (x <= px < x + sw and y <= py < y + sh)]
result = {
    "export_size": export.size,
    "recovers_frame_exactly": exact,
    "scaled_blocks_uniform": uniform,
    "outside_pixels": len(outside),
    "outside_all_background": all(p == bg for p in outside),
    "colours_in_export": sorted("#%02X%02X%02X" % c for _, c in export.getcolors(1 << 16)),
    "inside_safe_band_y_72_1008": y >= 72 and y + sh <= 1008,
    "inside_safe_band_x_120_1800": x >= 120 and x + sw <= 1800,
}
print(json.dumps(result, indent=2))
sys.exit(0 if exact and uniform and result["outside_all_background"] else 1)

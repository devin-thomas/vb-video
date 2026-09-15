"""Measure the delivered GIF: palette/transparency use, screen area, text rows, cursor cell."""
import sys
from collections import Counter

from PIL import Image, ImageSequence

path = sys.argv[1]
src = Image.open(path)
pal = src.getpalette() or []
print("size", src.size, "transparency index", src.info.get("transparency"), "background index", src.info.get("background"))
print("palette entries (first 8):", [tuple(pal[i * 3:i * 3 + 3]) for i in range(min(8, len(pal) // 3))])
frames = [f.copy() for f in ImageSequence.Iterator(src)]
for n, f in enumerate(frames):
    print("frame", n, "mode", f.mode, "index usage", dict(Counter(f.getdata())), "frame transparency", f.info.get("transparency"))

rgb = frames[0].convert("RGB")
w, h = rgb.size
screen = (0x42, 0x42, 0xE7)
xs = [x for x in range(w) for y in range(h) if rgb.getpixel((x, y)) == screen]
ys = [y for y in range(h) for x in range(w) if rgb.getpixel((x, y)) == screen]
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
print("screen colour bbox", (x0, y0, x1, y1), "size", (x1 - x0 + 1, y1 - y0 + 1))
print("border: left", x0, "right", w - 1 - x1, "top", y0, "bottom", h - 1 - y1)
rows = []
for r in range((y1 - y0 + 1) // 8):
    band = [(x, y) for y in range(y0 + r * 8, y0 + r * 8 + 8) for x in range(x0, x1 + 1) if rgb.getpixel((x, y)) != screen]
    if band:
        cols = sorted({(x - x0) // 8 for x, _ in band})
        rows.append(r)
        print("text row", r, "columns", cols[0], "to", cols[-1], "count", len(cols))
f1 = frames[1].convert("RGB")
diff = [(x, y) for y in range(h) for x in range(w) if rgb.getpixel((x, y)) != f1.getpixel((x, y))]
if diff:
    dx = min(p[0] for p in diff); dy = min(p[1] for p in diff)
    print("cursor cell: column", (dx - x0) // 8, "row", (dy - y0) // 8, "offset exact", (dx - x0) % 8 == 0 and (dy - y0) % 8 == 0,
          "cursor visible in frame", 1 if f1.getpixel((dx, dy)) != screen else 0)

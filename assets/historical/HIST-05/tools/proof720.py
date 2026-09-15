"""Make a 1280x720 review proof of a 1920x1080 export (Lanczos, as an HD timeline would scale it)."""
import sys

from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
img = Image.open(src)
assert img.size == (1920, 1080), img.size
img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(dst, format="PNG", optimize=True)
print("wrote", dst, Image.open(dst).size)

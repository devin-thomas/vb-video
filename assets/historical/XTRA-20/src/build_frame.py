#!/usr/bin/env python3
"""XTRA-20 editorial frame: typeset rendering of the archived access.lst text file.

Reads source/original.txt (byte-exact copy of access.lst), writes src/editorial-frame.svg,
exports/editorial-frame.png (1920x1080) and qa/editorial-frame-720p.png (1280x720).
Listing text is decoded from CP437 and placed unchanged; every rendered listing line is
checked against the source before export. Line numbers, the gap marker, the highlight
and the sidebar are authored display layers. Fonts are installed system fonts
(Consolas, Segoe UI); no font files are bundled and nothing is fetched.

Widths are measured from the fonts' own advance widths (fontTools, no kerning), which
matches or slightly exceeds what cairo draws, so layout checks err on the safe side.
"""
from __future__ import annotations
import hashlib
import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from fontTools.ttLib import TTFont
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'source/original.txt'
SOURCE_SHA256 = '883c34aefc363c4acaa5b1db9586e446b69fb9961935b70a666799ce6b875bc2'
SVG_OUT = BASE / 'src/editorial-frame.svg'
PNG_OUT = BASE / 'exports/editorial-frame.png'
PROOF_720 = BASE / 'qa/editorial-frame-720p.png'

W, H = 1920, 1080
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 120, 1800, 72, 1008
BG = '#111318'; PANEL = '#1b2027'; FG = '#f1f3f5'; MUTED = '#aeb6bf'; LINE = '#343d48'; GOLD = '#eab676'
MONO = 'Consolas'; SANS = 'Segoe UI'
FONT_FILES = {'mono': r'C:\Windows\Fonts\consola.ttf', 'sans': r'C:\Windows\Fonts\segoeui.ttf',
              'bold': r'C:\Windows\Fonts\segoeuib.ttf'}

# Source line ranges (1-based, inclusive) shown in the frame, and the highlighted entry.
BLOCKS = [(541, 548), (586, 599)]
HIGHLIGHT = (591, 592)

MONO_SIZE = 28
LEADING = 35
NUM_X = 162          # right edge of line-number column
TEXT_X = 178         # listing text origin
TOP = 118            # first baseline
PAD = 16             # panel padding right of the 80th column

_fonts: dict[str, tuple[dict, object, int]] = {}


def font(face: str):
    if face not in _fonts:
        f = TTFont(FONT_FILES[face])
        _fonts[face] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    return _fonts[face]


def text_width(s: str, face: str, size: float) -> float:
    cmap, hmtx, upem = font(face)
    total = 0
    for ch in s:
        glyph = cmap.get(ord(ch))
        if glyph is None:
            sys.exit(f'{face} font has no glyph for U+{ord(ch):04X}')
        total += hmtx[glyph][0]
    return total * size / upem


def source_lines() -> list[str]:
    raw = SOURCE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        sys.exit(f'source/original.txt hash changed: {digest}')
    return raw.decode('cp437').split('\r\n')


def wrap(s: str, limit: float, face: str, size: int) -> list[str]:
    out, cur = [], ''
    for word in s.split():
        trial = f'{cur} {word}'.strip()
        if text_width(trial, face, size) <= limit or not cur:
            cur = trial
        else:
            out.append(cur); cur = word
    if cur:
        out.append(cur)
    for line_ in out:
        if text_width(line_, face, size) > limit:
            sys.exit(f'unwrappable sidebar text: {line_!r}')
    return out


def t(x, y, s, size, fill, family, weight=400, anchor='start', cls=None, extra=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<text{c} x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve"{extra}>'
            f'{html.escape(s, quote=False)}</text>')


def build() -> tuple[str, list[tuple[int, str]]]:
    lines = source_lines()
    shown = [lines[n - 1] for lo, hi in BLOCKS for n in range(lo, hi + 1)]
    listing_right = TEXT_X + max(text_width(s, 'mono', MONO_SIZE) for s in shown)
    col80 = TEXT_X + text_width('=' * 80, 'mono', MONO_SIZE)
    listing_right = max(listing_right, col80)
    panel_right = listing_right + PAD
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="{BG}"/>',
             f'<rect x="{SAFE_X0}" y="{SAFE_Y0}" width="{panel_right - SAFE_X0:.1f}" '
             f'height="{SAFE_Y1 - SAFE_Y0}" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>']
    rendered: list[tuple[int, str]] = []
    y = TOP
    for bi, (lo, hi) in enumerate(BLOCKS):
        if bi:
            prev_hi = BLOCKS[bi - 1][1]
            gap = f'source lines {prev_hi + 1}\u2013{lo - 1} not shown'
            mid = (TEXT_X + listing_right) / 2
            gw = text_width(gap, 'sans', 24) + 32
            gy = y - 12
            parts.append(f'<line x1="{TEXT_X}" y1="{gy}" x2="{listing_right:.1f}" y2="{gy}" '
                         f'stroke="{LINE}" stroke-width="2" stroke-dasharray="8 8"/>')
            parts.append(f'<rect x="{mid - gw / 2:.1f}" y="{gy - 18}" width="{gw:.1f}" height="36" fill="{PANEL}"/>')
            parts.append(t(mid, gy + 8, gap, 24, MUTED, SANS, anchor='middle'))
            y += LEADING
        for n in range(lo, hi + 1):
            s = lines[n - 1]
            if n == HIGHLIGHT[0]:
                hh = (HIGHLIGHT[1] - HIGHLIGHT[0] + 1) * LEADING
                hl_right = TEXT_X + max(text_width(lines[k - 1].rstrip(), 'mono', MONO_SIZE)
                                        for k in range(HIGHLIGHT[0], HIGHLIGHT[1] + 1))
                parts.append(f'<rect x="{TEXT_X - 10}" y="{y - 27}" width="{hl_right - TEXT_X + 20:.1f}" '
                             f'height="{hh + 2}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
            parts.append(t(NUM_X, y, str(n), 20, MUTED, MONO, anchor='end'))
            parts.append(t(TEXT_X, y, s, MONO_SIZE, FG, MONO, cls='listing', extra=f' data-line="{n}"'))
            rendered.append((n, s))
            y += LEADING
    last_baseline = y - LEADING
    if last_baseline > SAFE_Y1 - 16:
        sys.exit(f'listing overflows safe area: last baseline {last_baseline}')
    if NUM_X - text_width('599', 'mono', 20) < SAFE_X0 + 4:
        sys.exit('line numbers overflow safe area')

    # Sidebar: authored labels, not listing text.
    sx = panel_right + 40
    sw = SAFE_X1 - sx
    sy = 146
    for line_ in wrap('Archived BBS file listing', sw, 'bold', 34):
        parts.append(t(sx, sy, line_, 34, FG, SANS, 700)); sy += 44
    sy += 12
    for line_ in wrap('The Access System, Huntsville, AL', sw, 'sans', 28) + ['Catalog dated 09/09/1992']:
        parts.append(t(sx, sy, line_, 28, FG, SANS)); sy += 38
    sy += 22
    parts.append(f'<rect x="{sx}" y="{sy - 22}" width="{sw:.1f}" height="4" fill="{GOLD}"/>')
    sy += 22
    for line_ in wrap('Highlighted: the Visual Basic runtime as its own download. No version is stated.',
                      sw, 'sans', 26):
        parts.append(t(sx, sy, line_, 26, FG, SANS)); sy += 35
    sy += 28
    for line_ in wrap('Typeset rendering of the archived text file. Listing text unchanged; line numbers, '
                      'gap marker and highlight added. Not a live board screen.', sw, 'sans', 26):
        parts.append(t(sx, sy, line_, 26, MUTED, SANS)); sy += 35
    sy += 28
    for line_ in ['Source: textfiles.com', '/bbs/FILELISTS/access.lst', 'Accessed 2026-09-15']:
        if text_width(line_, 'sans', 26) > sw:
            sys.exit(f'sidebar source line too wide: {line_}')
        parts.append(t(sx, sy, line_, 26, MUTED, SANS)); sy += 35
    if sy - 35 > SAFE_Y1 - 8:
        sys.exit(f'sidebar overflows safe area: last baseline {sy - 35}')
    parts.append('</svg>')
    print(f'listing right {listing_right:.1f}, panel right {panel_right:.1f}, sidebar x {sx:.1f} width {sw:.1f}, '
          f'listing last baseline {last_baseline}, sidebar last baseline {sy - 35}')
    return '\n'.join(parts) + '\n', rendered


def verify(svg: str, rendered: list[tuple[int, str]]) -> None:
    lines = source_lines()
    root = ET.fromstring(svg)
    ns = '{http://www.w3.org/2000/svg}'
    nodes = [el for el in root.iter(f'{ns}text') if el.get('class') == 'listing']
    if len(nodes) != len(rendered):
        sys.exit('listing node count mismatch')
    for el, (n, s) in zip(nodes, rendered):
        if int(el.get('data-line')) != n or (el.text or '') != lines[n - 1] or s != lines[n - 1]:
            sys.exit(f'listing text differs from source at line {n}')
    print(f'verified {len(nodes)} listing lines against source/original.txt (CP437, CRLF split)')


def main() -> None:
    svg, rendered = build()
    verify(svg, rendered)
    SVG_OUT.write_text(svg, encoding='utf-8', newline='\n')
    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=str(PNG_OUT), output_width=W, output_height=H)
    im = Image.open(PNG_OUT)
    if im.size != (W, H):
        sys.exit(f'unexpected export size {im.size}')
    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    im.convert('RGB').resize((1280, 720), Image.LANCZOS).save(PROOF_720)
    print('wrote', SVG_OUT.relative_to(BASE), PNG_OUT.relative_to(BASE), PROOF_720.relative_to(BASE))


if __name__ == '__main__':
    main()

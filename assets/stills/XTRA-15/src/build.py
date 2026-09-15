#!/usr/bin/env python3
"""XTRA-15 authoring script: Windows XP office / legacy VB6 scene (reconstruction).

Run from the repository root:  python assets/stills/XTRA-15/src/build.py
Writes editable SVG source, offline HTML, timeline, and build driver.
Rendering, browser checks and delivery finishing use tools/render with --id XTRA-15.
build_assets.py has no XTRA-15 composition, so this script replaces it here.

Editorial decisions (project owner approved):
  - Reconstruction approach: no documentary photo with adequate provenance was found.
    This is an authored reconstruction, explicitly labeled as such.
  - Source app: XTRA-11 (INVOICE-IT for Windows, a documented VB business application)
    is used as the on-screen application. Its VB provenance is documented independently
    (publisher's RELEASE.TXT names Visual Basic 2.0 and VBRUN200.DLL).
  - No Bliss wallpaper: rights unclear. A plain/generic XP desktop is used instead.
  - Internal proof only; not cleared for final release.
"""
from __future__ import annotations
import base64, hashlib, html as htmlmod, io, json, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]   # src -> XTRA-15 -> stills -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import (SVG, BG, PANEL, FG, MUTED, LINE, BLUE,
                    SANS, MONO, FONT_PATHS, width, wrap)

ID = 'XTRA-15'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)

# -- XP Luna color palette (authored reconstruction, not claimed pixel-accurate) --
XP_DESKTOP = '#3a6ea5'        # Default XP desktop blue (without Bliss wallpaper)
XP_TASKBAR = '#245ddb'        # Taskbar blue
XP_TASKBAR_TOP = '#3a7bf7'    # Taskbar gradient top edge
XP_START_GREEN = '#3c9a3c'    # Start button green
XP_START_DARK = '#287228'     # Start button darker edge
XP_TITLE_LEFT = '#0054e3'     # XP window title bar left
XP_TITLE_RIGHT = '#3a7bf7'    # XP window title bar right
XP_TITLE_BOTTOM = '#0046c8'   # Below title gradient
XP_FRAME = '#0054e3'          # Window frame border
XP_CLIENT = '#ece9d8'         # Classic XP client area background
XP_CLOCK = '#0f3b80'          # System tray area
RECONSTRUCTION_RED = '#c04040' # Label color


def load_upstream():
    """Read the XTRA-11 original screenshot and verify its hash."""
    up = ROOT / 'assets' / 'historical' / 'XTRA-11'
    raw = (up / 'source' / 'original.jpg').read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    delivery = json.loads((up / 'delivery.json').read_text(encoding='utf-8'))
    recorded = next(o for o in delivery['outputs'] if o['path'] == 'source/original.jpg')
    assert sha == recorded['sha256'] and len(raw) == recorded['bytes'], \
        'XTRA-11 original differs from its delivery.json record'
    img = Image.open(io.BytesIO(raw)).convert('RGB')
    return img, sha, len(raw)


def embed_png(img):
    """Convert a PIL Image to a PNG data URI."""
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    png = buf.getvalue()
    uri = 'data:image/png;base64,' + base64.b64encode(png).decode('ascii')
    return uri, hashlib.sha256(png).hexdigest(), len(png)


def build_scene_svg(img, title):
    """Compose the XTRA-15 reconstruction scene as an SVG."""
    s = SVG(BG, title)

    # -- Layout constants --
    # Screen area: a monitor-like rectangle on the dark canvas
    scr_x, scr_y = 160, 68
    scr_w, scr_h = 1600, 900
    taskbar_h = 36
    desktop_h = scr_h - taskbar_h

    # -- Monitor bezel (thin dark border around the screen) --
    bezel = 4
    s.rect(scr_x - bezel, scr_y - bezel,
           scr_w + 2 * bezel, scr_h + 2 * bezel,
           '#2a2a2a', '#444444', 2, rx=3)

    # -- XP Desktop background (plain blue, no Bliss) --
    s.rect(scr_x, scr_y, scr_w, desktop_h, XP_DESKTOP)

    # -- XP Taskbar --
    tb_y = scr_y + desktop_h
    # Taskbar gradient (simplified as two bands)
    s.rect(scr_x, tb_y, scr_w, 2, XP_TASKBAR_TOP)
    s.rect(scr_x, tb_y + 2, scr_w, taskbar_h - 2, XP_TASKBAR)

    # Start button (green pill shape, left side of taskbar)
    start_w, start_h = 108, taskbar_h - 4
    start_x, start_y = scr_x + 2, tb_y + 2
    s.rect(start_x, start_y, start_w, start_h, XP_START_GREEN, rx=4)
    # Windows logo (simplified colored squares)
    logo_x, logo_y = start_x + 8, start_y + 7
    logo_s = 8  # square size
    logo_g = 2  # gap
    # Four colored squares (red, green, blue, yellow)
    s.rect(logo_x, logo_y, logo_s, logo_s, '#ff2020')
    s.rect(logo_x + logo_s + logo_g, logo_y, logo_s, logo_s, '#20b020')
    s.rect(logo_x, logo_y + logo_s + logo_g, logo_s, logo_s, '#2060ff')
    s.rect(logo_x + logo_s + logo_g, logo_y + logo_s + logo_g, logo_s, logo_s, '#ffcc00')
    # "start" text
    s.text('start', start_x + 36, start_y + start_h - 7, 20, '#ffffff', bold=True)

    # Clock area (right side of taskbar)
    clock_w = 80
    clock_x = scr_x + scr_w - clock_w - 4
    clock_y = tb_y + 3
    s.rect(clock_x, clock_y, clock_w, taskbar_h - 6, XP_CLOCK, rx=2)
    s.text('2:47 PM', clock_x + 8, clock_y + taskbar_h - 14, 16, '#ffffff')

    # Taskbar button for the app (showing it's "running")
    btn_x = start_x + start_w + 6
    btn_w = 180
    btn_h = taskbar_h - 6
    s.rect(btn_x, tb_y + 3, btn_w, btn_h, '#1c4db5', rx=2)
    s.rect(btn_x, tb_y + 3, btn_w, 2, '#5590f0')
    s.text('INVOICE-IT FOR ...', btn_x + 6, tb_y + taskbar_h - 9, 14, '#ffffff')

    # -- XP Window with INVOICE-IT app --
    # Position the app window on the desktop
    # The original image is 591x423. Scale it up by 2x = 1182x846.
    # That's too big for the desktop area. Let me fit it appropriately.
    # Available desktop area: scr_w x desktop_h = 1600 x 864
    # Want to show the app centered with some desktop showing around it.
    # Use ~1.8x scale: 591*1.8=1064, 423*1.8=761 - good fit with room around it.
    img_w, img_h = img.size  # 591, 423
    scale = 1.7
    placed_w = round(img_w * scale)
    placed_h = round(img_h * scale)

    # XP window chrome dimensions
    title_h = 30
    frame_w = 4  # frame border width on sides/bottom
    win_w = placed_w + 2 * frame_w
    win_h = placed_h + title_h + frame_w  # title + content + bottom frame
    win_x = scr_x + (scr_w - win_w) // 2
    win_y = scr_y + (desktop_h - win_h) // 2 - 10  # slightly above center

    # Window outer frame
    s.rect(win_x, win_y, win_w, win_h, XP_FRAME, rx=5)
    # Title bar (blue gradient - simplified as solid with highlight)
    s.rect(win_x, win_y, win_w, title_h, XP_TITLE_LEFT, rx=5)
    # Title bar top highlight
    s.rect(win_x + 2, win_y + 2, win_w - 4, 12, XP_TITLE_RIGHT, rx=3, opacity=0.5)
    # Title text
    s.text('INVOICE-IT FOR WINDOWS', win_x + 10, win_y + title_h - 8, 16, '#ffffff', bold=True)

    # Window control buttons (minimize, maximize, close)
    btn_size = 18
    btn_gap = 2
    close_x = win_x + win_w - btn_size - 8
    max_x = close_x - btn_size - btn_gap
    min_x = max_x - btn_size - btn_gap

    # Close button (red)
    s.rect(close_x, win_y + 5, btn_size, btn_size, '#e04343', rx=2)
    s.path(f'M{close_x+5} {win_y+10}l{btn_size-10} {btn_size-10}m-{btn_size-10} 0l{btn_size-10} -{btn_size-10}', '#ffffff', 1.8)

    # Maximize button
    s.rect(max_x, win_y + 5, btn_size, btn_size, '#3567c4', rx=2)
    s.rect(max_x + 4, win_y + 9, btn_size - 8, btn_size - 8, 'none', '#ffffff', 1.5)

    # Minimize button
    s.rect(min_x, win_y + 5, btn_size, btn_size, '#3567c4', rx=2)
    s.line(min_x + 4, win_y + 5 + btn_size - 6, min_x + btn_size - 4, win_y + 5 + btn_size - 6, '#ffffff', 1.8)

    # Client area background
    client_x = win_x + frame_w
    client_y = win_y + title_h
    client_w = placed_w
    client_h = placed_h
    s.rect(client_x, client_y, client_w, client_h, XP_CLIENT)

    # Embed the XTRA-11 screenshot
    uri, _, _ = embed_png(img.resize((placed_w, placed_h), Image.Resampling.LANCZOS))
    s.raw(
        f'<image x="{client_x}" y="{client_y}" '
        f'width="{placed_w}" height="{placed_h}" '
        f'preserveAspectRatio="none" '
        f'image-rendering="optimizeSpeed" '
        f'href="{uri}">'
        f'<title>XTRA-11: INVOICE-IT for Windows (documented VB business application)</title>'
        f'</image>'
    )

    # -- Reconstruction label (below the monitor, within safe area) --
    label_y = scr_y + scr_h + bezel + 8
    s.text('RECONSTRUCTION', 160, label_y + 30, 28, RECONSTRUCTION_RED, bold=True)
    s.text('Authored scene  |  App source: INVOICE-IT for Windows (XTRA-11, VB 2.0 provenance)',
           160, label_y + 58, 20, MUTED)
    s.text('Not a documentary photograph. Windows XP desktop is a stylistic reconstruction.',
           160, label_y + 80, 18, MUTED)

    return s.finish()


def main():
    img, upstream_sha, upstream_bytes = load_upstream()
    title = 'Windows XP office / legacy VB6 scene (reconstruction)'

    svg = build_scene_svg(img, title)

    # Write poster/scene SVG
    (HERE / 'scene.svg').write_text(svg, encoding='utf-8', newline='\n')

    # Write variant SVG (legacy-scene is the same as poster for this still)
    (HERE / 'variant-legacy-scene.svg').write_text(svg, encoding='utf-8', newline='\n')

    # Write timeline.json
    timeline = {
        'id': ID,
        'durationSeconds': None,
        'fps': None,
        'width': W,
        'height': H,
        'beats': ROW['beats'],
        'frames': [{'time': 0, 'file': 'scene.svg'}],
        'cuts': {},
        'variant_names': ['legacy-scene'],
        'motion_model': 'Still asset: one state held for editorial timing.'
    }
    (HERE / 'timeline.json').write_text(
        json.dumps(timeline, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write build.json (render driver)
    script_path = ROOT / 'sources' / 'SCRIPT.md'
    script_hash = hashlib.sha256(script_path.read_bytes()).hexdigest()
    build = {
        'id': ID,
        'duration': None,
        'frames': [{'time': 0, 'file': 'scene.svg'}],
        'variants': {'legacy-scene': 'variant-legacy-scene.svg'},
        'poster': 'scene.svg',
        'cuts': {},
        'notes': [
            'Authored reconstruction: Windows XP desktop with a legacy VB business application.',
            'Application source: XTRA-11 (INVOICE-IT for Windows v2.06, Eastern Digital Resources, 1993). VB provenance: publisher documentation names Visual Basic 2.0 and VBRUN200.DLL.',
            'Desktop: generic XP appearance with plain blue background (no Bliss wallpaper; rights unclear).',
            'Explicitly labeled "Reconstruction" on screen. Not a documentary photograph.',
            'Internal proof only; release blocked under R01, R11, R14 pending the review deck.',
        ],
        'sources': [
            {
                'path': '../../../sources/SCRIPT.md',
                'lines': [691, 693],
                'sha256': script_hash,
                'relationship': 'source creative brief (VISUAL cue at line 693)',
            },
            {
                'path': '../../historical/XTRA-11/source/original.jpg',
                'asset': 'XTRA-11',
                'sha256': upstream_sha,
                'relationship': 'historical original from a produced upstream asset; uniformly scaled, not cropped',
            },
        ],
        'kind': 'still',
    }
    (HERE / 'build.json').write_text(
        json.dumps(build, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write brief.json (ticket data snapshot)
    brief = {k: ROW[k] for k in ['id', 'title', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates']}
    (HERE / 'brief.json').write_text(
        json.dumps(brief, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write the exact on-screen copy for traceability
    copy_text = '\n'.join([
        '# XTRA-15 on-screen copy (authored reconstruction, not from sources/)',
        '',
        'Scene: Windows XP desktop running a legacy VB business application.',
        '',
        'On-screen elements (all authored reconstruction, not documentary):',
        '  - Windows XP Luna-style desktop with plain blue background (no Bliss wallpaper)',
        '  - XP taskbar with Start button, app button, clock',
        '  - INVOICE-IT FOR WINDOWS application in XP window chrome',
        '  - Application content: XTRA-11 upstream screenshot (unmodified pixel content)',
        '',
        'Labels:',
        '  RECONSTRUCTION',
        '  Authored scene  |  App source: INVOICE-IT for Windows (XTRA-11, VB 2.0 provenance)',
        '  Not a documentary photograph. Windows XP desktop is a stylistic reconstruction.',
        '',
        'No present-day usage claim, no "today in 2024" wording, no business data.',
    ])
    (HERE / 'copy.txt').write_text(copy_text, encoding='utf-8', newline='\n')

    # Write inline HTML (same contract as other assets)
    table = {'scene.svg': svg}
    html_doc = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + htmlmod.escape(ROW['title']) + '</title>'
        '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}'
        '#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}'
        'svg{width:100%;height:100%;object-fit:contain}</style>'
        '<div id="stage" aria-label="' + htmlmod.escape(ROW['title'], quote=True) + '"></div>'
        '<script>'
        'const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';'
        'const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
        'const stage=document.getElementById(\'stage\');'
        'window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,'
        'fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,'
        'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));'
        'let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;'
        'else break}stage.innerHTML=scenes[f.file];return f.file}};'
        '__ASSET__.renderAt(0);'
        'document.addEventListener(\'keydown\',e=>'
        '{if(e.code===\'Home\')__ASSET__.renderAt(0)});'
        '</script></html>'
    )
    (HERE / 'index.html').write_text(html_doc, encoding='utf-8', newline='\n')

    print(f'AUTHORED {ID}: scene.svg, variant-legacy-scene.svg, index.html, build.json, timeline.json')


if __name__ == '__main__':
    main()

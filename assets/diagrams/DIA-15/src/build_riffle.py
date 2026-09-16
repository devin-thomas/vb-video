#!/usr/bin/env python3
"""DIA-15 — animated riffle shuffle. Deterministic scene generator plus the loop encoder.

Run from the package root:
  python assets/diagrams/DIA-15/src/build_riffle.py build        # scene SVGs, build.json, timeline.json, index.html
  python tools/render/render_assets.py --id DIA-15               # poster, riffle/loop stills, preview.mp4, riffle.mp4 (cut), keyframes
  python assets/diagrams/DIA-15/src/build_riffle.py encode-loop  # exports/loop.mp4 with the renderer's raster/encode recipe

Every frame is a pure function of time: state_main(t) and state_loop(t) return the 52 card placements for that
instant, so the HTML renderAt(seconds) and the MP4s share one authored state per 1/30 s. Card art is the shared
win95-workbench-1.1.0 back and faces drawn by tools/render/studio.py; nothing is copied from elsewhere.
"""
from __future__ import annotations
import hashlib, html, json, math, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # assets/diagrams/DIA-15/src
BASE = HERE.parent                              # assets/diagrams/DIA-15
ROOT = BASE.parents[2]                          # package root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
import studio  # noqa: E402  (read-only dependency: shared card primitives)

ID = 'DIA-15'
W, H, FPS = 1920, 1080, 30
CW, CH = 240, 336                               # card body, 1.667 × the shared 144 × 202 primitive
CENTRE = (960.0, 540.0)                         # squared deck
PILE = (960.0, 592.0)                           # ragged pile while riffling, before the square-up
HALF_DX, HALF_Y, HALF_ROT = 350.0, 468.0, 12.0  # the two halves: ±350 px from centre, tilted ∓12°
STEP = (0.3, -0.42)                             # stack offset per card index (deck thickness)
FLIGHT = 0.33                                   # seconds a card takes to drop from its half onto the pile
LIFT = 150.0                                    # px a dropping card rises at mid-flight (top-down 'lift' arc)
MAIN_DT, LOOP_DT = 0.045, 0.044                 # launch interval (52 cards)
FLASH_MAIN, FLASH_LOOP = (7, 18, 30, 41), (6, 20, 33, 44)   # launch indices whose face flashes mid-drop
MAIN_DURATION, LOOP_DURATION = 12.0, 4.0
# Main timeline phases (seconds): squared 0–1, split 1–2, riffle 2–5, square up 5–6, hold 6–12.
# Loop phases: apart 0–0.1, riffle 0.1–2.8, square up 2.8–3.4, split 3.4–3.9, apart 3.9–4.0 (frame 0 == last frame).


class LCG:
    """Tiny deterministic generator so every jitter value is reproducible from the seed."""
    def __init__(self, seed: int): self.x = seed
    def rnd(self) -> float:
        self.x = (self.x * 1103515245 + 12345) % 2**31
        return self.x / 2**31


def smooth(u: float) -> float:
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def ease_out(u: float) -> float:
    u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 2


def lerp(a, b, u): return a + (b - a) * u


def rot_about(px, py, cx, cy, deg):
    a = math.radians(deg); dx, dy = px - cx, py - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


def stack_centre(base, i, n):
    """Centre of card i in an n-card stack centred on base."""
    return base[0] + STEP[0] * (i - (n - 1) / 2), base[1] + STEP[1] * (i - (n - 1) / 2)


def half_base(side): return (CENTRE[0] - HALF_DX if side == 0 else CENTRE[0] + HALF_DX, HALF_Y)
def half_rot(side): return -HALF_ROT if side == 0 else HALF_ROT


def half_card(side, i):
    """Centre of card i (0 = bottom) of a 26-card half, after the whole half is tilted about its own centre."""
    b = half_base(side); x, y = stack_centre(b, i, 26)
    return rot_about(x, y, b[0], b[1], half_rot(side))


# ---------------------------------------------------------------- deck, riffle order, jitter
RANKS = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
DECK = [r + s for s in 'SHDC' for r in RANKS]


def initial_order() -> list[str]:
    rng = LCG(20260916); d = DECK[:]
    for i in range(51, 0, -1):
        j = int(rng.rnd() * (i + 1)); d[i], d[j] = d[j], d[i]
    return d


def riffle_sides(seed: int) -> list[int]:
    """52 drop sides (0 = left half, 1 = right half): mostly alternating, with the occasional double, 26 each."""
    rng = LCG(seed); sides = []; left = right = 26; cur = 0 if rng.rnd() < .5 else 1
    for k in range(52):
        if k and rng.rnd() < .78: cur = 1 - cur
        if cur == 0 and left == 0: cur = 1
        if cur == 1 and right == 0: cur = 0
        sides.append(cur)
        if cur == 0: left -= 1
        else: right -= 1
    return sides


def ragged(seed: int, sides: list[int]):
    """Per landing slot: (dx, dy, rot) — left-hand cards land nudged left and tilted one way, right-hand the other."""
    rng = LCG(seed); out = []
    for side in sides:
        sgn = -1 if side == 0 else 1
        out.append((sgn * 8 + (rng.rnd() - .5) * 8, (rng.rnd() - .5) * 6, sgn * 5 + (rng.rnd() - .5) * 5))
    return out


def launches(order: list[str], sides: list[int]):
    """(launch index k, side, stack index within the half, card) — each half releases from its top."""
    lp = rp = 25; out = []
    for k, side in enumerate(sides):
        if side == 0: si = lp; lp -= 1; card = order[si]
        else: si = rp; rp -= 1; card = order[26 + si]
        out.append((k, side, si, card))
    return out


def riffled_order(order, sides): return [c for _, _, _, c in launches(order, sides)]


# ---------------------------------------------------------------- states: lists of (card, cx, cy, rot, sx, sy, show_face)
def squared(order):
    return [(c, *stack_centre(CENTRE, i, 52), 0.0, 1.0, 1.0, False) for i, c in enumerate(order)]


def split(order, u):
    """Bottom 26 slide left, top 26 slide right, both tilting; u = 0 squared, u = 1 apart."""
    u = smooth(u); out = []
    for i, c in enumerate(order):
        side, si = (0, i) if i < 26 else (1, i - 26)
        x0, y0 = stack_centre(CENTRE, i, 52); x1, y1 = half_card(side, si)
        out.append((c, lerp(x0, x1, u), lerp(y0, y1, u), lerp(0.0, half_rot(side), u), 1.0, 1.0, False))
    return out


def flip(p: float):
    """Face-flash flip angle over a drop: quick to 90°, slow across the face-up span, quick back to 360°."""
    if p < .2: deg = 450 * p
    elif p < .8: deg = 90 + 300 * (p - .2)
    else: deg = 270 + 450 * (p - .8)
    return math.cos(math.radians(deg))


def riffle(order, tau, dt, flash, sides, rag):
    pile, flight = [], []; lp = rp = 25
    for k, side, si, card in launches(order, sides):
        tL = k * dt
        if tau < tL: break
        if side == 0: lp -= 1
        else: rp -= 1
        p = (tau - tL) / FLIGHT
        px, py = stack_centre(PILE, k, 52); dx, dy, drot = rag[k]
        ex, ey, erot = px + dx, py + dy, drot
        if p >= 1: pile.append((card, ex, ey, erot, 1.0, 1.0, False)); continue
        q = ease_out(p); sx0, sy0 = half_card(side, si); arc = math.sin(math.pi * p); s = 1 + .10 * arc
        cx, cy, rot = lerp(sx0, ex, q), lerp(sy0, ey, q) - LIFT * arc, lerp(half_rot(side), erot, q)
        sx, face = s, False
        if k in flash:
            c = flip(p); face = c < 0; sx = max(.04, abs(c)) * s
        flight.append((tL, (card, cx, cy, rot, sx, s, face)))
    left = [(order[i], *half_card(0, i), half_rot(0), 1.0, 1.0, False) for i in range(lp + 1)]
    right = [(order[26 + i], *half_card(1, i), half_rot(1), 1.0, 1.0, False) for i in range(rp + 1)]
    return pile + left + right + [rec for _, rec in sorted(flight, key=lambda f: f[0])]


def square_up(order, rag, u):
    """The ragged pile tightens into the squared deck; u = 0 ragged, u = 1 squared."""
    u = smooth(u); out = []
    for k, c in enumerate(order):
        px, py = stack_centre(PILE, k, 52); dx, dy, drot = rag[k]; qx, qy = stack_centre(CENTRE, k, 52)
        out.append((c, lerp(px + dx, qx, u), lerp(py + dy, qy, u), drot * (1 - u), 1.0, 1.0, False))
    return out


ORDER0 = initial_order()
SIDES_MAIN, SIDES_LOOP = riffle_sides(101), riffle_sides(202)
RAG_MAIN, RAG_LOOP = ragged(303, SIDES_MAIN), ragged(404, SIDES_LOOP)
ORDER1 = riffled_order(ORDER0, SIDES_MAIN)      # deck order after the main riffle; the loop starts from it
ORDER2 = riffled_order(ORDER1, SIDES_LOOP)


def state_main(t):
    if t < 1: return squared(ORDER0)
    if t < 2: return split(ORDER0, t - 1)
    if t < 5: return riffle(ORDER0, t - 2, MAIN_DT, FLASH_MAIN, SIDES_MAIN, RAG_MAIN)
    if t < 6: return square_up(ORDER1, RAG_MAIN, t - 5)
    return squared(ORDER1)


def state_loop(t):
    if t < .1: return split(ORDER1, 1)
    if t < 2.8: return riffle(ORDER1, t - .1, LOOP_DT, FLASH_LOOP, SIDES_LOOP, RAG_LOOP)
    if t < 3.4: return square_up(ORDER2, RAG_LOOP, (t - 2.8) / .6)
    if t < 3.9: return split(ORDER2, (t - 3.4) / .5)
    return split(ORDER2, 1)


# ---------------------------------------------------------------- SVG serialisation
def art(identity=None, back=False):
    s = studio.SVG(); s.a = []; s.card(identity or 'back', 0, 0, CW, CH, back=back); return ''.join(s.a)


BACK = art(back=True)
FACES = {c: art(c) for c in DECK}
PATTERNS = ('<pattern id="back" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 6L6 0L12 6L6 12Z" fill="none" stroke="#8fa1c5" stroke-width="1"/></pattern>'
            '<pattern id="felt" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M1 2h1M6 7h1" stroke="#ffffff" stroke-opacity=".035"/></pattern>')


def scene_svg(cards, title='Riffle shuffle'):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>{html.escape(title)}</title>',
             f'<defs>{PATTERNS}<g id="cb">{BACK}</g></defs>',
             f'<rect x="0" y="0" width="{W}" height="{H}" fill="{studio.FELT}"/><rect x="0" y="0" width="{W}" height="{H}" fill="url(#felt)"/>']
    for card, cx, cy, rot, sx, sy, face in cards:
        tf = f'translate({cx:.2f} {cy:.2f}) rotate({rot:.2f})' + (f' scale({sx:.3f} {sy:.3f})' if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3 else '') + f' translate({-CW / 2:.0f} {-CH / 2:.0f})'
        parts.append(f'<g transform="{tf}">{FACES[card]}</g>' if face else f'<use xlink:href="#cb" transform="{tf}"/>')
    parts.append('</svg>')
    return ''.join(parts)


def sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p: Path, text: str): p.write_text(text, encoding='utf-8', newline='\n')


def frame_files(state, duration, prefix):
    """One SVG per distinct state at 1/30 s; consecutive identical states share a file. Returns (frames, files)."""
    frames, files, names = [], {}, {}
    for n in range(int(round(duration * FPS))):
        t = n / FPS; svg = scene_svg(state(t)); key = hashlib.sha256(svg.encode()).hexdigest()
        if key not in names:
            name = f'{prefix}-{len(names):04d}.svg'; names[key] = name; files[name] = svg
        name = names[key]
        if not frames or frames[-1]['file'] != name: frames.append({'time': t, 'file': name})
    return frames, files


def build():
    for old in HERE.glob('scene-*.svg'): old.unlink()
    for old in HERE.glob('loop-*.svg'): old.unlink()
    main_frames, main_files = frame_files(state_main, MAIN_DURATION, 'scene')
    loop_frames, loop_files = frame_files(state_loop, LOOP_DURATION, 'loop')
    first, last = loop_frames[0]['file'], loop_frames[-1]['file']
    assert loop_files[first] == loop_files[last], 'loop is not seamless: first and last frames differ'
    for name, svg in list(main_files.items()) + list(loop_files.items()): write(HERE / name, svg)
    poster = scene_svg(squared(ORDER0), 'Riffle shuffle — squared deck'); write(HERE / 'scene.svg', poster)
    write(HERE / 'variant-riffle.svg', scene_svg(state_main(2.5), 'Riffle shuffle — interleave'))
    write(HERE / 'variant-loop.svg', scene_svg(state_loop(1.3), 'Riffle shuffle — loop, mid-interleave'))
    flashes = {'riffle': [launches(ORDER0, SIDES_MAIN)[k][3] for k in FLASH_MAIN], 'loop': [launches(ORDER1, SIDES_LOOP)[k][3] for k in FLASH_LOOP]}
    sources = [
        {'path': '../../../sources/SCRIPT.md', 'lines': [180, 180], 'sha256': sha(ROOT / 'sources/SCRIPT.md'), 'relationship': 'source creative brief'},
        {'path': '../../../review/cut-notes-2026-09-16.md', 'lines': [14, 16], 'sha256': sha(ROOT / 'review/cut-notes-2026-09-16.md'), 'relationship': 'review note (Devin, notes 8 and 10)'},
    ]
    notes = [
        'Stylised top-down riffle: the deck splits, each half releases cards from its top into a centre pile in a deterministic mostly-alternating order (seeded), the ragged pile squares up. Not a physical simulation.',
        f'Faces flash on four drops per riffle ({", ".join(flashes["riffle"])} in the main timeline; {", ".join(flashes["loop"])} in the loop); every card lands face down.',
        'exports/riffle.mp4 is the 0–12 s cut of the main timeline (identical states to preview.mp4). exports/loop.mp4 is a separate 4 s timeline whose first and last authored frames are identical, encoded by src/build_riffle.py encode-loop with the same CairoSVG + ffmpeg recipe as tools/render/render_assets.py.',
        'Card backs and faces are the shared win95-workbench-1.1.0 primitives (tools/render/studio.py card()) at 240 × 336 px.',
    ]
    build_json = {'id': ID, 'duration': MAIN_DURATION, 'frames': main_frames, 'variants': {'riffle': 'variant-riffle.svg', 'loop': 'variant-loop.svg'},
                  'poster': 'scene.svg', 'cuts': {'riffle': [0, MAIN_DURATION]},
                  'loops': {'loop': {'duration': LOOP_DURATION, 'frames': loop_frames, 'output': 'exports/loop.mp4', 'encoder': 'python assets/diagrams/DIA-15/src/build_riffle.py encode-loop'}},
                  'notes': notes, 'sources': sources, 'kind': 'motion'}
    write(HERE / 'build.json', json.dumps(build_json, indent=2, ensure_ascii=False) + '\n')
    beats = ['0–1 s: squared deck.', '1–2 s: split into two tilted halves.', '2–5 s: riffle interleave, cards dropping alternately from both halves; four faces flash.', '5–6 s: the ragged pile squares up.', '6–12 s: hold on the squared deck (poster).']
    timeline = {'id': ID, 'durationSeconds': MAIN_DURATION, 'fps': FPS, 'width': W, 'height': H, 'beats': beats, 'frames': main_frames,
                'cuts': {'riffle': [0, MAIN_DURATION]}, 'variant_names': ['riffle', 'loop'],
                'key_seconds': {'riffle': 2.0, 'loop': 0.1},
                'loops': {'loop': {'durationSeconds': LOOP_DURATION, 'seamless': True,
                                   'beats': ['0–0.1 s: halves apart.', '0.1–2.8 s: riffle interleave; four faces flash.', '2.8–3.4 s: square up.', '3.4–3.9 s: split again.', '3.9–4.0 s: halves apart — identical to frame 0.'],
                                   'frames': loop_frames}},
                'motion_model': 'Per-frame deterministic states (one authored SVG per distinct 1/30 s state) computed from time by src/build_riffle.py; MP4s encode the same states at 30 fps.'}
    write(HERE / 'timeline.json', json.dumps(timeline, indent=2, ensure_ascii=False) + '\n')
    scenes = {**main_files, **loop_files}
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Animated riffle shuffle of a real deck</title>'
            '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style>'
            '<div id="stage" aria-label="Animated riffle shuffle of a real deck"></div><script>'
            f'const timeline={json.dumps(timeline, ensure_ascii=False)};const scenes={json.dumps(scenes, ensure_ascii=False)};'
            "const stage=document.getElementById('stage');function pick(frames,t){let f=frames[0];for(const x of frames){if(x.time<=t)f=x;else break}return f}"
            "window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,"
            "renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));const f=pick(timeline.frames,t);stage.innerHTML=scenes[f.file];return f.file},"
            "variants:{loop:{durationSeconds:timeline.loops.loop.durationSeconds,seamless:true,renderAt(t){const d=timeline.loops.loop.durationSeconds;t=Number.isFinite(t)?((t%d)+d)%d:0;const f=pick(timeline.loops.loop.frames,t);stage.innerHTML=scenes[f.file];return f.file}}}};"
            "__ASSET__.renderAt(0);let start=null,playing=false,mode='main';"
            "document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();mode='main';playing=!playing;start=null;requestAnimationFrame(tick)}"
            "if(e.code==='KeyL'){mode='loop';playing=!playing;start=null;requestAnimationFrame(tick)}"
            "if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});"
            "function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;"
            "if(mode==='loop'){__ASSET__.variants.loop.renderAt(t);requestAnimationFrame(tick);return}"
            "__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script>")
    write(HERE / 'index.html', page)
    print(f'BUILT {ID}: {len(main_files)} main scene files over {len(main_frames)} state changes, {len(loop_files)} loop files; flashes {flashes}')
    print('riffle order (bottom to top):', ' '.join(ORDER1))


def encode_loop():
    """Raster the loop frames and encode exports/loop.mp4 exactly the way render_assets.encode() does."""
    import cairosvg
    from PIL import Image
    data = json.loads((HERE / 'build.json').read_text(encoding='utf-8'))['loops']['loop']
    frames, duration = data['frames'], data['duration']; dst = BASE / data['output']; dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='vb-') as td:
        cache = {}
        for f in frames:
            if f['file'] not in cache:
                p = Path(td) / Path(f['file']).with_suffix('.png').name
                cairosvg.svg2png(url=str(HERE / f['file']), write_to=str(p), output_width=W, output_height=H)
                assert Image.open(p).size == (W, H); cache[f['file']] = p
        n = math.ceil(duration * FPS - 1e-8); runs = []
        for i, frame in enumerate(frames):
            start = math.ceil(frame['time'] * FPS - 1e-8)
            end = min(n, math.ceil(frames[i + 1]['time'] * FPS - 1e-8)) if i + 1 < len(frames) else n
            if end - start > 0: runs.append((cache[frame['file']], (end - start) / FPS))
        concat = dst.with_suffix('.concat.txt'); lines = []
        for p, d in runs: lines.extend([f"file '{p.as_posix()}'", f'duration {d:.9f}'])
        lines.append(f"file '{runs[-1][0].as_posix()}'")
        concat.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat), '-vf', 'fps=30,format=yuv420p', '-frames:v', str(n),
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '2', '-movflags', '+faststart', str(dst)]
        subprocess.run(cmd, check=True); concat.unlink()
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,nb_frames', '-of', 'json', str(dst)], text=True))
    st = info['streams'][0]
    assert st['width'] == W and st['height'] == H and st['r_frame_rate'] == '30/1' and st['pix_fmt'] == 'yuv420p'
    assert abs(float(info['format']['duration']) - duration) < .07
    report = {'renderer': 'CairoSVG ' + cairosvg.__version__, 'png_dimensions': f'{W}x{H}', 'video_probes': [{'file': dst.relative_to(BASE).as_posix(), 'command': ' '.join(cmd), 'probe': info}],
              'seamless': frames[0]['file'] == frames[-1]['file'], 'command': 'python assets/diagrams/DIA-15/src/build_riffle.py encode-loop'}
    write(BASE / 'evidence' / 'loop-encode.json', json.dumps(report, indent=2) + '\n')
    print('ENCODED', dst, info['format']['duration'], 's, seamless =', report['seamless'])


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    {'build': build, 'encode-loop': encode_loop}[cmd]()

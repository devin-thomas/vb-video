#!/usr/bin/env python3
"""DIA-05 revision 2 authoring: the Hand diagram as four beat-accurate cutdowns plus the continuous preview.

Run from the repository root:  python assets/diagrams/DIA-05/src/author.py
Writes scene-NNNN.svg, variant-*.svg, build.json, timeline.json, index.html and brief.json into this folder,
using the shared primitives in tools/render/studio.py (win95-workbench-1.1.0 card faces). Nothing outside
assets/diagrams/DIA-05/ is written. Rendering is a separate step: python assets/diagrams/DIA-05/src/render.py

Layout (1920 x 1080, 120 px safe area): heading; a zoomed row of the first six slots (or, for `cost`, all 26
slots of a full dealt hand); the Count boundary; the 52-slot strip; the active code line; the ticket copy.
Motion is discrete state animation at 15 authored states per second, encoded at 30 fps by the renderer.
"""
from __future__ import annotations
import copy, hashlib, html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools/render'))
from studio import SVG, BG, PANEL, FG, MUTED, LINE, BLUE, GOLD  # noqa: E402

ID = 'DIA-05'
TITLE = 'Arrays as queues'
HAND = ['2S', '5H', '9D', 'KC']
# A full dealt hand (26 cards, DealCards' "26 apiece") for the cost view. The first four are the ticket's cards;
# the other 22 are an authored illustrative fixture, not program output.
FULL_HAND = HAND + ['AS', '7D', 'JH', '3C', '10S', 'QD', '6H', '8C', '4S', 'KH', '9C', '2D', 'JS', '5C', '10H', 'AD',
                    '7S', 'QC', '3H', '8D', '6S', 'JC']
assert len(FULL_HAND) == 26 and len(set(FULL_HAND)) == 26

# Zoom row: six slots, cards at the shared 144 x 202 proportion.
ZX0, ZP, ZW, ZH, ZY = 360, 240, 200, 212, 300
ZCW, ZCH, ZCX, ZCY = 128, 180, 36, 16
TOP_X, TOP_Y = 150, 316                      # the "Top" card area left of slot 0
C_X, C_Y = ZX0 + 4 * ZP + ZCX, 112           # the incoming card C above slot 4
# Wide row: 26 slots across the safe width; cards 56 px wide (rank-and-pips face style).
WX0, WP, WW, WH, WY = 128, 64, 62, 99, 330
WCW, WCH, WCX, WCY = 56, 79, 3, 10
LIFT_Y = 220                                 # where the drawn card rests in the wide view
GHOST = 0.3                                  # opacity of a copied-from (stale) slot value
TWEEN_FPS = 15


def ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def geom(mode: str):
    if mode == 'zoom':
        return dict(x0=ZX0, p=ZP, w=ZW, h=ZH, y=ZY, cw=ZCW, ch=ZCH, cx=ZCX, cy=ZCY, n=6, lab_y=ZY + ZH + 44, lab=34)
    return dict(x0=WX0, p=WP, w=WW, h=WH, y=WY, cw=WCW, ch=WCH, cx=WCX, cy=WCY, n=26, lab_y=WY + WH + 30, lab=20)


def slot_card_xy(mode: str, i: int):
    g = geom(mode)
    return g['x0'] + i * g['p'] + g['cx'], g['y'] + g['cy']


def draw(st: dict) -> str:
    """One deterministic SVG state. `st` is a plain dict so every frame is an independent, seekable picture."""
    g = geom(st['mode']); count = st['count']
    s = SVG(BG, TITLE); s.heading(TITLE, st.get('sub'))
    # Top area (draw states only)
    if st.get('top') in ('outline', 'card') and st['mode'] == 'zoom':
        s.raw(f'<rect x="{TOP_X}" y="{TOP_Y}" width="{ZCW}" height="{ZCH}" rx="7" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="8 6"/>')
        s.text('Top', TOP_X + ZCW / 2, 300, 26, MUTED, anchor='middle')
    # Slots with their resident values; the value keeps the slot's live/inactive stroke from Count, not from itself.
    for i in range(g['n']):
        x = g['x0'] + i * g['p']; live = i < count
        s.rect(x, g['y'], g['w'], g['h'], PANEL, BLUE if live else LINE, 2)
        s.text(str(i), x + g['w'] / 2, g['lab_y'], g['lab'], MUTED, mono=True, anchor='middle')
        slot = st['slots'][i] if i < len(st['slots']) else None
        if slot and slot.get('card'):
            s.card(slot['card'], x + g['cx'], g['y'] + g['cy'], g['cw'], g['ch'], opacity=slot.get('opacity', 1))
        if slot and slot.get('label'):
            s.text(slot['label'], x + g['w'] / 2, g['lab_y'] + (34 if st['mode'] == 'zoom' else 26), 24 if st['mode'] == 'zoom' else 18, MUTED, anchor='middle')
    # Moving or parked cards, drawn above the slots.
    for c in st.get('float', []):
        s.card(c['card'], c['x'], c['y'], c['w'], c['h'], opacity=c.get('opacity', 1), accent=c.get('accent'))
    for t in st.get('labels', []):
        s.text(t['text'], t['x'], t['y'], t.get('size', 26), t.get('fill', MUTED), mono=t.get('mono', False), anchor=t.get('anchor', 'start'))
    # Count: an integer marking the live boundary (a line between slots), not a pointer to a card.
    b = st.get('boundary', count); bx = g['x0'] + b * g['p'] - (g['p'] - g['w']) / 2
    s.line(bx, g['y'] - 16, bx, g['lab_y'] + 14, GOLD, 3)
    if bx > 1560:
        s.text(f'Count = {count}', bx + 6, g['lab_y'] + 84, 40, GOLD, mono=True, anchor='end')
        s.text('live boundary', bx + 6, g['lab_y'] + 118, 26, GOLD, anchor='end')
    else:
        s.text(f'Count = {count}', bx, g['lab_y'] + 84, 40, GOLD, mono=True, anchor='middle')
        s.text('live boundary', bx, g['lab_y'] + 118, 26, GOLD, anchor='middle')
    # The whole array: 52 slots, Count of them live.
    shown = g['n'] - 1
    s.text(f'slots 0–{shown} shown above', 120, 712, 22, MUTED)
    s.line(120, 722, 120 + shown * 32 + 25, 722, LINE, 2)
    s.text('Capacity: 52', 1800, 712, 28, FG, True, anchor='end')
    live_cells = st['strip_live']
    for i in range(52):
        s.rect(120 + i * 32, 730, 25, 60, BLUE if i < live_cells else PANEL, BLUE if i < live_cells else LINE, 2)
    for i in (0, 51):
        s.text(str(i), 120 + i * 32 + 12.5, 822, 22, MUTED, mono=True, anchor='middle')
    sb = st.get('strip_boundary', live_cells); sx = 120 + sb * 32 - 3.5
    s.line(sx, 720, sx, 800, GOLD, 3)
    # Active code line(s): exact Program.vb text, shown as the state's annotation.
    lines = st.get('code', [])
    if len(lines) == 1:
        s.text(lines[0], 120, 890, 37, GOLD, mono=True)
    elif len(lines) == 2:
        s.text(lines[0], 120, 868, 34, GOLD, mono=True); s.text(lines[1], 120, 912, 34, GOLD, mono=True)
    if st.get('note'):
        s.text(st['note'], 1800, 890, 37, GOLD, mono=True, anchor='end')
    # Ticket copy.
    s.text('Cards(0): next to draw', 120, 955, 30, FG)
    s.text('Live: 0 … Count − 1', 760, 955, 30, FG)
    s.text('Inactive: Count … 51', 1330, 955, 30, MUTED)
    return s.finish()


def base_state(mode: str, cards: list, count: int, **kw) -> dict:
    n = geom(mode)['n']
    st = {'mode': mode, 'sub': 'The first six of 52 slots' if mode == 'zoom' else 'A full dealt hand: 26 cards',
          'count': count, 'boundary': count, 'strip_live': count,
          'slots': [{'card': cards[i] if i < len(cards) else None} for i in range(n)], 'float': [], 'labels': [], 'code': []}
    st.update(kw); return st


class Cut:
    """A named cutdown: (time, state) keyframes; the last state holds to `duration`."""
    def __init__(self, name, duration, key_second, key_moment, serves):
        self.name, self.duration, self.key_second, self.key_moment, self.serves = name, duration, key_second, key_moment, serves
        self.frames: list[tuple[float, dict]] = []; self.action_end = 0.0

    def at(self, t, st):
        self.frames.append((round(t, 6), copy.deepcopy(st))); self.action_end = max(self.action_end, t)

    def tween(self, t0, dur, fn):
        n = max(1, round(dur * TWEEN_FPS))
        for k in range(n + 1):
            self.at(t0 + k * dur / n, fn(ease(k / n)))
        return t0 + dur


def build_live_slots() -> Cut:
    c = Cut('live-slots', 18, 0.0, 'the array at rest, Count = 4 marking the live boundary',
            ['S08-B01', 'S08-B04'])
    c.at(0, base_state('zoom', HAND, 4, code=['Dim Cards() As Card', 'Dim Count As Integer']))
    return c


def build_append() -> Cut:
    c = Cut('append', 12, 1.0, 'the card C lands in slot 4 (position Count)', ['S08-B05'])
    st = base_state('zoom', HAND, 4, code=['H.Cards(H.Count) = C'])
    st['float'] = [{'card': 'AS', 'x': C_X, 'y': C_Y, 'w': ZCW, 'h': ZCH}]
    st['labels'] = [{'text': 'C', 'x': C_X - 16, 'y': 210, 'size': 34, 'mono': True, 'anchor': 'end'}]
    c.at(0, st)
    tx, ty = slot_card_xy('zoom', 4)

    def drop(u):
        f = copy.deepcopy(st); f['float'][0]['y'] = lerp(C_Y, ty, u); f['float'][0]['x'] = lerp(C_X, tx, u); return f
    t = c.tween(0.4, 0.6, drop)
    landed = base_state('zoom', HAND + ['AS'], 4, code=['H.Cards(H.Count) = C'])
    c.at(t, landed)
    inc = copy.deepcopy(landed); inc['code'] = ['H.Count = H.Count + 1']

    def grow(u):
        f = copy.deepcopy(inc); f['boundary'] = lerp(4, 5, u); f['strip_boundary'] = lerp(4, 5, u); return f
    t = c.tween(1.7, 0.6, grow)
    c.at(t, base_state('zoom', HAND + ['AS'], 5, code=['H.Count = H.Count + 1']))
    return c


def build_draw_shift() -> Cut:
    c = Cut('draw-shift', 12, 1.2, 'the first shift movement: H.Cards(0) = H.Cards(1)', ['S08-B06', 'S08-B07'])
    cards = HAND + ['AS']
    st = base_state('zoom', cards, 5, code=['Top = H.Cards(0)'], top='outline')
    c.at(0, st)
    sx, sy = slot_card_xy('zoom', 0)
    lifted = copy.deepcopy(st); lifted['slots'][0]['opacity'] = GHOST

    def take(u):
        f = copy.deepcopy(lifted); f['float'] = [{'card': '2S', 'x': lerp(sx, TOP_X, u), 'y': sy, 'w': ZCW, 'h': ZCH}]; return f
    t = c.tween(0.3, 0.6, take)
    cur = copy.deepcopy(lifted); cur['float'] = [{'card': '2S', 'x': TOP_X, 'y': TOP_Y, 'w': ZCW, 'h': ZCH}]; cur['top'] = 'card'
    c.at(t, cur)
    t = 1.2
    for i in range(1, 5):
        moving = cur['slots'][i]['card']; fx, fy = slot_card_xy('zoom', i); tx, _ = slot_card_xy('zoom', i - 1)
        before = copy.deepcopy(cur); before['code'] = [f'H.Cards({i - 1}) = H.Cards({i})']
        before['slots'][i]['opacity'] = GHOST

        def shift(u, before=before, moving=moving, fx=fx, fy=fy, tx=tx):
            f = copy.deepcopy(before); f['float'] = before['float'] + [{'card': moving, 'x': lerp(fx, tx, u), 'y': fy, 'w': ZCW, 'h': ZCH}]; return f
        t = c.tween(t, 0.5, shift)
        cur = copy.deepcopy(before); cur['slots'][i - 1] = {'card': moving}
        c.at(t, cur); t += 0.2
    dec = copy.deepcopy(cur); dec['code'] = ['H.Count = H.Count - 1']

    def shrink(u):
        f = copy.deepcopy(dec); f['boundary'] = lerp(5, 4, u); f['strip_boundary'] = lerp(5, 4, u); return f
    t = c.tween(t + 0.1, 0.5, shrink)
    end = copy.deepcopy(dec); end.update(count=4, boundary=4, strip_live=4); end.pop('strip_boundary', None)
    end['slots'][4]['label'] = 'stale'
    c.at(t, end)
    ret = copy.deepcopy(end); ret['code'] = ['DrawTopCard = Top']; ret['float'][0]['accent'] = GOLD
    c.at(t + 0.8, ret)
    return c


def build_cost() -> Cut:
    c = Cut('cost', 20, 1.2, 'every remaining card starts moving one slot forward at once', ['S08-B07', 'S08-B08'])
    st = base_state('wide', FULL_HAND, 26, code=['Top = H.Cards(0)'])
    c.at(0, st)
    sx, sy = slot_card_xy('wide', 0)
    lifted = copy.deepcopy(st); lifted['slots'][0]['opacity'] = GHOST

    def take(u):
        f = copy.deepcopy(lifted); f['float'] = [{'card': '2S', 'x': sx, 'y': lerp(sy, LIFT_Y, u), 'w': WCW, 'h': WCH}]; return f
    t = c.tween(0.4, 0.5, take)
    cur = copy.deepcopy(lifted); cur['float'] = [{'card': '2S', 'x': sx, 'y': LIFT_Y, 'w': WCW, 'h': WCH}]
    cur['labels'] = [{'text': 'Top', 'x': sx + WCW + 12, 'y': LIFT_Y + 42, 'size': 26}]
    cur['code'] = ['For i = 1 To H.Count - 1', '    H.Cards(i - 1) = H.Cards(i)']
    c.at(t, cur)
    before = copy.deepcopy(cur); before['note'] = 'O(n): 25 moves for 26 cards'
    for i in range(1, 26):
        before['slots'][i]['opacity'] = GHOST

    def slide(u):
        f = copy.deepcopy(before)
        for i in range(1, 26):
            fx, fy = slot_card_xy('wide', i)
            f['float'].append({'card': cur['slots'][i]['card'], 'x': fx - u * WP, 'y': fy, 'w': WCW, 'h': WCH})
        return f
    t = c.tween(1.2, 0.8, slide)
    after = copy.deepcopy(before)
    for i in range(25):
        after['slots'][i] = {'card': cur['slots'][i + 1]['card']}
    c.at(t, after)
    dec = copy.deepcopy(after); dec['code'] = ['H.Count = H.Count - 1']

    def shrink(u):
        f = copy.deepcopy(dec); f['boundary'] = lerp(26, 25, u); f['strip_boundary'] = lerp(26, 25, u); return f
    t = c.tween(2.3, 0.5, shrink)
    end = copy.deepcopy(dec); end.update(count=25, boundary=25, strip_live=25); end.pop('strip_boundary', None)
    end['slots'][25]['label'] = 'stale'
    c.at(t, end)
    return c


def main():
    cuts = [build_live_slots(), build_append(), build_draw_shift(), build_cost()]
    preview_hold = {'live-slots': 4.0, 'append': 2.2, 'draw-shift': 2.6, 'cost': 3.2}
    files: dict[str, str] = {}; svg_cache: dict[str, str] = {}

    def file_for(st: dict) -> str:
        key = json.dumps(st, sort_keys=True)
        if key not in svg_cache:
            svg_cache[key] = draw(st)
        svg = svg_cache[key]
        if svg not in files:
            files[svg] = f'scene-{len(files):04d}.svg'
        return files[svg]

    for old in list(HERE.glob('scene-*.svg')) + list(HERE.glob('variant-*.svg')):
        old.unlink()
    preview_frames = []; cutdowns = {}; offset = 0.0; beats = []
    for cut in cuts:
        frames = [{'time': t, 'file': file_for(st)} for t, st in cut.frames]
        # Drop consecutive duplicates so every frame record is a real state change.
        dedup = [f for i, f in enumerate(frames) if i == 0 or f['file'] != frames[i - 1]['file']]
        cutdowns[cut.name] = {'file': f'exports/{cut.name}.mp4', 'duration': cut.duration, 'key_second': cut.key_second,
                              'key_moment': cut.key_moment, 'serves': cut.serves, 'action_end': round(cut.action_end, 3),
                              'frames': dedup}
        for f in dedup:
            preview_frames.append({'time': round(offset + f['time'], 6), 'file': f['file']})
        seg_len = cut.action_end + preview_hold[cut.name]
        beats.append(f'{offset:g}–{offset + seg_len:g} s: {cut.name} — {cut.key_moment}; holds {preview_hold[cut.name]:g} s.')
        offset += seg_len
    duration = round(offset, 3)
    for svg, name in files.items():
        (HERE / name).write_text(svg, encoding='utf-8', newline='\n')
    hold_svg = {cut.name: svg_cache[json.dumps(cut.frames[-1][1], sort_keys=True)] for cut in cuts}
    variants = {'live-slots': 'live-slots', 'append': 'append', 'draw-shift': 'draw-shift', 'cost': 'cost',
                # Legacy names still required by manifest.json: the same hold states under the revision-1 names.
                '52-slot-overview': 'live-slots', 'draw-and-shift': 'draw-shift', 'append-at-count': 'append'}
    variant_files = {}
    for name, src in variants.items():
        fn = f'variant-{name}.svg'; (HERE / fn).write_text(hold_svg[src], encoding='utf-8', newline='\n'); variant_files[name] = fn

    def source(rel, lines, rel_type):
        return {'path': f'../../../sources/{rel}', 'lines': lines, 'sha256': hashlib.sha256((ROOT / 'sources' / rel).read_bytes()).hexdigest(), 'relationship': rel_type}
    sources = [source('ASSET_PLAN.md', [20, 20], 'source creative brief'), source('SCRIPT.md', [315, 360], 'source creative brief'),
               source('Program.vb', [23, 26], 'literal excerpt'), source('Program.vb', [128, 167], 'literal excerpt')]
    notes = [
        'Revision 2: four independent cutdowns (live-slots, append, draw-shift, cost), each starting at its named moment and holding its end state; key_second is the second of the key moment inside that cutdown.',
        'Narration order is append (S08-B05) before draw (S08-B06/B07), so the append drops A♠ at index Count = 4 and Count becomes 5; the draw then copies 5♥→0, 9♦→1, K♣→2, A♠→3 in increasing i order and Count becomes 4. The revision-1 indices (draw first, append at 3) assumed the reverse order.',
        'Copy semantics are shown literally: a copied-from slot keeps a faded duplicate until it is overwritten; the last one is stale storage beyond Count, never presented as a live card. Count is drawn as a boundary line between slots, not as a pointer to a card.',
        'The cost view uses a full dealt hand of 26 cards (DealCards deals 26 apiece); the first four are the ticket cards and the other 22 are an authored illustrative fixture, not program output.',
    ]
    build = {'id': ID, 'duration': duration, 'frames': preview_frames, 'variants': variant_files, 'poster': 'variant-live-slots.svg', 'cuts': {},
             'cutdowns': cutdowns, 'notes': notes, 'sources': sources, 'kind': 'motion',
             'render': 'python assets/diagrams/DIA-05/src/render.py (render_assets.render for preview/poster/stills, then the same encode() for each cutdown)'}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    timeline = {'id': ID, 'durationSeconds': duration, 'fps': 30, 'width': 1920, 'height': 1080, 'revision': 2, 'beats': beats,
                'frames': preview_frames, 'cuts': {},
                'cutdowns': {n: {k: v for k, v in c.items()} for n, c in cutdowns.items()},
                'variant_names': list(variant_files), 'authored_state_rate': TWEEN_FPS,
                'motion_model': 'Explicit deterministic step states (15 authored states per second during motion, readable holds); MP4 encodes the same scene changes at 30 fps. Each cutdown is an independent timeline that starts at its named moment and holds its end state.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    scenes = {name: svg for svg, name in files.items()}
    title = 'Array as queue: live slots, draw, shift, append'
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>html,body{{margin:0;background:#000;height:100%;overflow:hidden}}#stage{{width:100%;height:100%;display:flex;align-items:center;justify-content:center}}svg{{width:100%;height:100%;object-fit:contain}}</style>'
            f'<div id="stage" aria-label="{html.escape(title)}"></div><script>const timeline={json.dumps(timeline, ensure_ascii=False)};const scenes={json.dumps(scenes, ensure_ascii=False)};'
            "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")
    (HERE / 'index.html').write_text(page, encoding='utf-8', newline='\n')
    brief = json.loads((HERE / 'brief.json').read_text(encoding='utf-8'))
    brief['revision'] = 2; brief['beats'] = beats
    brief['cutdowns'] = {n: {'duration_seconds': c['duration'], 'key_second': c['key_second'], 'key_moment': c['key_moment'], 'serves': c['serves']} for n, c in cutdowns.items()}
    (HERE / 'brief.json').write_text(json.dumps(brief, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(f'{ID}: {len(files)} scene files, preview {duration} s, cutdowns ' + ', '.join(f"{n} {c['duration']} s key {c['key_second']} s ({len(c['frames'])} states)" for n, c in cutdowns.items()))


if __name__ == '__main__':
    main()

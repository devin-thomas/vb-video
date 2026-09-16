"""Render the OPS-04 review deck page from deck-data.json."""
import json
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE / "deck-data.json").read_text(encoding="utf-8"))
SECTION_TITLES = {
    1: "Cold open", 2: "A very brief history of BASIC to Visual Basic", 3: "The toolchain: what you actually installed",
    4: "How we're doing this today", 5: "The card game War: rules in 60 seconds", 6: "Modeling a card in VB",
    7: "Building and shuffling the deck", 8: "The player's hand: arrays as queues", 9: "The game loop",
    10: "War! The recursion within the loop", 11: "Running it: full simulation", 12: "When the cards run out",
    13: "What this code would have become", 14: "VB vs. the competition in 1995", 15: "What if you were on a Mac?",
    16: "Why VB mattered (and why it died)", 17: "Outro", 0: "Whole video and shared systems",
}
for s in data["sections"]:
    s["title"] = SECTION_TITLES.get(s["n"], s["title"])
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

html = r"""<title>VB War Review Deck</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root {
  --blue: #1B4B8A; --amber: #D4952A; --amber-dim: #B07D22; --green: #2D7D46; --green-bg: #e8f3ec; --red: #C45D3E; --red-bg: #fceae5;
  --surface: #F0EDE8; --surface-raised: #FFFFFF; --surface-sunken: #E4E0D9;
  --text: #1E1D1A; --text-mid: #5C584E; --text-dim: #8B8578; --border: #D5D0C8; --focus: #2A6BC4;
  --font-mono: 'IBM Plex Mono', 'Consolas', monospace; --font-sans: 'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --blue: #5B9FE8; --amber: #E8B44A; --amber-dim: #C9982E; --green: #5DBF78; --green-bg: #1a2e20; --red: #E87A5E; --red-bg: #2e1a15;
  --surface: #1A1917; --surface-raised: #252420; --surface-sunken: #131210;
  --text: #E8E5DF; --text-mid: #A9A49A; --text-dim: #767068; --border: #3A3832; --focus: #7BB8F5; } }
:root[data-theme="dark"] {
  --blue: #5B9FE8; --amber: #E8B44A; --amber-dim: #C9982E; --green: #5DBF78; --green-bg: #1a2e20; --red: #E87A5E; --red-bg: #2e1a15;
  --surface: #1A1917; --surface-raised: #252420; --surface-sunken: #131210;
  --text: #E8E5DF; --text-mid: #A9A49A; --text-dim: #767068; --border: #3A3832; --focus: #7BB8F5; }
* { box-sizing: border-box; }
body { background: var(--surface); color: var(--text); font-family: var(--font-sans); margin: 0; padding-block: 0 4rem; padding-inline: 1.25rem; line-height: 1.45; font-size: 14px; }
.wrap { max-width: 1040px; margin: 0 auto; }
.top { position: sticky; top: 0; z-index: 5; background: var(--surface); border-bottom: 1px solid var(--border); padding-block: 0.8rem 0.6rem; margin-inline: -1.25rem; padding-inline: 1.25rem; }
.top-inner { max-width: 1040px; margin: 0 auto; display: flex; flex-wrap: wrap; align-items: center; gap: 0.6rem 1.25rem; }
h1 { font-family: var(--font-mono); font-size: 1rem; font-weight: 600; margin: 0; }
.prog { display: flex; align-items: center; gap: 0.6rem; font-size: 0.8rem; color: var(--text-mid); }
.prog b { font-family: var(--font-mono); color: var(--text); font-variant-numeric: tabular-nums; }
.bar { width: 160px; height: 6px; background: var(--surface-sunken); border-radius: 3px; overflow: hidden; }
.bar i { display: block; height: 100%; background: var(--green); width: 0; transition: width .2s; }
.chips { display: flex; gap: 0.35rem; flex-wrap: wrap; }
.chip { font-family: var(--font-mono); font-size: 0.68rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; border: 1px solid var(--border); background: var(--surface-raised); color: var(--text-mid); border-radius: 999px; padding: 0.25rem 0.65rem; cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--blue); border-color: var(--blue); color: #fff; }
.chip:focus-visible, button:focus-visible, textarea:focus-visible, select:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
select { font: inherit; font-size: 0.8rem; color: var(--text); background: var(--surface-raised); border: 1px solid var(--border); border-radius: 4px; padding: 0.3rem 0.5rem; }
.save-state { font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); }
.save-state.warn { color: var(--amber-dim); }
.intro { font-size: 0.86rem; color: var(--text-mid); max-width: 70ch; margin: 1.25rem 0 0; }
.intro b { color: var(--text); font-weight: 600; }
section.sec { margin-top: 2.25rem; }
.sec-head { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; flex-wrap: wrap; border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; margin-bottom: 0.9rem; }
.sec-head h2 { font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--text-dim); margin: 0; }
.sec-head h2 b { color: var(--text); }
.sec-meta { font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); }
.sec-approve { font: inherit; font-size: 0.72rem; font-family: var(--font-mono); font-weight: 600; color: var(--green); background: var(--green-bg); border: 1px solid transparent; border-radius: 4px; padding: 0.25rem 0.6rem; cursor: pointer; }
.asset { display: grid; grid-template-columns: 300px 1fr; gap: 1rem; background: var(--surface-raised); border: 1px solid var(--border); border-radius: 6px; padding: 0.9rem; margin-bottom: 0.75rem; border-left-width: 4px; }
.asset[data-state="approved"] { border-left-color: var(--green); }
.asset[data-state="changes"] { border-left-color: var(--red); }
.asset[data-state="undecided"] { border-left-color: var(--amber); }
.asset.hidden { display: none; }
.thumb { background: #000; border-radius: 4px; overflow: hidden; aspect-ratio: 16 / 9; max-width: 100%; }
.thumb img { display: block; width: 100%; height: 100%; object-fit: contain; }
.thumb.none { display: flex; align-items: center; justify-content: center; color: var(--text-dim); font-family: var(--font-mono); font-size: 0.7rem; background: var(--surface-sunken); }
.meta { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-dim); margin-top: 0.4rem; line-height: 1.5; }
.meta span + span::before { content: " · "; }
.head { display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; }
.tid { font-family: var(--font-mono); font-size: 0.78rem; font-weight: 600; color: var(--blue); }
.ttl { font-weight: 600; font-size: 0.95rem; }
.pill { font-family: var(--font-mono); font-size: 0.62rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; padding: 0.1rem 0.45rem; border-radius: 3px; margin-left: auto; white-space: nowrap; }
.pill.approved { background: var(--green-bg); color: var(--green); }
.pill.changes { background: var(--red-bg); color: var(--red); }
.pill.undecided { background: color-mix(in srgb, var(--amber) 15%, transparent); color: var(--amber-dim); }
.pill.repo { background: var(--surface-sunken); color: var(--text-mid); }
.claim { font-size: 0.83rem; color: var(--text-mid); margin: 0.35rem 0 0; }
.copy { font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-mid); background: var(--surface-sunken); border-radius: 4px; padding: 0.4rem 0.6rem; margin-top: 0.45rem; white-space: pre-wrap; max-height: 6.5em; overflow: hidden; }
.gates { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.55rem; }
.gate { font-family: var(--font-mono); font-size: 0.66rem; font-weight: 600; border-radius: 3px; padding: 0.12rem 0.45rem; border: 1px solid var(--border); color: var(--text-mid); cursor: help; }
.gate.blocked, .gate.open { border-color: color-mix(in srgb, var(--amber) 50%, var(--border)); color: var(--amber-dim); }
.gate.approved { border-color: color-mix(in srgb, var(--green) 50%, var(--border)); color: var(--green); }
details { margin-top: 0.5rem; }
summary { font-size: 0.76rem; color: var(--text-mid); cursor: pointer; font-family: var(--font-mono); }
.qs { margin: 0.35rem 0 0; padding-left: 1.1rem; font-size: 0.8rem; color: var(--text-mid); display: grid; gap: 0.3rem; }
.qs li.res { color: var(--text-dim); }
.qs li.res::after { content: " (resolved)"; font-family: var(--font-mono); font-size: 0.68rem; }
.qs .gtag { font-family: var(--font-mono); font-size: 0.66rem; color: var(--text-dim); margin-right: 0.3rem; }
.ev { font-size: 0.76rem; color: var(--text-mid); margin: 0.3rem 0 0; }
.ev b { font-family: var(--font-mono); color: var(--text); font-weight: 600; }
.decide { display: grid; grid-template-columns: auto auto 1fr; gap: 0.5rem; align-items: start; margin-top: 0.75rem; }
.btn { font: inherit; font-size: 0.78rem; font-weight: 600; border-radius: 4px; padding: 0.4rem 0.8rem; cursor: pointer; border: 1px solid var(--border); background: var(--surface-raised); color: var(--text); }
.btn.ok { border-color: var(--green); color: var(--green); }
.btn.ok[aria-pressed="true"] { background: var(--green); color: #fff; }
.btn.bad { border-color: var(--red); color: var(--red); }
.btn.bad[aria-pressed="true"] { background: var(--red); color: #fff; }
textarea { font: inherit; font-size: 0.8rem; color: var(--text); background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 0.4rem 0.55rem; min-height: 2.4rem; resize: vertical; width: 100%; }
.saved { grid-column: 1 / -1; font-family: var(--font-mono); font-size: 0.68rem; color: var(--text-dim); min-height: 1em; }
.empty { font-size: 0.85rem; color: var(--text-dim); padding: 2rem 0; text-align: center; }
@media (max-width: 720px) { .asset { grid-template-columns: 1fr; } .decide { grid-template-columns: 1fr 1fr; } textarea { grid-column: 1 / -1; } }
@media (prefers-reduced-motion: reduce) { .bar i { transition: none; } }
</style>

<div class="top"><div class="top-inner">
  <h1>VB War — Review Deck</h1>
  <div class="prog"><b id="p-num">0</b><span>of <b id="p-total">0</b> decided</span><div class="bar"><i id="p-bar"></i></div></div>
  <div class="chips" role="group" aria-label="Filter">
    <button class="chip" data-f="undecided" aria-pressed="true">Needs decision</button>
    <button class="chip" data-f="all" aria-pressed="false">All</button>
    <button class="chip" data-f="approved" aria-pressed="false">Approved</button>
    <button class="chip" data-f="changes" aria-pressed="false">Needs changes</button>
  </div>
  <label class="save-state"><span class="sr" hidden>Jump to section</span><select id="jump" aria-label="Jump to section"><option value="">Jump to section…</option></select></label>
  <span class="save-state" id="save-state">connecting…</span>
</div></div>

<div class="wrap">
<p class="intro"><b>Every produced asset, in script order.</b> Each card shows what the asset claims, the editorial gates it carries with the worker's finding, and the questions evidence could not settle. Mark each <b>Approve</b> or <b>Needs changes</b> with a note; answers save as you go and the producer reads them back to apply the result. Assets already approved in the repo are pre-marked and can still be changed. Gate-free assets need only your look.</p>
<div id="deck"></div>
<p class="empty" id="empty" hidden>Nothing matches this filter.</p>
</div>

<script id="deck-data" type="application/json">__DATA__</script>
<script>
(function () {
  const data = JSON.parse(document.getElementById('deck-data').textContent);
  const assets = data.assets;
  const byId = Object.fromEntries(assets.map(a => [a.id, a]));
  const decisions = {};  // id -> {decision, note, at}
  let db = null, filter = 'undecided';
  const $ = (s, el) => (el || document).querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  function stateOf(a) {
    const d = decisions[a.id];
    if (d && d.decision) return d.decision;           // 'approved' | 'changes'
    return a.release === 'approved' ? 'approved' : 'undecided';
  }
  function gateTitle(g) { return g.title ? `${g.id}: ${g.title}` : g.id; }

  function card(a) {
    const st = stateOf(a); const d = decisions[a.id] || {};
    const repoApproved = a.release === 'approved' && !(d.decision);
    const pill = repoApproved ? `<span class="pill repo">approved in repo${a.reviewer ? ' · ' + esc(a.reviewer) : ''}</span>`
      : `<span class="pill ${st}">${st === 'changes' ? 'needs changes' : st}</span>`;
    const gates = a.gates.map(g => `<span class="gate ${esc(g.status)}" title="${esc(gateTitle(g))} — ${esc(g.status)}${g.reason ? ': ' + esc(g.reason) : ''}${g.approver ? ' (approver: ' + esc(g.approver) + ')' : ''}">${esc(g.id)} ${esc(g.status)}</span>`).join('');
    const qs = a.questions.length ? `<details ${a.open_questions ? 'open' : ''}><summary>${a.open_questions} open question${a.open_questions === 1 ? '' : 's'}${a.questions.length > a.open_questions ? ` · ${a.questions.length - a.open_questions} resolved` : ''}</summary><ul class="qs">${a.questions.map(q => `<li class="${q.status === 'open' ? '' : 'res'}">${q.gate ? `<span class="gtag">${esc(q.gate)}</span>` : ''}${esc(q.question)}${q.resolution && q.resolution.decision ? ` <em>— ${esc(q.resolution.resolved_by || '')}: ${esc(q.resolution.decision)}</em>` : ''}</li>`).join('')}</ul></details>` : '';
    const findings = a.gates.filter(g => g.reason && g.status !== 'approved').map(g => `<p class="ev"><b>${esc(g.id)}</b> ${esc(g.reason)}</p>`).join('');
    const meta = [a.kind, a.duration ? `${a.duration}s` : null, a.dimensions && a.dimensions.width ? `${a.dimensions.width}×${a.dimensions.height}` : null,
      a.variants.length ? `${a.variants.length} variant${a.variants.length > 1 ? 's' : ''}: ${a.variants.map(v => v.name || v).slice(0, 4).join(', ')}` : null,
      a.cues.length ? `script line${a.cues.length > 1 ? 's' : ''} ${a.cues.join(', ')}` : null, a.issue ? `#${a.issue}` : null].filter(Boolean).map(x => `<span>${esc(x)}</span>`).join('');
    const credits = a.credits.length ? `<p class="ev"><b>credit</b> ${esc(a.credits.map(c => typeof c === 'string' ? c : (c.credit || c.text || JSON.stringify(c))).join(' · '))}</p>` : '';
    return `<article class="asset" id="a-${a.id}" data-id="${a.id}" data-state="${st}">
      <div><div class="thumb ${a.thumb ? '' : 'none'}">${a.thumb ? `<img src="${a.thumb}" alt="${esc(a.title)}" loading="lazy">` : 'no image (coordination ticket)'}</div><div class="meta">${meta}</div></div>
      <div>
        <div class="head"><span class="tid">${esc(a.id)}</span><span class="ttl">${esc(a.title)}</span>${pill}</div>
        <p class="claim">${esc(a.brief)}</p>
        ${a.copy ? `<div class="copy">${esc(a.copy)}</div>` : ''}
        ${a.provenance ? `<p class="ev"><b>provenance</b> ${esc(a.provenance)}</p>` : ''}
        ${credits}
        <div class="gates">${gates || '<span class="gate approved">no editorial gate</span>'}</div>
        ${findings}
        ${qs}
        <div class="decide">
          <button class="btn ok" data-d="approved" aria-pressed="${st === 'approved'}">Approve</button>
          <button class="btn bad" data-d="changes" aria-pressed="${st === 'changes'}">Needs changes</button>
          <textarea id="note-${a.id}" placeholder="Note (required for Needs changes)">${esc(d.note || '')}</textarea>
          <div class="saved" id="saved-${a.id}">${d.at ? 'saved ' + esc(d.at) : ''}</div>
        </div>
      </div></article>`;
  }

  function render() {
    const deck = $('#deck'); deck.innerHTML = '';
    const jump = $('#jump'); jump.innerHTML = '<option value="">Jump to section…</option>';
    let shown = 0;
    for (const s of data.sections) {
      const list = assets.filter(a => a.section === s.n);
      if (!list.length) continue;
      const vis = list.filter(a => filter === 'all' || stateOf(a) === filter);
      if (!vis.length) continue;
      shown += vis.length;
      const undecided = list.filter(a => stateOf(a) === 'undecided').length;
      const sec = document.createElement('section'); sec.className = 'sec'; sec.id = 'sec-' + s.n;
      sec.innerHTML = `<div class="sec-head"><h2>${s.n ? `Section ${s.n} · ` : ''}<b>${esc(s.title)}</b></h2><span class="sec-meta">${list.length} asset${list.length > 1 ? 's' : ''} · ${undecided} undecided</span>${undecided ? `<button class="sec-approve" data-sec="${s.n}">Approve all ${undecided} undecided here</button>` : ''}</div>` + vis.map(card).join('');
      deck.appendChild(sec);
      jump.insertAdjacentHTML('beforeend', `<option value="sec-${s.n}">${s.n ? s.n + ' · ' : ''}${esc(s.title)}</option>`);
    }
    $('#empty').hidden = shown > 0;
    const decided = assets.filter(a => stateOf(a) !== 'undecided').length;
    $('#p-num').textContent = decided; $('#p-total').textContent = assets.length;
    $('#p-bar').style.width = (100 * decided / assets.length) + '%';
  }

  async function save(id, decision, note) {
    const rec = { decision, note: note || '', at: new Date().toISOString().slice(0, 16).replace('T', ' '), by: 'Devin', release_before: byId[id].release };
    decisions[id] = rec;
    const el = $('#saved-' + id); if (el) el.textContent = 'saving…';
    if (!db) { if (el) el.textContent = 'not saved: no database in this view — tell the producer in chat'; return; }
    try { await db.doc('reviews/' + id).set(rec); if (el) el.textContent = 'saved ' + rec.at; }
    catch (e) { if (el) el.textContent = 'save failed (' + (e && e.code || 'error') + ') — try again'; }
  }

  document.addEventListener('click', async ev => {
    const chip = ev.target.closest('.chip');
    if (chip) { filter = chip.dataset.f; document.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', c === chip)); render(); return; }
    const btn = ev.target.closest('.btn');
    if (btn) {
      const art = btn.closest('.asset'); const id = art.dataset.id; const note = $('#note-' + id).value.trim();
      if (btn.dataset.d === 'changes' && !note) { $('#note-' + id).focus(); $('#saved-' + id).textContent = 'add a note saying what to change'; return; }
      await save(id, btn.dataset.d, note);
      art.dataset.state = btn.dataset.d; art.querySelectorAll('.btn').forEach(b => b.setAttribute('aria-pressed', b === btn));
      const pill = art.querySelector('.pill'); pill.className = 'pill ' + btn.dataset.d; pill.textContent = btn.dataset.d === 'changes' ? 'needs changes' : 'approved';
      const decided = assets.filter(a => stateOf(a) !== 'undecided').length; $('#p-num').textContent = decided; $('#p-bar').style.width = (100 * decided / assets.length) + '%';
      return;
    }
    const sa = ev.target.closest('.sec-approve');
    if (sa) {
      const n = Number(sa.dataset.sec); const targets = assets.filter(a => a.section === n && stateOf(a) === 'undecided');
      if (!confirm(`Approve all ${targets.length} undecided assets in this section as they stand?`)) return;
      sa.disabled = true; sa.textContent = 'approving…';
      for (const a of targets) { await save(a.id, 'approved', $('#note-' + a.id) ? $('#note-' + a.id).value.trim() : ''); }
      render();
    }
  });
  document.addEventListener('change', ev => { if (ev.target.id === 'jump' && ev.target.value) { const el = document.getElementById(ev.target.value); if (el) el.scrollIntoView({ block: 'start' }); ev.target.value = ''; } });
  document.addEventListener('input', ev => {
    if (ev.target.tagName === 'TEXTAREA') { const id = ev.target.id.slice(5); const d = decisions[id]; if (d && d.decision) { clearTimeout(ev.target._t); ev.target._t = setTimeout(() => save(id, d.decision, ev.target.value.trim()), 800); } }
  });

  render();
  (async () => {
    const st = $('#save-state');
    try { db = window.claude && window.claude.use ? await window.claude.use('db') : null; } catch (e) { db = null; }
    if (!db) { st.textContent = 'answers will not save in this view — reply in chat instead'; st.classList.add('warn'); return; }
    st.textContent = 'saving to the shared record';
    db.collection('reviews').onSnapshot(snap => {
      let changed = false;
      for (const doc of snap.docs) { const d = doc.data(); if (d && byId[doc.id]) { decisions[doc.id] = d; changed = true; } }
      if (changed) render();
    }, e => { st.textContent = 'live updates unavailable (' + (e && e.code || 'error') + '); saves still attempted'; st.classList.add('warn'); });
  })();
})();
</script>
"""
out = HERE / "review-deck.html"
out.write_text(html.replace("__DATA__", payload), encoding="utf-8", newline="\n")
print("wrote", out, out.stat().st_size // 1024, "KB")

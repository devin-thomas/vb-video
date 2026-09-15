#!/usr/bin/env python3
"""Build an offline, dependency-free review gallery and editor handoff."""
from pathlib import Path
import json,html,shutil
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'manifest.json').read_text())['tickets'];deliveries=json.loads((ROOT/'review/production-index.json').read_text());assets=[d for d in deliveries if not d['id'].startswith('OPS')]
byid={r['id']:r for r in rows};items=[]
for d in assets:
 id=d['id'];base=ROOT/'assets'/id;build=json.loads((base/'src/build.json').read_text())
 thumb=base/'proofs/gallery.jpg';Image.open(base/'exports/poster.png').convert('RGB').resize((640,360),Image.Resampling.LANCZOS).save(thumb,quality=86,optimize=True)
 item={**d,'group':id.split('-')[0],'poster':f'assets/{id}/exports/poster.png','thumb':f'assets/{id}/proofs/gallery.jpg','video':f'assets/{id}/exports/preview.mp4' if d['duration_seconds'] else None,'source':f'assets/{id}/src/index.html','ticket':f'tickets/{id}.md','qa':f'assets/{id}/qa.md','delivery':f'assets/{id}/delivery.json','variants':[{'name':name,'png':f'assets/{id}/exports/{name}.png','mp4':f'assets/{id}/exports/{name}.mp4' if (base/'exports'/f'{name}.mp4').exists() else None,'svg':f'assets/{id}/src/variant-{name}.svg'} for name in build['variants']]}
 items.append(item)
DATA=json.dumps(items,ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Visual Basic — Asset review</title><style>
:root{color-scheme:dark;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#111318;color:#f1f3f5}*{box-sizing:border-box}body{margin:0}header{padding:28px 32px 22px;border-bottom:1px solid #303840}h1{font-size:25px;font-weight:650;margin:0 0 12px}header p{color:#aeb6bf;margin:10px 0;font-size:14px}a{color:#91bcff;text-underline-offset:3px}nav{display:flex;gap:18px;flex-wrap:wrap}main{padding:22px 32px 50px;max-width:1900px;margin:auto}.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:22px}input,select,button{font:inherit;border:1px solid #46515d;border-radius:3px;background:#1b2027;color:inherit;padding:11px 13px}input{min-width:240px;flex:1;max-width:470px}button{cursor:pointer}button:hover,a:hover{filter:brightness(1.25)}#count{color:#aeb6bf;font-size:14px;margin-left:auto}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:25px 20px}.tile{border:0;background:none;padding:0;text-align:left;display:block;width:100%}.tile img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block;border:1px solid #323b46;background:#08090c}.tile h2{font-size:15px;font-weight:600;line-height:1.4;margin:10px 0 4px}.meta{font-size:12px;color:#aeb6bf}.flag{color:#eab676}.empty{color:#adb5bf}dialog{width:min(1500px,96vw);max-height:95vh;border:1px solid #485460;background:#111318;color:inherit;padding:20px;border-radius:4px}dialog::backdrop{background:#000c}.dialogtop{display:flex;align-items:center;gap:12px;margin-bottom:14px}.dialogtop h2{font-size:18px;margin:0;flex:1}.media{background:#000}.media video,.media img{display:block;width:100%;max-height:65vh;object-fit:contain}.tools{display:flex;gap:17px;flex-wrap:wrap;align-items:center;margin-top:17px}.note{color:#c4cbd2;font-size:14px;line-height:1.6}.note strong{color:#eab676}@media(max-width:600px){header,main{padding:20px 16px}.grid{grid-template-columns:1fr}dialog{padding:12px}.filters{align-items:stretch}#count{margin-left:0;width:100%}}
</style></head><body><header><h1>Visual Basic · Asset review</h1><nav><a href="PREVIEW_REEL.mp4">Preview reel</a><a href="README.md">Delivery guide</a><a href="review/REMAINING_TICKETS.md">Remaining tickets</a><a href="assets/OPS-01/exports/card-atlas.png">Card atlas</a></nav><p>71 produced asset packages · 1920 × 1080 · motion at 30 fps · silent. Claim-gated assets remain internal proofs.</p></header><main><div class="filters"><input id="search" type="search" placeholder="Find a ticket or asset" aria-label="Find a ticket or asset"><select id="group" aria-label="Asset family"><option value="">All assets</option><option value="DIA">Diagrams</option><option value="CODE">Code</option><option value="CMP">Comparisons</option><option value="CH">Chapters</option><option value="CARD">Opening / end cards</option><option value="MOCK">Mockups</option><option value="FACT">Fact cards</option><option value="REF">Reference code</option></select><span id="count"></span></div><div class="grid" id="grid"></div></main><dialog id="dialog"><div class="dialogtop"><h2 id="title"></h2><button id="close" aria-label="Close preview">Close</button></div><div class="media" id="media"></div><div class="tools"><select id="variant" aria-label="Variant"></select><a id="png" href="#">PNG</a><a id="mp4" href="#">MP4</a><a id="svg" href="#">SVG</a><a id="source" href="#">HTML source</a><a id="ticket" href="#">Ticket</a><a id="qa" href="#">QA</a></div><p class="note" id="note"></p></dialog><script>
const assets=__DATA__,grid=document.getElementById('grid'),search=document.getElementById('search'),group=document.getElementById('group'),dlg=document.getElementById('dialog');let current=null;
function render(){const query=search.value.toLowerCase(),items=assets.filter(a=>(!group.value||a.group===group.value)&&(!query||(a.id+' '+a.title).toLowerCase().includes(query)));document.getElementById('count').textContent=items.length+' assets';grid.replaceChildren();for(const a of items){const b=document.createElement('button');b.className='tile';const img=document.createElement('img');img.src=a.thumb;img.alt=a.title;img.loading='lazy';b.append(img);const h=document.createElement('h2');h.textContent=a.title;b.append(h);const m=document.createElement('div');m.className='meta';m.textContent=a.id+' · '+(a.duration_seconds?a.duration_seconds+' s':'Still')+(a.unresolved_gates.length?' · Claim review pending':'');b.append(m);b.onclick=()=>open(a);grid.append(b)}}
function setmedia(png,mp4,svg){const media=document.getElementById('media');media.replaceChildren();let el;if(mp4){el=document.createElement('video');el.src=mp4;el.controls=true;el.playsInline=true;el.preload='metadata';el.poster=png}else{el=document.createElement('img');el.src=png;el.alt=current.title}media.append(el);document.getElementById('png').href=png;const link=document.getElementById('mp4');link.hidden=!mp4;if(mp4)link.href=mp4;document.getElementById('svg').href=svg}
function open(a){current=a;document.getElementById('title').textContent=a.id+' · '+a.title;document.getElementById('source').href=a.source;document.getElementById('ticket').href=a.ticket;document.getElementById('qa').href=a.qa;const v=document.getElementById('variant');v.replaceChildren();v.add(new Option('Main preview','-1'));a.variants.forEach((x,i)=>v.add(new Option(x.name,i)));v.onchange=()=>{const i=Number(v.value);if(i<0)setmedia(a.poster,a.video,'assets/'+a.id+'/src/scene.svg');else{const x=a.variants[i];setmedia(x.png,x.mp4,x.svg)}};v.onchange();document.getElementById('note').textContent=a.unresolved_gates.length?'Produced artwork. Editorial gates still open: '+a.unresolved_gates.join(', ')+'. Review QA before publication.':'Produced artwork. Final producer approval and narration timing remain separate.';dlg.showModal()}
document.getElementById('close').onclick=()=>dlg.close();dlg.addEventListener('close',()=>document.getElementById('media').replaceChildren());search.oninput=render;group.onchange=render;render();
</script></body></html>'''.replace('__DATA__',DATA)
(ROOT/'START_HERE.html').write_text(page)
# All links in the gallery are relative; no server, deployment, account or build needed.
records=[]
for r in rows:
 state=json.loads((ROOT/'assets'/r['id']/'state.json').read_text())
 if state['production_status']!='produced':records.append((r,state))
text='# Remaining tickets\n\nThe gallery contains produced media, not a declaration that the entire episode is complete. The original tickets remain the execution basis. A blocked capture is not replaced by a source-code illustration.\n\n'
for label in ['support','capture','archive','scout','still','motion','code']:
 filtered=[(r,s) for r,s in records if r['kind']==label]
 if not filtered:continue
 text+='## '+label.title()+'\n\n'
 for r,s in filtered:text+=f"- [{r['id']} — {r['title']}](../tickets/{r['id']}.md): **{s['production_status']}**.\n"
 text+='\n'
text+='## Human / capability handoffs\n\nThe seven original handoffs are preserved under [handoffs/README.md](../handoffs/README.md). Narration, sound, full screen recording, assembly, rights decisions, and upload were not silently completed. No account, purchase, or publication was performed.\n'
(ROOT/'review/REMAINING_TICKETS.md').write_text(text)
counts=Counter(a['group'] for a in items);motion=sum(bool(a['duration_seconds']) for a in assets);mp4s=list((ROOT/'assets').glob('*/exports/*.mp4'));pngs=list((ROOT/'assets').glob('*/exports/*.png'));duration=sum(a['duration_seconds'] or 0 for a in assets)
summary={'asset_packages':len(assets),'support_packages':1,'families':dict(counts),'motion_assets':motion,'still_assets':len(assets)-motion,'mp4_files':len(mp4s),'full_hd_export_pngs':sum(p.name!='contact-sheet.png' for p in pngs),'main_animation_duration_seconds':duration,'remaining_asset_tickets':130-len(assets),'release_approved_assets':0,'release_gated_assets':sum(bool(a['unresolved_gates']) for a in assets)}
(ROOT/'review/summary.json').write_text(json.dumps(summary,indent=2))
old=ROOT/'README.md';orig=ROOT/'docs/ORIGINAL_BUILD_PACK_README.md'
if not orig.exists():shutil.copyfile(old,orig)
old.write_text(f'''# Visual Basic — Produced asset delivery

**71 individually packaged assets + the shared visual/export system.** Open [START_HERE.html](START_HERE.html) after extracting the entire folder. No server or installation is required to browse the gallery and watch the MP4s.

## See the work
[Preview reel](PREVIEW_REEL.mp4) · [Visual contact sheet](CONTACT_SHEET.jpg) · [Remaining tickets](review/REMAINING_TICKETS.md) · [Original ticket index](docs/TICKET_INDEX.md)

This is an asset-production delivery, not the final narrated episode. Media is 1920 × 1080; motion is H.264 at 30 fps with no audio. The animations use deliberate step states and reading holds. They are not live program captures. The preview reel is a silent selection of assets, not narration-synchronized editing.

## Produced
| Family | Assets |
|---|---:|
| Opening and end cards | 2 |
| Chapter cards | 16 |
| Exact Program.vb code cards | 25 |
| C# / VB comparisons | 8 |
| Fact cards | 6 |
| War GUI and download mockups | 2 |
| MsgBox and BASIC reference-code visuals | 2 |
| Diagrams and algorithm animations | 10 |
| **Total asset tickets with rendered deliverables** | **71** |

There are **{motion} motion assets**, **{len(assets)-motion} still assets**, **{len(mp4s)} MP4 files** including required cutdowns, and **{summary['full_hd_export_pngs']} full-HD export PNGs** excluding contact sheets and temporal-keyframe subfolders. Main animation durations total **{duration:.2f} seconds**, excluding duplicated cutdowns. OPS-01 supplies the shared system, original 52-card vector deck plus card back, atlas, capability report, and export contract.

## Working with an asset
`assets/CODE-02/` is an example. `exports/` contains usable rendered media, `src/` contains separately editable SVG states plus HTML/timing data, `evidence/` preserves source anchors and actual checks, `proofs/` contains review-size imagery, and `delivery.json` inventories the outputs by SHA-256. `qa.md` describes the review actually performed and remaining gates. Each original ticket has a delivery addendum and links back to its own results.

Import PNGs and MP4s from the chosen asset's exports folder into your editor. Code-card clean and highlighted variants are separate, and long excerpts have extra clean pages rather than being reduced to illegible type. No narration timing is locked. For regeneration, read [shared/REBUILD.md](shared/REBUILD.md). Do not redistribute system fonts: no font files are included.

## Status and limits
**Produced is not release-approved.** All 71 have rendered files and executed technical checks. No publication approval is invented. Claim-gated proofs retain their original wording rather than silently rewriting your script. In particular, CH-10 still carries the source's “recursion” title; the matching diagram depicts the actual inner loop. Historical fact cards and other assigned claims remain marked for editorial review. See [EDITORIAL_REGISTER.md](docs/EDITORIAL_REGISTER.md).

**59 asset tickets remain unproduced.** The .NET SDK is absent here, so runtime captures and the actual project-settings capture are blocked. Code illustrations are not terminal screenshots. Historical-image sourcing and stock-footage scouting were not attempted in this batch; no reconstructed interface is passed off as archive material. Narration, music, effects, final assembly, and upload remain outside this delivery.

## Verification
The unchanged original sources passed their hash checks. The original pack's 130-ticket/50-family/74-cue coverage validator passed. All produced media packages are checked with the original delivery validator. Full-HD dimensions and MP4 codec/rate/duration are checked; offline HTML, deterministic seeking, and text canvas bounds are tested in installed Chromium. Visual review includes all posters on contact sheets and selected detailed/temporal views. It is not a claim that every frame received independent full-resolution human review.

Reports live in `review/`: summary.json, delivery-validation.json, browser-summary.json, pack-validation.txt, manual-review.json, reel-edit.json, and production-index.json. The immutable planning manifest remains in manifest.json; current production state is in assets/<ID>/state.json. The original start guide is preserved under docs/ORIGINAL_BUILD_PACK_README.md.
''')
# Curated contact sheet, made from actual rendered assets, not a replacement for them.
chosen=['CARD-01','MOCK-01','DIA-06','CODE-02','DIA-07','DIA-08','DIA-05','CMP-05','DIA-09','CH-07','FACT-02','MOCK-02']
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,22);fh=ImageFont.truetype(font,40)
sheet=Image.new('RGB',(1920,1760),'#111318');draw=ImageDraw.Draw(sheet);draw.text((24,22),'Visual Basic · Produced assets',font=fh,fill='#f1f3f5');draw.text((24,82),'Selected frames · 71 individual asset packages',font=f,fill='#aeb6bf')
for i,id in enumerate(chosen):
 x=(i%3)*640;y=145+(i//3)*394;im=Image.open(ROOT/'assets'/id/'exports/poster.png').convert('RGB').resize((628,353),Image.Resampling.LANCZOS);sheet.paste(im,(x+6,y));draw.text((x+16,y+361),id,font=f,fill='#c7d0dc')
sheet.save(ROOT/'CONTACT_SHEET.jpg',quality=92,optimize=True)
print(json.dumps(summary,indent=2))

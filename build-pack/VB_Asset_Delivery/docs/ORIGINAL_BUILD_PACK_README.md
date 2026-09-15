# Visual Basic War Video — Agent Asset Build Pack

**130 individual asset tickets · 4 coordination tickets · 7 human/capability handoffs**

This turns the supplied categorized plan into individually assignable work orders. It includes the exact original ASSET_PLAN.md, SCRIPT.md, and Program.vb, preserved byte-for-byte. It does **not** claim the visual assets have already been rendered, historical images acquired, rights cleared, the game executed, or the video assembled.

## Start here
1. Read [AGENTS.md](AGENTS.md) and the [production bible](docs/PRODUCTION_BIBLE.md).
2. Give your coordinator the kickoff prompt in [DISPATCH_PROMPTS.md](docs/DISPATCH_PROMPTS.md). Begin [OPS-01](tickets/OPS-01.md), [OPS-02](tickets/OPS-02.md), and [OPS-03](tickets/OPS-03.md) in parallel when supported.
3. Assign one [full ticket](docs/TICKET_INDEX.md) per worker. Each worker writes only its own asset folder and state file. Use `manifest.json` or `asset_index.csv` to select work; never substitute their short descriptions for the ticket.
4. Finish with [OPS-04](tickets/OPS-04.md), the delivery validator, manual inspection, and the relevant [human handoffs](handoffs/README.md).

```sh
python tools/validate_pack.py
python tools/dispatch.py --all
python tools/dispatch.py --lane code
# After CODE-02 has actually been produced:
python tools/validate_delivery.py --id CODE-02
```

The Python helpers use the standard library. Media production itself still requires appropriate local rendering/capture/.NET tools, inspected by the setup tickets rather than assumed installed. No remote service, paid subscription, renderer download, or system installation is authorized by the pack.

## What expanded
The plan contains **50 agent-assigned family rows**, not 50 final individually craftable files. Its “chapter cards” row alone becomes 16 tickets. Grouped code, comparisons, facts, historical versions, and independent runs are split rather than left as vague batches.

| Asset class | Individual tickets |
|---|---:|
| Diagrams and animations | 14 |
| Opening / end cards | 2 |
| Chapter title cards | 16 |
| Exact Program.vb code cards | 25 |
| C# / VB comparisons | 8 |
| Factoid cards | 6 |
| GUI / download mockups | 2 |
| Historical reference-code illustrations | 4 |
| Local runtime / editor captures | 6 |
| Historical-source visuals from the plan | 21 |
| Stock B-roll scouting shots | 6 |
| Script-only visual supplements | 20 |
| **Total asset tickets** | **130** |

Four additional OPS tickets coordinate infrastructure, the runtime harness, editorial evidence, and final QA. Seven H tickets cover the original Tier 3 boundaries. Optional/maybe script visuals are explicitly labeled in their tickets; a missing source cannot be silently replaced with fake evidence.

## Every ticket contains
An assigned owner role, scope and owned paths, source-file line anchors and embedded excerpts, dependencies, a specific creative/technical brief, exact copy or source payload, composition/states/timing, named variants, concrete output files, tailored acceptance checks, provenance/rights and editorial gates, and an individual completion-report contract.

The common templates provide consistency; they do not replace per-asset craft or review. Distinct titles, code excerpts, image versions, and runs have distinct IDs. Clean/highlighted states or cutdowns of the same underlying animation remain explicitly named variants of that asset.

## Source discrepancies are visible, not silently corrected
Read [EDITORIAL_REGISTER.md](docs/EDITORIAL_REGISTER.md). It flags the recursion heading versus the actual inner loop, the actual insufficient-card handling, round-cap/counter wording, pot allocation versus physical deck size, script sample output versus authentic runtime evidence, the absent .vbproj, historical/current-year assertions, and source-specific rights assumptions.

These gates do not freeze unrelated production. A code card or diagram can be an internal proof while its relevant publication wording awaits a decision. Production status and release approval are separate. No historical, legal, or lifecycle verification is claimed by this packaging work.

## Files and entry points
- [TICKET_INDEX.md](docs/TICKET_INDEX.md): every work order, grouped for navigation.
- [COVERAGE.md](docs/COVERAGE.md): all 50 original families and all 74 inline script visual cues mapped to specific tickets.
- [OUTPUT_CONTRACT.md](docs/OUTPUT_CONTRACT.md): formats, filenames, metadata, provenance, state, and QA requirements.
- `manifest.json` / `asset_index.csv`: machine-readable assignments, references, dependencies, and gates.
- `sources/LOCK.json`: hashes/byte counts of the unchanged uploaded originals.
- `fixtures/`: explicitly labeled deterministic teaching data, not observed game output.
- `assets/<ID>/state.json`: individually owned initial planning state; no fake placeholder media.
- `schemas/`: metadata examples to fill during real production.
- `handoffs/`: screen recording, gated media, music, sound, assembly, narration, and upload boundaries.

## Done means something specific
A source file is not a rendered asset. A public image URL is not an acquired, cleared image. A script’s example output is not a program run. An internal proof is not publication approval. An asset build pack is not a completed video. Preserve those distinctions throughout execution.

# Visual Basic War — video production

An AI-made YouTube video about writing the card game War in mid-90s-style Visual Basic. This repository holds the script, the program, every production asset, and the tooling that made and checks them.

- **Gallery:** open [START_HERE.html](START_HERE.html) locally to browse every produced asset.
- **Tracker:** each ticket and human handoff is a [GitHub issue](https://github.com/devin-thomas/vb-video/issues). Produced tickets are closed as a record; everything else is open.
- **What's left:** [review/REMAINING_TICKETS.md](review/REMAINING_TICKETS.md).

## Layout

| Path | What lives there |
|---|---|
| `War/` | Working copy of the script (`SCRIPT.md`, revised) and the program (`Program.vb`, `War.vbproj`) |
| `sources/` | Hash-locked original inputs (`ASSET_PLAN.md`, `SCRIPT.md`, `Program.vb`, `LOCK.json`). Never edit. |
| `assets/<family>/<ID>/` | One folder per ticket: `state.json`, and when produced `delivery.json`, `qa.md`, `exports/`, `src/`, `evidence/`, `proofs/` |
| `assets/shared/` | Shared visual system (original 52-card vector deck, atlas, version) |
| `assets/diagrams/`, `assets/slides/`, `assets/mockups/` | Also hold copies under the file names the original issues #1–#26 promised; see [assets/LEGACY_NAMES.md](assets/LEGACY_NAMES.md) |
| `docs/` | [Production bible](docs/PRODUCTION_BIBLE.md), [editorial register](docs/EDITORIAL_REGISTER.md), [output contract](docs/OUTPUT_CONTRACT.md), coverage and ticket index, [integration log](docs/INTEGRATION_LOG.md) |
| `docs/tickets/`, `docs/handoffs/` | The full work orders behind each GitHub issue |
| `tools/` | Validators, dispatcher, index builder, GitHub issue sync; `render/` (asset renderer), `war-harness/` (.NET harness and real-terminal capture), `fixtures/` |
| `review/` | QA reports, validation results, contact sheet, preview reel, generated summaries |
| `manifest.json`, `asset_index.csv` | Machine-readable ticket index: family, folder, dependencies, gates, GitHub issue |

Families: `cards`, `chapters`, `code`, `comparisons`, `diagrams`, `facts`, `mockups`, `reference-code`, `captures`, `stills`, `historical`, `broll`, `ops`.

## Working on a ticket

Read [AGENTS.md](AGENTS.md), the ticket in `docs/tickets/`, and the documents it names. Write only inside the ticket's asset folder, keep `state.json` current, and keep the GitHub issue in step. *Produced* is not *release-approved*: release needs the producer's recorded decision on every editorial gate.

```sh
python tools/validate_pack.py                  # planning structure, source hashes, coverage
python tools/validate_delivery.py --id CODE-02 # one delivered asset: files, hashes, gates
python tools/dispatch.py --lane research       # tickets ready to start
python tools/build_indexes.py                  # gallery, asset_index.csv, remaining tickets, summary
python tools/github_issues.py --dry-run        # compare issues with ticket state
```

## History

The work orders and the first 71 assets came from a build pack (`Visual_Basic_Produced_Assets.zip`) that was first kept in `build-pack/` and then moved into this layout. [docs/INTEGRATION_LOG.md](docs/INTEGRATION_LOG.md) records each session, including corrections made during the move.

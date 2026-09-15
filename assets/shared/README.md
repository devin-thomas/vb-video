# Shared visual system (OPS-01)

Every rendered asset draws on this folder. `cards/` holds the 52 original card-face vectors plus the card back, `card-atlas.svg` shows them together, and `VERSION.json` records the frozen system version (`win95-workbench-1.0.0`), canvas size and frame rate.

OPS-01 owns this folder. Its delivery record, QA and export contract are in [../ops/OPS-01/](../ops/OPS-01/); the renderer code that uses the system is in [../../tools/render/](../../tools/render/).

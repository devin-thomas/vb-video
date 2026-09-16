# Shared visual system (OPS-01)

Every rendered asset draws on this folder. `cards/` holds the 52 original card-face vectors plus the card back, `card-atlas.svg` shows them together, and `VERSION.json` records the frozen system version (`win95-workbench-1.1.0`), canvas size and frame rate.

Version 1.1.0 (OPS-01 revision 2, 2026-09-16) redrew the faces as regular playing cards: corner index and small suit in two opposite corners, the standard pip layout for 2–10 with the lower half rotated 180°, J/Q/K with a large letter and a simple court mark (cap, coronet, crown), and the ace alone with one large pip. Card size, colours, fonts, corner treatment and the back are unchanged from 1.0.0. Assets rendered before this version carry the old single-pip faces in their own `src/` copies until they are re-rendered.

OPS-01 owns this folder. Its delivery record, QA and export contract are in [../ops/OPS-01/](../ops/OPS-01/); the renderer code that uses the system is in [../../tools/render/](../../tools/render/).

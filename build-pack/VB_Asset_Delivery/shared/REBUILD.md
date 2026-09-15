# Local rebuild

No installation script is included. Required preinstalled capabilities are Python, CairoSVG, Pillow, ffmpeg/ffprobe. Chromium plus Playwright are used only for browser checks. The actual environment is recorded under assets/OPS-01/exports/capabilities.json. Font files are not supplied.

```sh
python shared/build_assets.py --id CODE-02
python shared/render_assets.py --id CODE-02
python shared/qa_browser.py
python tools/validate_pack.py
```

Read assets/OPS-01/exports/template-contract.md before editing. Regeneration overwrites the chosen ticket's source and resets its live state; it is intentionally not an automatic publication approval. Use the finish_delivery script only after personally reviewing the batch's current results. The checked-in review record describes this delivery, not all possible future modifications.

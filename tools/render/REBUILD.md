# Local rebuild

No installation script is included. Required preinstalled capabilities are Python, CairoSVG, Pillow, ffmpeg/ffprobe. Chromium plus Playwright are used only for browser checks. The original batch's environment is recorded under assets/ops/OPS-01/exports/capabilities.json; a delivery finished later with `--id` records its own toolchain in delivery.json. Font files are not supplied. On Windows, CairoSVG also needs a native Cairo DLL (for example MSYS2's mingw-w64-ucrt-x86_64-cairo, found through CAIROCFFI_DLL_DIRECTORIES) and fontconfig's fc-match on PATH.

```sh
python tools/render/build_assets.py --id CODE-02
python tools/render/render_assets.py --id CODE-02
python tools/render/qa_browser.py --id CODE-02
python tools/render/finish_delivery.py --id CODE-02
python tools/validate_delivery.py --id CODE-02
python tools/validate_pack.py
```

Read assets/ops/OPS-01/exports/template-contract.md before editing. Regeneration overwrites the chosen ticket's source and resets its live state; it is intentionally not an automatic publication approval. Use the finish_delivery script only after personally reviewing the chosen tickets' current results: without `--id` it re-finishes every delivery, and without `--deliveries-only` it also rebuilds OPS-01. The checked-in review record describes this delivery, not all possible future modifications.

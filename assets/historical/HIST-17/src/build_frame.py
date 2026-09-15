#!/usr/bin/env python3
"""HIST-17 editorial frame: the 1996-10-22 TUCOWS capture framed at 16:9 without the Wayback toolbar.

Run from the repository root:  python assets/historical/HIST-17/src/build_frame.py

Method (reversible, recorded in evidence/frame.json):
1. Load the toolbar-free Wayback replay (if_ mode) in Chromium with a 1280x720 CSS viewport and
   deviceScaleFactor 1.5, so the page is rendered natively at 1920x1080 pixels (no raster upscaling,
   no stretching). The frame is the top of the page: logo, headline, banner and first mirror rows.
2. Also crop the same CSS region (0,0)-(1280,720) from source/raw/wayback-replay-fullpage.png and
   upscale it with Lanczos to 1920x1080 as proofs/frame-crop-check.png, so a reviewer can confirm the
   frame matches the uncropped capture.
3. Downscale the export to 1280x720 as proofs/editorial-frame-720.png for the 720p review.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path

from PIL import Image

import acquire

BASE = acquire.BASE
URL = f"https://web.archive.org/web/{acquire.TS}if_/{acquire.PAGE}"
CSS_VIEW = (1280, 720)
SCALE = 1.5


async def render(dest: Path) -> dict:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": CSS_VIEW[0], "height": CSS_VIEW[1]},
                                        device_scale_factor=SCALE)
        page = await ctx.new_page()
        responses: list = []
        page.on("response", lambda r: responses.append([r.status, r.url]))
        error = None
        for _ in range(3):
            try:
                await page.goto(URL, wait_until="load", timeout=180000)
                await page.wait_for_timeout(5000)
                error = None
                break
            except Exception as exc:
                error = str(exc)
        # Frame-less replay injects no toolbar; confirm no Wayback UI element is present.
        toolbar = await page.evaluate("!!document.getElementById('wm-ipp-base') || !!document.getElementById('wm-ipp')")
        await page.screenshot(path=str(dest), clip={"x": 0, "y": 0, "width": CSS_VIEW[0], "height": CSS_VIEW[1]})
        info = {"url": URL, "final_url": page.url, "title": await page.title(), "load_error": error,
                "wayback_toolbar_present": toolbar, "chromium": browser.version, "accessed": acquire.now(),
                "responses": responses}
        await browser.close()
    return info


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    exports = BASE / "exports"
    proofs = BASE / "proofs"
    exports.mkdir(exist_ok=True)
    proofs.mkdir(exist_ok=True)
    frame = exports / "editorial-frame.png"
    info = asyncio.run(render(frame))
    with Image.open(frame) as im:
        assert im.size == (1920, 1080), im.size
        im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(proofs / "editorial-frame-720.png", optimize=True)
    full = BASE / "source" / "raw" / "wayback-replay-fullpage.png"
    with Image.open(full) as im:
        full_size = im.size
        im.crop((0, 0, *CSS_VIEW)).resize((1920, 1080), Image.LANCZOS).save(proofs / "frame-crop-check.png", optimize=True)
    record = {
        "export": "exports/editorial-frame.png",
        "method": "Native Chromium render of the same Wayback capture at deviceScaleFactor 1.5; no raster upscale of the export.",
        "crop_css_px": {"x": 0, "y": 0, "width": CSS_VIEW[0], "height": CSS_VIEW[1]},
        "crop_of_uncropped_capture": {"file": "source/raw/wayback-replay-fullpage.png", "size_px": list(full_size),
                                      "region_px": [0, 0, *CSS_VIEW]},
        "omitted_context": "Everything below CSS y=720: the remaining regional mirror lists (Canada through South America) and the page footer with the 1996 copyright line. The Wayback toolbar is excluded.",
        "added_elements": "none",
        "render": info,
        "sha256": {"exports/editorial-frame.png": sha(frame)},
    }
    (BASE / "evidence" / "frame.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "render"}, indent=2))
    print("toolbar present:", info["wayback_toolbar_present"], "load_error:", info["load_error"])


if __name__ == "__main__":
    main()

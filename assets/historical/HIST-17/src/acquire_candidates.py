#!/usr/bin/env python3
"""HIST-17 alternate candidates: TUCOWS mirror pages archived in late 1996.

Run from the repository root:  python assets/historical/HIST-17/src/acquire_candidates.py
Writes raw id_ HTML, uncropped toolbar captures and toolbar-free replay captures to
source/candidates/<name>/ and appends a log to evidence/candidates-log.json.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import acquire  # noqa: E402  (reuses fetch/now helpers)

BASE = acquire.BASE
CANDIDATES = {
    "B-idirect-19961230": ("19961230051406", "http://tucows.idirect.com:80/"),
    "C-phoenix-win95oct96-19961117": ("19961117161725", "http://tucows.phoenix.net:80/archive/win95oct96.html"),
}


async def capture(name: str, ts: str, page_url: str) -> dict:
    from playwright.async_api import async_playwright
    out = BASE / "source" / "candidates" / name
    out.mkdir(parents=True, exist_ok=True)
    log = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for mode, url in {"wayback-toolbar": f"https://web.archive.org/web/{ts}/{page_url}",
                          "wayback-replay": f"https://web.archive.org/web/{ts}if_/{page_url}"}.items():
            ctx = await browser.new_context(viewport={"width": 1280, "height": 1024}, device_scale_factor=1)
            page = await ctx.new_page()
            responses: list = []
            page.on("response", lambda r, responses=responses: responses.append([r.status, r.url]))
            error = None
            for _ in range(3):
                try:
                    await page.goto(url, wait_until="load", timeout=180000)
                    await page.wait_for_timeout(5000)
                    error = None
                    break
                except Exception as exc:
                    error = str(exc)
            await page.screenshot(path=str(out / f"{mode}-viewport.png"))
            await page.screenshot(path=str(out / f"{mode}-fullpage.png"), full_page=True)
            log[mode] = {"url": url, "final_url": page.url, "title": await page.title(),
                         "document_px": await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]"),
                         "viewport": [1280, 1024], "accessed": acquire.now(), "load_error": error,
                         "chromium": browser.version, "responses": responses}
            await ctx.close()
        await browser.close()
    return log


def main() -> None:
    result = {}
    for name, (ts, page_url) in CANDIDATES.items():
        dest = BASE / "source" / "candidates" / name / "original.html"
        rec = acquire.fetch(f"https://web.archive.org/web/{ts}id_/{page_url}", dest)
        cap = asyncio.run(capture(name, ts, page_url))
        result[name] = {"timestamp": ts, "archived_url": page_url, "download": rec, "captures": cap}
        print(name, rec["bytes"], {k: (v["title"], v["document_px"], v["load_error"]) for k, v in cap.items()})
    (BASE / "evidence" / "candidates-log.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

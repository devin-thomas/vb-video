#!/usr/bin/env python3
"""HIST-17 acquisition: raw Wayback Machine payloads plus Chromium captures of the replay.

Run from the repository root:  python assets/historical/HIST-17/src/acquire.py
Network access to web.archive.org is required. No account, cookie, or form is used.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source"
RAW = SRC / "raw"
EVI = BASE / "evidence"
TS = "19961022175612"
PAGE = "http://www.tucows.com:80/"

# id_ = the archived bytes exactly as captured, without Wayback rewriting or toolbar.
DOWNLOADS = [
    (f"https://web.archive.org/web/{TS}id_/{PAGE}", SRC / "original.html"),
    ("https://web.archive.org/web/19961228134206id_/http://www.tucows.com:80/", RAW / "comparison-19961228134206.html"),
    ("https://web.archive.org/web/19961022175627id_/http://www.tucows.com:80/images/Logo.gif", RAW / "Logo-19961022175627.gif"),
    ("https://web.archive.org/web/19961023235229id_/http://www.tucows.com:80/images/blue.gif", RAW / "blue-19961023235229.gif"),
    ("https://web.archive.org/web/19961023235236id_/http://www.tucows.com:80/images/fast-burst.gif", RAW / "fast-burst-19961023235236.gif"),
    ("https://web.archive.org/web/19961023235207id_/http://www.tucows.com:80/images/adds/cs_ad.gif", RAW / "cs_ad-19961023235207.gif"),
]

CAPTURES = {
    # Uncropped evidence: includes the Wayback Machine toolbar with URL and capture date.
    "wayback-toolbar": f"https://web.archive.org/web/{TS}/{PAGE}",
    # Same capture in Wayback's frame-less replay mode (no toolbar); basis for the editorial frame.
    "wayback-replay": f"https://web.archive.org/web/{TS}if_/{PAGE}",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fetch(url: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HIST-17 archival research (python urllib)"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                headers = dict(resp.headers.items())
                status = resp.status
                final = resp.geturl()
            dest.write_bytes(data)
            return {"url": url, "final_url": final, "status": status, "path": dest.relative_to(BASE).as_posix(),
                    "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "accessed": now(),
                    "headers": {k: v for k, v in headers.items()
                                if k.lower().startswith(("x-archive", "memento", "content-type", "link", "date", "last-modified"))}}
        except Exception as exc:  # network flakiness from the Wayback Machine is common
            last = exc
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


async def capture() -> dict:
    from playwright.async_api import async_playwright
    RAW.mkdir(parents=True, exist_ok=True)
    log: dict = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for name, url in CAPTURES.items():
            ctx = await browser.new_context(viewport={"width": 1280, "height": 1024}, device_scale_factor=1)
            page = await ctx.new_page()
            responses: list = []
            page.on("response", lambda r, responses=responses: responses.append([r.status, r.url]))
            error = None
            for attempt in range(3):
                try:
                    await page.goto(url, wait_until="load", timeout=180000)
                    await page.wait_for_timeout(5000)
                    error = None
                    break
                except Exception as exc:
                    error = str(exc)
            await page.screenshot(path=str(RAW / f"{name}-viewport.png"))
            await page.screenshot(path=str(RAW / f"{name}-fullpage.png"), full_page=True)
            dims = await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]")
            log[name] = {"url": url, "final_url": page.url, "title": await page.title(), "document_px": dims,
                         "viewport": [1280, 1024], "accessed": now(), "load_error": error,
                         "chromium": browser.version, "responses": responses}
            await ctx.close()
        await browser.close()
    return log


def main() -> None:
    EVI.mkdir(parents=True, exist_ok=True)
    records = []
    for url, dest in DOWNLOADS:
        rec = fetch(url, dest)
        print("downloaded", rec["path"], rec["bytes"], rec["status"])
        records.append(rec)
        time.sleep(2)
    log = asyncio.run(capture())
    for name, info in log.items():
        print("captured", name, info["title"], info["document_px"], info["load_error"])
    (EVI / "acquisition-log.json").write_text(
        json.dumps({"downloads": records, "captures": log}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

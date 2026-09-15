"""Capture the Wayback Machine replay of the classicvb.org petition (banner kept)."""
import datetime
import json
import os
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://web.archive.org/web/20050312064351/http://classicvb.org:80/petition/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5)
    responses = []
    page.on("response", lambda r: responses.append([r.status, r.url]))
    accessed = datetime.datetime.now(datetime.timezone.utc).isoformat()
    page.goto(URL, wait_until="networkidle", timeout=120000)
    time.sleep(3)
    page.screenshot(path=os.path.join(HERE, "wayback_fullpage_dpr15.png"), full_page=True)
    banner = page.evaluate(
        "(()=>{const w=document.getElementById('wm-ipp-base');"
        "if(!w) return null; const r=w.shadowRoot||w;"
        "return r.textContent.replace(/\\s+/g,' ').trim().slice(0,600)})()"
    )
    log = {
        "url": URL,
        "final_url": page.url,
        "accessed_utc": accessed,
        "title": page.title(),
        "chromium": browser.version,
        "viewport": [1280, 720],
        "device_scale_factor": 1.5,
        "doc_size": page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.scrollHeight]"
        ),
        "banner_text": banner,
        "responses": responses,
    }
    browser.close()

with open(os.path.join(HERE, "capture_log.json"), "w", encoding="utf-8") as fh:
    json.dump(log, fh, indent=1)
print(json.dumps({k: v for k, v in log.items() if k != "responses"}, indent=1))
print(len(responses), "responses")
for status, url in responses:
    if "classicvb" in url:
        print(status, url)

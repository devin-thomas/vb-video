"""HIST-18 capture: render the archived download.com front door (Wayback capture 19961221110042).

Offline mode (default) loads the byte-exact archived HTML (source/original.html) in headless Chromium and
answers every request for http://www.download.com/... with the byte-exact archived image copies in
source/embeds/ (mapping: evidence/embeds.json). The HTML is not modified; nothing is fetched from the network;
any request without an archived copy is aborted and logged (a missing image would render as broken, not
substituted). JavaScript is disabled (the page contains none).

--replay additionally screenshots the live Wayback Machine replay page (with the archive's own toolbar)
as evidence of the source page. It needs network access and is not required to rebuild the exports.

Run from the repository root:
    python assets/historical/HIST-18/src/capture.py [--replay]
"""
import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

A = Path(__file__).resolve().parents[1]
ORIGIN = 'http://www.download.com'
WAYBACK = 'https://web.archive.org/web/19961221110042/http://www.download.com/'
VIEWPORT = {'width': 800, 'height': 600}  # common 1996 desktop resolution; the page layout is a fixed 600 px table


def embed_map():
    rows = json.loads((A / 'evidence/embeds.json').read_text(encoding='utf-8'))
    return {ORIGIN + r['src']: A / 'source/embeds' / r['saved'] for r in rows}


async def offline(pw, scale, out, log):
    html = (A / 'source/original.html').read_bytes()
    files = embed_map()
    browser = await pw.chromium.launch()
    ctx = await browser.new_context(viewport=VIEWPORT, device_scale_factor=scale, java_script_enabled=False)
    page = await ctx.new_page()

    async def handle(route):
        url = route.request.url
        if url in (ORIGIN + '/', ORIGIN + ':80/'):
            await route.fulfill(status=200, body=html, content_type='text/html; charset=iso-8859-1')
        elif url in files:
            await route.fulfill(status=200, body=files[url].read_bytes(), content_type='image/gif')
        else:
            log.append({'scale': scale, 'aborted': url})
            await route.abort()

    await page.route('**/*', handle)
    await page.goto(ORIGIN + '/', wait_until='load')
    broken = await page.evaluate("[...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)")
    fonts = await page.evaluate("""() => {
        const pick = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily : null; };
        return {body: pick('body'), tt: pick('tt'), courier_highlight: pick('font[face]')};
    }""")
    size = await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]")
    # Size the viewport to the whole document and take a plain viewport shot: equivalent to a full-page
    # capture, and avoids a Chromium full_page stall observed at device_scale_factor 2 on Windows.
    await page.set_viewport_size({'width': max(VIEWPORT['width'], size[0]), 'height': max(VIEWPORT['height'], size[1])})
    await page.screenshot(path=str(out), full_page=False, animations='disabled', timeout=60000)
    await browser.close()
    return {'scale': scale, 'out': out.relative_to(A).as_posix(), 'css_size': size, 'images': len(files),
            'broken_images': broken, 'computed_font_family': fonts}


async def replay(pw, out):
    browser = await pw.chromium.launch()
    ctx = await browser.new_context(viewport={'width': 1280, 'height': 900})
    page = await ctx.new_page()
    failed = []
    page.on('response', lambda r: failed.append([r.status, r.url]) if r.status >= 400 else None)
    await page.goto(WAYBACK, wait_until='load', timeout=120000)
    try:
        await page.wait_for_load_state('networkidle', timeout=60000)
    except Exception:
        pass
    await page.screenshot(path=str(out), full_page=False)
    await browser.close()
    return {'out': out.relative_to(A).as_posix(), 'url': WAYBACK, 'http_errors': failed}


async def main():
    log, results = [], []
    async with async_playwright() as pw:
        results.append(await offline(pw, 1, A / 'source/raw/capture-800w-1x.png', log))
        results.append(await offline(pw, 2, A / 'source/raw/capture-800w-2x.png', log))
        if '--replay' in sys.argv:
            results.append(await replay(pw, A / 'evidence/wayback-replay-page.png'))
        results.append({'chromium_version': pw.chromium.name, 'aborted_requests': log})
    print(json.dumps(results, indent=1))
    (A / 'evidence/capture-log.json').write_text(json.dumps(results, indent=1) + '\n', encoding='utf-8')


asyncio.run(main())

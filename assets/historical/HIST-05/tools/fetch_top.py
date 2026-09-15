"""Single wait, then a minimal fetch: top candidate plus one backup. No polling, no retry loop."""
import datetime as dt
import hashlib
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "VBWarVideoResearch/1.0 (HIST-05 provenance research; minimal fetch)"
OUT = Path(__file__).parent / "candidates"
OUT.mkdir(exist_ok=True)
NOT_BEFORE = dt.datetime(2026, 9, 15, 20, 50, 30, tzinfo=dt.timezone.utc)
FILES = [
    ("C64_startup_animiert.gif", "https://upload.wikimedia.org/wikipedia/commons/4/48/C64_startup_animiert.gif"),
    ("Commodore_64_Splash.png", "https://upload.wikimedia.org/wikipedia/commons/f/fd/Commodore_64_Splash.png"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=40)
    return resp.read(), resp.geturl(), resp.headers


wait = (NOT_BEFORE - dt.datetime.now(dt.timezone.utc)).total_seconds()
if wait > 0:
    print(f"single wait {wait:.0f}s until {NOT_BEFORE.isoformat()}", flush=True)
    time.sleep(wait)

for name, url in FILES:
    routes = [("commons-upload", url), ("wayback-raw", "https://web.archive.org/web/2026id_/" + url)]
    for route, u in routes:
        try:
            data, final, headers = fetch(u)
        except urllib.error.HTTPError as exc:
            print(f"{name} via {route}: HTTP {exc.code} Retry-After={exc.headers.get('Retry-After')}", flush=True)
            continue
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"{name} via {route}: network error {exc}", flush=True)
            continue
        (OUT / name).write_bytes(data)
        print(f"{name} via {route}: OK bytes={len(data)} sha1={hashlib.sha1(data).hexdigest()} "
              f"sha256={hashlib.sha256(data).hexdigest()} final_url={final} date={headers.get('Date')} "
              f"last_modified={headers.get('Last-Modified')} content_type={headers.get('Content-Type')}", flush=True)
        break
    time.sleep(10)
print("finished", dt.datetime.now(dt.timezone.utc).isoformat(), flush=True)

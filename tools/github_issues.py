#!/usr/bin/env python3
"""Keep one GitHub issue per ticket (docs/tickets) and per human handoff (docs/handoffs), and record the numbers.

An issue whose title starts with "<ID>:" is reused, so reruns update rather than duplicate. Produced tickets are
closed as completed; everything else stays open. Labels are created when missing. Authentication comes from gh.

  python tools/github_issues.py --dry-run        # show what would change
  python tools/github_issues.py                  # create/update issues, write github_issue into manifest.json
  python tools/github_issues.py --link-legacy    # one-time comment on the original issues #1–#26
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "devin-thomas/vb-video"
URL = f"https://github.com/{REPO}"
PACE_SECONDS = 1.1
LEGACY_MARKER = "<!-- vb-video:ticket-links -->"

COLORS = {"family": "1d76db", "status: produced": "0e8a16", "status: in progress": "fbca04", "status: planned": "c5def5",
          "release: approved": "0e8a16", "release: blocked": "b60205", "release: unreviewed": "d4c5f9",
          "gate": "e99695", "lane": "bfdadc", "ticket": "5319e7", "handoff": "d93f0b"}

# Original coarse issues -> tickets that now carry their work, plus the file names those issues promised.
LEGACY = {
    1: (["DIA-01"], ["assets/diagrams/event-driven-programming.svg"]),
    2: (["DIA-02"], ["assets/diagrams/war-rules-animation.html"]),
    3: (["DIA-03"], ["assets/diagrams/card-rank-chart.svg"]),
    4: (["DIA-04"], ["assets/diagrams/byref-vs-byval.svg"]),
    5: (["DIA-05"], ["assets/diagrams/array-as-queue.html"]),
    6: (["DIA-06"], ["assets/diagrams/fisher-yates-shuffle.html"]),
    7: (["DIA-07"], ["assets/diagrams/deck-building-loop.html"]),
    8: (["DIA-08"], ["assets/diagrams/war-mechanic-steps.svg"]),
    9: (["DIA-09"], ["assets/diagrams/pot-growth.svg"]),
    10: (["DIA-10"], ["assets/diagrams/game-flowchart.svg"]),
    11: (["DIA-11"], ["assets/diagrams/1995-tools-comparison.svg"]),
    12: (["DIA-12"], ["assets/diagrams/mac-vs-windows.svg"]),
    13: (["DIA-13"], ["assets/diagrams/vb-influence-lineage.svg"]),
    14: (["DIA-14"], ["assets/diagrams/vb-timeline.svg"]),
    15: (["CARD-01"], ["assets/slides/title-card.html"]),
    16: ([f"CH-{n:02d}" for n in range(1, 17)], ["assets/slides/chapter-01.svg … chapter-16.svg", "assets/slides/chapter-template.html"]),
    17: ([f"CODE-{n:02d}" for n in range(1, 26)], ["assets/slides/code-01-structure-card.svg … code-08-give-cards.svg"]),
    18: ([f"CMP-{n:02d}" for n in range(1, 9)], ["assets/slides/compare-01-void-vs-sub.svg … compare-04-declaration.svg"]),
    19: ([f"FACT-{n:02d}" for n in range(1, 7)], ["assets/slides/factoid-01.svg … factoid-06.svg", "assets/slides/factoid-template.html"]),
    20: (["CARD-02"], ["assets/slides/end-card.html"]),
    21: (["MOCK-01"], ["assets/mockups/vb4-war-gui.html"]),
    22: (["MOCK-02"], ["assets/mockups/1996-download-dialog.html"]),
    23: (["REF-02", "REF-01"], ["assets/slides/code-contrast-win32-hello.svg", "assets/slides/code-contrast-mfc-msgmap.svg"]),
    24: (["REF-03"], ["assets/slides/code-contrast-vb-msgbox.svg"]),
    25: (["REF-04"], ["assets/slides/retro-basic-terminal.html"]),
    26: ([], ["assets/slides/code-contrast-java-awt.svg"]),
}


def load(path: Path):
    return json.loads(path.read_bytes().decode("utf-8"))


def gh(method: str, path: str, body: dict | None = None, content: bool = False):
    cmd = ["gh", "api", "--method", method, path]
    if body is not None:
        cmd += ["--input", "-"]
    for attempt in range(6):
        proc = subprocess.run(cmd, input=json.dumps(body) if body is not None else None, capture_output=True, text=True,
                              encoding="utf-8")
        if proc.returncode == 0:
            if content:
                time.sleep(PACE_SECONDS)
            return json.loads(proc.stdout) if proc.stdout.strip() else None
        err = proc.stderr + proc.stdout
        if "rate limit" in err.lower() or "HTTP 429" in err or "HTTP 502" in err or "HTTP 503" in err:
            wait = 60 * (attempt + 1)
            print(f"  rate limited or unavailable; waiting {wait}s", flush=True)
            time.sleep(wait)
            continue
        raise SystemExit(f"gh api {method} {path} failed: {err.strip()}")
    raise SystemExit(f"gh api {method} {path}: gave up after retries")


def paged(path: str) -> list[dict]:
    items, page = [], 1
    while True:
        batch = gh("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def absolute_links(markdown: str, base_dir: str, issue_for_path: dict[str, int]) -> str:
    def fix(match: re.Match) -> str:
        target = match.group(1)
        if re.match(r"^(https?:|mailto:|#)", target):
            return match.group(0)
        path, _, anchor = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(base_dir, path))
        if resolved in issue_for_path:
            return f"]({URL}/issues/{issue_for_path[resolved]})"
        kind = "tree" if path.endswith("/") or not posixpath.splitext(resolved)[1] else "blob"
        return f"]({URL}/{kind}/main/{resolved}{'#' + anchor if anchor else ''})"
    return re.sub(r"\]\(([^)\s]+)\)", fix, markdown)


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n+", "", text, flags=re.S)


def topo_order(rows: list[dict]) -> list[dict]:
    by_id, done, order = {r["id"]: r for r in rows}, set(), []
    first = [r["id"] for r in rows if r["kind"] == "support" and not r["deps"]]

    def visit(tid: str) -> None:
        if tid in done:
            return
        done.add(tid)
        for dep in by_id[tid]["deps"]:
            visit(dep)
        order.append(by_id[tid])
    for tid in first + [r["id"] for r in rows]:
        visit(tid)
    return order


def labels_for(row: dict, state: dict) -> list[str]:
    status = {"produced": "status: produced", "reviewed": "status: produced", "in_progress": "status: in progress"}.get(
        state["production_status"], "status: planned")
    return (["ticket", f"family: {row['asset_dir'].split('/')[1]}", f"lane: {row['lane']}", status,
             f"release: {state['release_status']}"] + [f"gate: {g}" for g in row["gates"]])


def ticket_body(row: dict, state: dict, numbers: dict[str, int], rows: list[dict], states: dict[str, dict]) -> str:
    tid, base = row["id"], row["asset_dir"]
    legacy = [n for n, (ids, _) in LEGACY.items() if tid in ids]
    deps = ", ".join(f"#{numbers[d]} ({d})" if d in numbers else d for d in row["deps"]) or "none"
    links = [f"[ticket file]({URL}/blob/main/{row['ticket']})", f"[asset folder]({URL}/tree/main/{base})",
             f"[state.json]({URL}/blob/main/{base}/state.json)"]
    for name in ["qa.md", "delivery.json"]:
        if (ROOT / base / name).exists():
            links.append(f"[{name}]({URL}/blob/main/{base}/{name})")
    ops03 = f"#{numbers['OPS-03']}" if "OPS-03" in numbers else "OPS-03"
    production, release = state["production_status"], state["release_status"]
    if production == "produced":
        if release == "approved":
            note = "Produced and release-approved by the producer. Closed as a record."
        elif row["gates"]:
            note = (f"Produced, so this issue is closed as a production record. Release is still blocked on editorial gates "
                    f"{', '.join(row['gates'])}; see qa.md and docs/EDITORIAL_REGISTER.md. Producer decisions are tracked in {ops03}.")
        else:
            note = f"Produced, so this issue is closed as a production record. The producer has not reviewed release yet ({ops03})."
    else:
        note = " ".join(state.get("notes") or []) or "Not started."
    head = [
        "| | |", "|---|---|",
        f"| **Ticket** | `{tid}` · {row['kind']} · lane `{row['lane']}` · priority `{row['priority']}` |",
        f"| **Production** | {production} |",
        f"| **Release** | {release} |",
        f"| **Editorial gates** | {', '.join(row['gates']) or 'none'} |",
        f"| **Depends on** | {deps} |",
        f"| **Original issue** | {', '.join(f'#{n}' for n in legacy) or 'none'} |",
        "", " · ".join(links), "", f"> {note}", "",
    ]
    if tid == "OPS-03":
        pending = [r for r in rows if states[r["id"]]["production_status"] == "produced" and states[r["id"]]["release_status"] != "approved"]
        head += ["### Produced assets awaiting a producer release decision", ""]
        head += [f"- [ ] {('#' + str(numbers[r['id']])) if r['id'] in numbers else r['id']} {r['id']} — "
                 f"{('gates ' + ', '.join(r['gates'])) if r['gates'] else 'no gates, approval only'}" for r in pending]
        head += [""]
    issue_for_path = {f"docs/tickets/{t}.md": n for t, n in numbers.items()}
    text = absolute_links(strip_frontmatter((ROOT / row["ticket"]).read_bytes().decode("utf-8")), "docs/tickets", issue_for_path)
    body = "\n".join(head) + "\n---\n\n" + text
    return body if len(body) < 60000 else body[:59000] + f"\n\n…truncated; read the full [ticket file]({URL}/blob/main/{row['ticket']})."


def handoff_body(path: Path, numbers: dict[str, int]) -> str:
    issue_for_path = {f"docs/tickets/{t}.md": n for t, n in numbers.items()}
    text = absolute_links(path.read_bytes().decode("utf-8"), "docs/handoffs", issue_for_path)
    return (f"> Human or capability handoff from the build pack: [{path.name}]({URL}/blob/main/docs/handoffs/{path.name}). "
            "It stays open until the real action has been performed and recorded.\n\n---\n\n" + text)


def ensure_labels(needed: set[str], dry: bool) -> None:
    existing = {l["name"] for l in paged(f"repos/{REPO}/labels")}
    for name in sorted(needed - existing):
        color = COLORS.get(name) or COLORS.get(name.split(":")[0], "ededed")
        print(f"label + {name}")
        if not dry:
            gh("POST", f"repos/{REPO}/labels", {"name": name, "color": color}, content=True)


def save_manifest(manifest: dict, raw: str) -> None:
    # A Windows checkout with core.autocrlf=true hands us CRLF; normalise before sniffing the layout, or the
    # pretty-printed 12k-line manifest silently collapses to one line.
    raw = raw.replace("\r\n", "\n")
    indent = 2 if raw.startswith("{\n") else None
    text = json.dumps(manifest, indent=indent, ensure_ascii="\\u" in raw) + ("\n" if raw.endswith("\n") else "")
    (ROOT / "manifest.json").write_bytes(text.encode("utf-8"))


def sync(dry: bool) -> None:
    raw = (ROOT / "manifest.json").read_bytes().decode("utf-8")
    manifest = json.loads(raw)
    rows = manifest["tickets"]
    states = {r["id"]: load(ROOT / r["asset_dir"] / "state.json") for r in rows}
    handoffs = sorted((ROOT / "docs/handoffs").glob("H[0-9][0-9].md"))
    existing = {}
    for issue in paged(f"repos/{REPO}/issues?state=all"):
        match = re.match(r"^([A-Z]+-\d+|H\d{2}):", issue["title"])
        if match and "pull_request" not in issue:
            existing[match.group(1)] = issue
    numbers = {k: v["number"] for k, v in existing.items()}
    needed = {"handoff"} | {label for r in rows for label in labels_for(r, states[r["id"]])}
    ensure_labels(needed, dry)

    def upsert(key: str, title: str, body: str, labels: list[str], closed: bool) -> None:
        issue = existing.get(key)
        state = "closed" if closed else "open"
        if issue is None:
            print(f"create {key} ({state})", flush=True)
            if dry:
                return
            created = gh("POST", f"repos/{REPO}/issues", {"title": title, "body": body, "labels": labels}, content=True)
            numbers[key] = created["number"]
            existing[key] = {**created, "body": body}
            if closed:
                gh("PATCH", f"repos/{REPO}/issues/{created['number']}", {"state": "closed", "state_reason": "completed"}, content=True)
                existing[key]["state"] = "closed"
            return
        changes = {}
        if issue["title"] != title:
            changes["title"] = title
        if (issue.get("body") or "") != body:
            changes["body"] = body
        if sorted(l["name"] if isinstance(l, dict) else l for l in issue.get("labels", [])) != sorted(labels):
            changes["labels"] = labels
        if issue["state"] != state:
            changes["state"] = state
            if closed:
                changes["state_reason"] = "completed"
        if changes:
            print(f"update #{issue['number']} {key}: {sorted(changes)}", flush=True)
            if not dry:
                gh("PATCH", f"repos/{REPO}/issues/{issue['number']}", changes, content=True)
                existing[key] = {**issue, **changes, "labels": [{"name": l} for l in changes.get("labels", [])] or issue.get("labels", [])}

    for passes in range(2):  # second pass fills issue references that did not exist yet during the first
        for row in topo_order(rows):
            state = states[row["id"]]
            upsert(row["id"], f"{row['id']}: {row['title']}", ticket_body(row, state, numbers, rows, states),
                   labels_for(row, state), state["production_status"] in ("produced", "reviewed"))
        for path in handoffs:
            title = path.read_bytes().decode("utf-8").splitlines()[0].lstrip("# ").strip()
            upsert(path.stem, title.replace(" — ", ": ", 1), handoff_body(path, numbers), ["handoff"], False)
        if dry:
            break
        for row in rows:
            if row["id"] in numbers:
                row["github_issue"] = numbers[row["id"]]
        manifest["handoff_issues"] = {p.stem: numbers[p.stem] for p in handoffs if p.stem in numbers}
        save_manifest(manifest, raw)
    print(f"tickets with issues: {sum(r['id'] in numbers for r in rows)}/{len(rows)}; handoffs: {sum(p.stem in numbers for p in handoffs)}/{len(handoffs)}")


def link_legacy(dry: bool) -> None:
    manifest = load(ROOT / "manifest.json")
    rows = {r["id"]: r for r in manifest["tickets"]}
    for number, (ids, names) in LEGACY.items():
        comments = gh("GET", f"repos/{REPO}/issues/{number}/comments?per_page=100")
        if any(LEGACY_MARKER in (c.get("body") or "") for c in comments):
            print(f"#{number}: already linked")
            continue
        lines = [LEGACY_MARKER, "**This work is now tracked per build-pack ticket.**", ""]
        for tid in ids:
            r = rows[tid]
            state = load(ROOT / r["asset_dir"] / "state.json")
            lines.append(f"- #{r.get('github_issue', '?')} `{tid}` {r['title']} — {state['production_status']}, "
                         f"release {state['release_status']} · [`{r['asset_dir']}/`]({URL}/tree/main/{r['asset_dir']})")
        if number in (11, 12, 13, 14, 23):
            lines += ["", "Correction: this issue was closed when only an SVG existed. The ticket is `in_progress` until its "
                          "PNG export, delivery record and QA exist."]
        if number == 26:
            lines += ["No build-pack ticket covers this Java 1.0 AWT code card (HIST-16 is a real archive screenshot, not this "
                      "card). The SVG was misfiled under XTRA-04 and now lives at the name this issue asked for."]
        lines += ["", "The file name(s) this issue promised now exist as copies (see "
                      f"[assets/LEGACY_NAMES.md]({URL}/blob/main/assets/LEGACY_NAMES.md)):"]
        lines += [f"- `{n}`" for n in names]
        print(f"#{number}: comment ({len(ids)} tickets)")
        if not dry:
            gh("POST", f"repos/{REPO}/issues/{number}/comments", {"body": "\n".join(lines)}, content=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--link-legacy", action="store_true")
    args = parser.parse_args()
    if args.link_legacy:
        link_legacy(args.dry_run)
    else:
        sync(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())

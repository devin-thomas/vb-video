"""Locate ticket folders (assets/<family>/<ID>/) through manifest.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = {r["id"]: r for r in json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["tickets"]}


def asset_dir(asset_id: str) -> Path:
    return ROOT / ROWS[asset_id]["asset_dir"]

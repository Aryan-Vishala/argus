"""
I/O utility functions for Argus.

This module contains small, reusable helpers for filesystem
operations and simple serialization. No business logic should
live here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


# -----------------------------
# Filesystem helpers
# -----------------------------

def ensure_dir(path: Path) -> None:
    """
    Ensure a directory exists.

    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# JSON helpers
# -----------------------------

def save_json(data: Dict[str, Any], path: Path) -> None:
    """
    Save a dictionary to a JSON file.

    Args:
        data: Data to save
        path: Output file path
    """
    ensure_dir(path.parent)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_json(path: Path) -> Dict[str, Any]:
    """
    Load a JSON file.

    Args:
        path: JSON file path

    Returns:
        Parsed JSON as dictionary
    """
    return json.loads(path.read_text(encoding="utf-8"))


# -----------------------------
# CSV helpers (lightweight)
# -----------------------------

def save_csv(
    rows: Iterable[Dict[str, Any]],
    path: Path,
) -> None:
    """
    Save a list of dictionaries as a CSV file.

    Keys of the first row define the header.

    Args:
        rows: Iterable of dictionaries
        path: Output CSV path
    """
    rows = list(rows)
    if not rows:
        return

    ensure_dir(path.parent)

    headers = rows[0].keys()
    lines: List[str] = [",".join(headers)]

    for row in rows:
        line = ",".join(str(row.get(h, "")) for h in headers)
        lines.append(line)

    path.write_text("\n".join(lines), encoding="utf-8")

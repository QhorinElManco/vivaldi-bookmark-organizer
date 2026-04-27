"""Shared helpers: Chrome paths, JSON I/O, tree traversal."""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from typing import Iterator


def default_chrome_bookmarks_path() -> Path:
    """Return the platform-default Chrome Default profile Bookmarks path."""
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library/Application Support/Google/Chrome/Default/Bookmarks"
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", str(home / "AppData/Local"))
        return Path(local) / "Google/Chrome/User Data/Default/Bookmarks"
    return home / ".config/google-chrome/Default/Bookmarks"


def load(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_compact(path: Path, data: dict) -> None:
    """Write Chrome-compatible compact JSON. Strips checksum so Chrome regenerates it."""
    data.pop("checksum", None)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def walk_urls(node: dict, folder_path: str = "") -> Iterator[tuple[str, dict]]:
    """Yield (folder_path, url_node) for every URL bookmark under node."""
    if not isinstance(node, dict):
        return
    t = node.get("type")
    if t == "folder":
        name = node.get("name", "")
        new_path = f"{folder_path}/{name}" if folder_path else name
        for child in node.get("children", []):
            yield from walk_urls(child, new_path)
    elif t == "url":
        yield folder_path, node


def find_folder(parent: dict, name: str) -> dict | None:
    for c in parent.get("children", []):
        if c.get("type") == "folder" and c.get("name") == name:
            return c
    return None


def resolve_path(roots: dict, path: str) -> dict | None:
    """Resolve a path like 'other/AI Tools' to a folder node. Returns None if not found."""
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    root_name = parts[0]
    if root_name not in roots:
        return None
    cur = roots[root_name]
    for part in parts[1:]:
        nxt = find_folder(cur, part)
        if nxt is None:
            return None
        cur = nxt
    return cur


def collect_max_id(node: dict, acc: list[int]) -> None:
    if isinstance(node, dict):
        v = node.get("id")
        if v is not None:
            try:
                acc.append(int(v))
            except (TypeError, ValueError):
                pass
        for c in node.get("children", []):
            collect_max_id(c, acc)


def index_by_id(data: dict) -> dict[str, tuple[dict, list]]:
    """Return {id: (node, parent_children_list)} for every node with an id."""
    out: dict[str, tuple[dict, list]] = {}

    def _walk(node: dict, parent_list: list | None) -> None:
        if not isinstance(node, dict):
            return
        nid = node.get("id")
        if nid is not None and parent_list is not None:
            out[str(nid)] = (node, parent_list)
        children = node.get("children")
        if isinstance(children, list):
            for c in children:
                _walk(c, children)

    for root_name in ("bookmark_bar", "other", "synced"):
        if root_name in data.get("roots", {}):
            _walk(data["roots"][root_name], None)
    return out

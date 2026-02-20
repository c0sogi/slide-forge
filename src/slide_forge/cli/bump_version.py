"""Bump version across pyproject.toml, plugin.json, __init__.py, and slide-forge-api.md.

Usage:
    slide-forge bump-version 1.3.0
    slide-forge bump-version 1.3.0 --root /path/to/project
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("bump-version", help="Bump version across project files")
    parser.add_argument("version", help="New version string (X.Y.Z)")
    parser.add_argument(
        "--root",
        default=None,
        help="Project root directory (default: auto-detect by searching for pyproject.toml)",
    )
    parser.set_defaults(func=_run)


def _run(args: argparse.Namespace) -> None:
    root = Path(args.root) if args.root else _find_project_root()
    if root is None:
        print("Error: Could not find project root (no pyproject.toml found)", file=sys.stderr)
        sys.exit(1)
    bump(args.version, root)


def _find_project_root() -> Path | None:
    """Walk upward from cwd to find the directory containing pyproject.toml."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return None


def _get_targets(root: Path) -> dict[str, Path]:
    return {
        "pyproject": root / "pyproject.toml",
        "plugin": root / "plugins" / "slide-forge" / ".claude-plugin" / "plugin.json",
        "init": root / "src" / "slide_forge" / "__init__.py",
        "api_doc": root / "plugins" / "slide-forge" / "skills" / "slide-anvil" / "slide-forge-api.md",
    }


def bump(version: str, root: Path) -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print(f"Error: invalid version format '{version}' (expected X.Y.Z)")
        sys.exit(1)

    targets = _get_targets(root)

    # pyproject.toml
    path = targets["pyproject"]
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'(?m)^version\s*=\s*"[^"]+"', f'version = "{version}"', text)
    path.write_text(text, encoding="utf-8")
    print(f"  Updated {path.relative_to(root)}")

    # plugin.json
    path = targets["plugin"]
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  Updated {path.relative_to(root)}")

    # __init__.py
    path = targets["init"]
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{version}"', text)
    path.write_text(text, encoding="utf-8")
    print(f"  Updated {path.relative_to(root)}")

    # slide-forge-api.md (PEP 723 dependency pins)
    path = targets["api_doc"]
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'# dependencies = \["slide-forge[^"]*"\]', f'# dependencies = ["slide-forge=={version}"]', text)
    path.write_text(text, encoding="utf-8")
    print(f"  Updated {path.relative_to(root)}")

    print(f"\nVersion bumped to {version}")

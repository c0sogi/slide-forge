"""slide-forge CLI — unified command-line interface.

Usage:
    slide-forge <command> [options]

Commands:
    render        Render PPTX slides to PNG images (Windows, requires PowerPoint)
    thumbnail     Create thumbnail grids from slides (Linux/WSL, requires LibreOffice)
    pack          Pack an unpacked directory into a PPTX file
    unpack        Unpack a PPTX file for editing
    validate      Validate PPTX XML against XSD schemas
    clean         Remove unreferenced files from an unpacked PPTX
    add-slide     Add a new slide to an unpacked PPTX directory
    bump-version  Bump version across pyproject.toml, plugin.json, and __init__.py
"""

from __future__ import annotations

import argparse
import sys

from slide_forge import __version__


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="slide-forge",
        description="slide-forge CLI tools for PowerPoint processing",
    )
    parser.add_argument("--version", action="version", version=f"slide-forge {__version__}")
    subparsers = parser.add_subparsers(dest="command", title="commands")

    # Register all subcommands
    from slide_forge.cli import add_slide, bump_version, clean, pack, render, thumbnail, unpack, validate

    render.configure_parser(subparsers)
    thumbnail.configure_parser(subparsers)
    pack.configure_parser(subparsers)
    unpack.configure_parser(subparsers)
    validate.configure_parser(subparsers)
    clean.configure_parser(subparsers)
    add_slide.configure_parser(subparsers)
    bump_version.configure_parser(subparsers)

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()

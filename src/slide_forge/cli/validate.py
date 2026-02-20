"""Validate PowerPoint document XML files against XSD schemas."""

from __future__ import annotations

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

from slide_forge.cli.validators import PPTXSchemaValidator


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("validate", help="Validate PPTX XML against XSD schemas")
    parser.add_argument("path", help="Path to unpacked directory or packed .pptx file")
    parser.add_argument(
        "--original",
        required=False,
        default=None,
        help="Path to original .pptx file. If omitted, all XSD errors are reported.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--auto-repair",
        action="store_true",
        help="Automatically repair common issues (whitespace preservation)",
    )
    parser.set_defaults(func=_run)


def _run(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    original_file = None
    if args.original:
        original_file = Path(args.original)
        if not original_file.is_file():
            print(f"Error: {original_file} is not a file", file=sys.stderr)
            sys.exit(1)
        if original_file.suffix.lower() != ".pptx":
            print(f"Error: {original_file} must be a .pptx file", file=sys.stderr)
            sys.exit(1)

    if path.is_file() and path.suffix.lower() == ".pptx":
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(temp_dir)
        unpacked_dir = Path(temp_dir)
    else:
        if not path.is_dir():
            print(f"Error: {path} is not a directory or .pptx file", file=sys.stderr)
            sys.exit(1)
        unpacked_dir = path

    validators = [
        PPTXSchemaValidator(unpacked_dir, original_file, verbose=args.verbose),
    ]

    if args.auto_repair:
        total_repairs = sum(v.repair() for v in validators)
        if total_repairs:
            print(f"Auto-repaired {total_repairs} issue(s)")

    success = all(v.validate() for v in validators)

    if success:
        print("All validations PASSED!")

    sys.exit(0 if success else 1)

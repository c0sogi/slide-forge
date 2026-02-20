"""
Command line tool to validate PowerPoint document XML files against XSD schemas.

Usage:
    python validate.py <path> [--original <original_file>] [--auto-repair]

The first argument can be either:
- An unpacked directory containing the PPTX XML files
- A packed .pptx file which will be unpacked to a temp directory

Auto-repair fixes:
- Missing xml:space="preserve" on text elements with whitespace
"""

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

from validators import PPTXSchemaValidator


def main():
    parser = argparse.ArgumentParser(description="Validate PowerPoint document XML files")
    parser.add_argument(
        "path",
        help="Path to unpacked directory or packed .pptx file",
    )
    parser.add_argument(
        "--original",
        required=False,
        default=None,
        help="Path to original .pptx file. If omitted, all XSD errors are reported.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--auto-repair",
        action="store_true",
        help="Automatically repair common issues (whitespace preservation)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    assert path.exists(), f"Error: {path} does not exist"

    original_file = None
    if args.original:
        original_file = Path(args.original)
        assert original_file.is_file(), f"Error: {original_file} is not a file"
        assert original_file.suffix.lower() == ".pptx", f"Error: {original_file} must be a .pptx file"

    if path.is_file() and path.suffix.lower() == ".pptx":
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(temp_dir)
        unpacked_dir = Path(temp_dir)
    else:
        assert path.is_dir(), f"Error: {path} is not a directory or .pptx file"
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


if __name__ == "__main__":
    main()

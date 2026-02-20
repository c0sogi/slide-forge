"""Render PPTX slides to individual PNG images for visual QA.

Uses MS PowerPoint COM automation (PPTX -> PDF) + PyMuPDF (PDF -> PNG).
Requires: pip install pywin32 pymupdf
"""

from __future__ import annotations

import argparse
import os
import sys


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("render", help="Render PPTX slides to PNG images (Windows only)")
    parser.add_argument("pptx", help="Path to the .pptx file")
    parser.add_argument("output_dir", nargs="?", help="Output directory (default: <name>_slides/)")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (default: 150)")
    parser.set_defaults(func=_run)


def _run(args: argparse.Namespace) -> None:
    render(args.pptx, args.output_dir, args.dpi)


def _check_dependencies() -> None:
    missing = []
    try:
        import win32com.client  # noqa: F401
    except ImportError:
        missing.append("pywin32")
    try:
        import fitz  # noqa: F401
    except ImportError:
        missing.append("pymupdf")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)


def _pptx_to_pdf(pptx_path: str, pdf_path: str) -> None:
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    try:
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        abs_pptx = os.path.abspath(pptx_path)
        abs_pdf = os.path.abspath(pdf_path)
        presentation = powerpoint.Presentations.Open(abs_pptx, WithWindow=False)
        presentation.SaveAs(abs_pdf, 32)  # 32 = ppSaveAsPDF
        presentation.Close()
        powerpoint.Quit()
    finally:
        pythoncom.CoUninitialize()


def _pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    import fitz

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        img_path = os.path.join(output_dir, f"slide-{i + 1:02d}.png")
        pix.save(img_path)
        paths.append(img_path)
    doc.close()
    return paths


def render(pptx_path: str, output_dir: str | None = None, dpi: int = 150) -> list[str]:
    """Full pipeline: PPTX -> PDF -> PNG images.

    Args:
        pptx_path: Path to the .pptx file
        output_dir: Directory for output images (default: same dir as pptx)
        dpi: Resolution for rendered images (default: 150)

    Returns:
        List of paths to generated PNG images
    """
    _check_dependencies()

    if not os.path.exists(pptx_path):
        print(f"File not found: {pptx_path}")
        sys.exit(1)

    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(pptx_path) or ".",
            os.path.splitext(os.path.basename(pptx_path))[0] + "_slides",
        )

    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "render.pdf")

    print(f"PPTX -> PDF: {pptx_path}")
    _pptx_to_pdf(pptx_path, pdf_path)

    print(f"PDF -> PNG ({dpi} DPI): {pdf_path}")
    images = _pdf_to_images(pdf_path, output_dir, dpi)

    try:
        os.remove(pdf_path)
    except OSError:
        pass

    print(f"Rendered {len(images)} slides to {output_dir}/")
    for img in images:
        print(f"  {os.path.basename(img)}")
    return images

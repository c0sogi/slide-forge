#!/usr/bin/env python3
"""
Render PPTX slides to individual PNG images for visual QA.

Uses MS PowerPoint COM automation (PPTX -> PDF) + PyMuPDF (PDF -> PNG).
Requires: uv add pywin32 pymupdf

Usage:
    uv run python scripts/render_slides.py <input.pptx> [output_dir] [--dpi N]

Examples:
    uv run python scripts/render_slides.py output.pptx
    uv run python scripts/render_slides.py output.pptx ./slides --dpi 200

Output:
    slide-01.png, slide-02.png, ... in the output directory.
    Also creates a temporary PDF in the output directory.
"""

import argparse
import os
import sys
import tempfile


def check_dependencies():
    """Verify required packages are available."""
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
        print(f"Install with: uv add {' '.join(missing)}")
        sys.exit(1)


def pptx_to_pdf(pptx_path: str, pdf_path: str) -> None:
    """Convert PPTX to PDF using MS PowerPoint COM automation."""
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


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    """Convert PDF pages to PNG images using PyMuPDF."""
    import fitz

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc):
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
    check_dependencies()

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
    pptx_to_pdf(pptx_path, pdf_path)

    print(f"PDF -> PNG ({dpi} DPI): {pdf_path}")
    images = pdf_to_images(pdf_path, output_dir, dpi)

    # Clean up temporary PDF
    try:
        os.remove(pdf_path)
    except OSError:
        pass

    print(f"Rendered {len(images)} slides to {output_dir}/")
    for img in images:
        print(f"  {os.path.basename(img)}")
    return images


def main():
    parser = argparse.ArgumentParser(description="Render PPTX slides to PNG images")
    parser.add_argument("pptx", help="Path to the .pptx file")
    parser.add_argument("output_dir", nargs="?", help="Output directory (default: <name>_slides/)")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (default: 150)")
    args = parser.parse_args()
    render(args.pptx, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()

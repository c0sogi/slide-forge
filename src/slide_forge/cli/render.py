"""Render PPTX slides to individual PNG images for visual QA.

Windows: PowerPoint COM automation (PPTX -> PDF) + PyMuPDF (PDF -> PNG).
macOS/Linux: LibreOffice headless (PPTX -> PDF) + PyMuPDF (PDF -> PNG).
"""

from __future__ import annotations

import argparse
import os
import sys


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("render", help="Render PPTX slides to PNG images")
    parser.add_argument("pptx", help="Path to the .pptx file")
    parser.add_argument("output_dir", nargs="?", help="Output directory (default: <name>_slides/)")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (default: 150)")
    parser.set_defaults(func=_run)


def _run(args: argparse.Namespace) -> None:
    render(args.pptx, args.output_dir, args.dpi)


def _check_dependencies() -> None:
    if sys.platform != "win32":
        import shutil

        if not shutil.which("soffice"):
            print("LibreOffice is required for rendering on this platform.")
            print("Install: https://www.libreoffice.org/download/")
            sys.exit(1)


def _pptx_to_pdf(pptx_path: str, pdf_path: str) -> None:
    if sys.platform == "win32":
        _pptx_to_pdf_windows(pptx_path, pdf_path)
    else:
        _pptx_to_pdf_soffice(pptx_path, pdf_path)


def _pptx_to_pdf_windows(pptx_path: str, pdf_path: str) -> None:
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


def _pptx_to_pdf_soffice(pptx_path: str, pdf_path: str) -> None:
    from slide_forge.cli.soffice import run_soffice

    abs_pptx = os.path.abspath(pptx_path)
    output_dir = os.path.dirname(os.path.abspath(pdf_path))
    result = run_soffice(
        ["--headless", "--convert-to", "pdf", "--outdir", output_dir, abs_pptx],
        capture_output=True,
    )
    # soffice outputs <stem>.pdf
    stem = os.path.splitext(os.path.basename(abs_pptx))[0]
    soffice_pdf = os.path.join(output_dir, f"{stem}.pdf")

    if result.returncode != 0 or not os.path.exists(soffice_pdf):
        stderr = result.stderr.decode(errors="replace").strip() if result.stderr else ""
        raise RuntimeError(f"LibreOffice PDF conversion failed (exit {result.returncode}):\n{stderr}")

    if os.path.normcase(soffice_pdf) != os.path.normcase(os.path.abspath(pdf_path)):
        os.replace(soffice_pdf, pdf_path)


def _pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    import pymupdf

    os.makedirs(output_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
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

import re

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.presentation import Presentation
from pptx.slide import Slide
from pptx.text.text import TextFrame, _Paragraph
from pptx.util import Emu, Length, Pt

# ── Default fonts ─────────────────────────────────────────────
FONT_ASCII = "Arial"
FONT_EA = "HY\uacac\uace0\ub515"  # HY견고딕

# ── Layout / Master indices ───────────────────────────────────
_BLANK_LAYOUT_NAME = "\ube48 \ud654\uba74"  # 빈 화면
_COVER_MASTER_IDX = 0  # Master 0: full background image (앞/뒤 표지)
_CONTENT_MASTER_IDX = 1  # Master 1: header lines + logos (내용)

# ── Slide title ───────────────────────────────────────────────
_TITLE_LEFT = Emu(179512)
_TITLE_TOP = Emu(154732)
_TITLE_WIDTH = Emu(8352928)
_TITLE_HEIGHT = Emu(461665)
_TITLE_SIZE = Pt(24)
_TITLE_COLOR = RGBColor(0x07, 0x2A, 0x5E)

# ── Content text box ─────────────────────────────────────────
_CONTENT_LEFT = Emu(166261)
_CONTENT_TOP = Emu(724090)
_CONTENT_WIDTH = Emu(8870234)
_CONTENT_HEIGHT = Emu(3599447)

# ── Line spacing (130 %) ─────────────────────────────────────
_LINE_SPACING_PCT = 130000

# ── Section header (▌) ──────────────────────────────────────
_SECTION_SIZE = Pt(18)
_SECTION_COLOR = RGBColor(0x40, 0x40, 0x40)

# ── Level-0 bullet: "-" in HY견고딕 ─────────────────────────
_L0_MARL = "266700"
_L0_INDENT = "-174625"
_L0_BU_CHAR = "-"
_L0_BU_FONT = FONT_EA
_L0_BU_PITCH = "18"
_L0_BU_CHARSET = "-127"
_L0_SIZE = Pt(14)
_L0_COLOR = RGBColor(0x40, 0x40, 0x40)

# ── Level-1 bullet: "Ø" in Wingdings ────────────────────────
_L1_MARL = "449263"
_L1_INDENT = "-182563"
_L1_BU_CHAR = "\u00d8"  # Ø rendered by Wingdings
_L1_BU_FONT = "Wingdings"
_L1_BU_PITCH = "2"
_L1_BU_CHARSET = "2"
_L1_SIZE = Pt(12)
_L1_COLOR = RGBColor(0x40, 0x40, 0x40)

# ── Caption ──────────────────────────────────────────────────
_CAPTION_SIZE = Emu(133350)  # ≈ 10.5 pt

# ── Inline color tags ────────────────────────────────────────
_COLOR_TAG_RE = re.compile(r"\[(#[0-9A-Fa-f]{6}|\w+)\](.*?)\[/\1\]")

_COLOR_MAP: dict[str, RGBColor] = {
    "red": RGBColor(0xC0, 0x00, 0x00),
    "green": RGBColor(0x00, 0x80, 0x00),
    "blue": RGBColor(0x00, 0x70, 0xC0),
    "orange": RGBColor(0xFF, 0x7F, 0x00),
    "purple": RGBColor(0x80, 0x00, 0x80),
    "navy": RGBColor(0x07, 0x2A, 0x5E),
    "teal": RGBColor(0x00, 0x80, 0x80),
    "gray": RGBColor(0x80, 0x80, 0x80),
    "grey": RGBColor(0x80, 0x80, 0x80),
}


# ─── internal helpers ────────────────────────────────────────


def _resolve_color(name: str) -> RGBColor | None:
    """Resolve a color name or ``#RRGGBB`` hex code to :class:`RGBColor`."""
    if name.startswith("#") and len(name) == 7:
        try:
            return RGBColor(int(name[1:3], 16), int(name[3:5], 16), int(name[5:7], 16))
        except ValueError:
            return None
    return _COLOR_MAP.get(name.lower())


def _parse_color_tags(text: str) -> list[tuple[str, RGBColor | None]]:
    """Parse ``[color]text[/color]`` inline markup.

    Returns ``[(text, color_override), ...]``.
    *color_override* is ``None`` for untagged portions.
    Unknown color names are left as literal text (tags preserved).
    """
    segments: list[tuple[str, RGBColor | None]] = []
    last_end = 0
    for m in _COLOR_TAG_RE.finditer(text):
        color = _resolve_color(m.group(1))
        if color is None:
            continue  # unknown color — keep tags as literal text
        if m.start() > last_end:
            segments.append((text[last_end : m.start()], None))
        segments.append((m.group(2), color))
        last_end = m.end()
    if last_end < len(text):
        segments.append((text[last_end:], None))
    if not segments:
        segments.append((text, None))
    return segments


def _is_ascii(ch: str) -> bool:
    return bool(ch) and ord(ch) < 128


def _split_by_script(text: str) -> list[tuple[str, bool]]:
    """Split *text* into ``(segment, is_ascii)`` chunks.

    Whitespace is kept with the preceding chunk so that run boundaries
    don't land on spaces.
    """
    if not text:
        return []

    chunks: list[tuple[str, bool]] = []
    buf: list[str] = [text[0]]
    cur = _is_ascii(text[0])

    for ch in text[1:]:
        if ch.isspace():
            buf.append(ch)
            continue
        a = _is_ascii(ch)
        if a == cur:
            buf.append(ch)
        else:
            chunks.append(("".join(buf), cur))
            buf = [ch]
            cur = a

    chunks.append(("".join(buf), cur))
    return chunks


def _set_ea_font(run, typeface: str = FONT_EA) -> None:
    """Append ``<a:ea typeface="…"/>`` to a run's ``rPr``."""
    rPr = run._r.get_or_add_rPr()
    for existing in rPr.findall(qn("a:ea")):
        rPr.remove(existing)
    ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", typeface)


def _set_line_spacing(pPr, pct: int = _LINE_SPACING_PCT) -> None:
    lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
    spcPct = etree.SubElement(lnSpc, qn("a:spcPct"))
    spcPct.set("val", str(pct))


def _set_bullet(
    pPr,
    char: str,
    typeface: str,
    pitch: str,
    charset: str,
) -> None:
    buFont = etree.SubElement(pPr, qn("a:buFont"))
    buFont.set("typeface", typeface)
    buFont.set("pitchFamily", pitch)
    buFont.set("charset", charset)
    buChar = etree.SubElement(pPr, qn("a:buChar"))
    buChar.set("char", char)


def _add_runs(
    p: _Paragraph,
    text: str,
    *,
    size: Length,
    color: RGBColor,
    ascii_font: str = FONT_ASCII,
    ea_font: str = FONT_EA,
    ascii_bold: bool = True,
    unicode_bold: bool = False,
) -> None:
    """Add mixed-font runs to *p*, splitting on ASCII / non-ASCII.

    Supports ``[color]text[/color]`` inline markup for per-span color
    overrides.  Named colors (``red``, ``green``, …) and hex codes
    (``#RRGGBB``) are both accepted.
    """
    for seg_text, color_override in _parse_color_tags(text):
        effective_color = color_override if color_override is not None else color
        for chunk, is_ascii in _split_by_script(seg_text):
            run = p.add_run()
            run.text = chunk
            run.font.name = ascii_font if is_ascii else ea_font
            run.font.bold = ascii_bold if is_ascii else unicode_bold
            run.font.size = size
            run.font.color.rgb = effective_color
            _set_ea_font(run, ea_font)


def _next_para(tf: TextFrame) -> _Paragraph:
    """Re-use the empty first paragraph or append a new one."""
    paras = tf.paragraphs
    if len(paras) == 1 and not paras[0].text and not paras[0].runs:
        return paras[0]
    return tf.add_paragraph()


# ─── internal: layout lookup ─────────────────────────────────


def _get_blank_layout(prs: Presentation, master_idx: int):
    """Return the '빈 화면' layout from a specific slide master."""
    master = prs.slide_masters[master_idx]
    for layout in master.slide_layouts:
        if layout.name == _BLANK_LAYOUT_NAME:
            return layout
    raise ValueError(f"Layout '{_BLANK_LAYOUT_NAME}' not found in master {master_idx}")


# ─── public API ──────────────────────────────────────────────


def create_slide(prs: Presentation) -> Slide:
    """Add a **content** slide (Master 1: header lines + logos)."""
    return prs.slides.add_slide(_get_blank_layout(prs, _CONTENT_MASTER_IDX))


def create_cover_slide(prs: Presentation) -> Slide:
    """Add a **cover** slide (Master 0: full background image, 앞/뒤 표지)."""
    return prs.slides.add_slide(_get_blank_layout(prs, _COVER_MASTER_IDX))


def add_slide_title(
    slide: Slide,
    text: str,
    *,
    left: Length = _TITLE_LEFT,
    top: Length = _TITLE_TOP,
    width: Length = _TITLE_WIDTH,
    height: Length = _TITLE_HEIGHT,
    font_size: Length = _TITLE_SIZE,
    color: RGBColor = _TITLE_COLOR,
) -> None:
    """Add the top-of-slide title text box."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    _add_runs(p, text, size=font_size, color=color)


def add_content_box(
    slide: Slide,
    *,
    left: Length = _CONTENT_LEFT,
    top: Length = _CONTENT_TOP,
    width: Length = _CONTENT_WIDTH,
    height: Length = _CONTENT_HEIGHT,
) -> TextFrame:
    """Create the main content area and return its :class:`TextFrame`.

    Pass the returned object to :func:`add_section`, :func:`add_bullet`,
    and :func:`add_spacer` to populate the slide.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.clear()
    return tf


def add_section(
    tf: TextFrame,
    title: str,
    *,
    font_size: Length = _SECTION_SIZE,
    color: RGBColor = _SECTION_COLOR,
) -> _Paragraph:
    """Add a **▌Section Header** paragraph."""
    p = _next_para(tf)
    pPr = p._element.get_or_add_pPr()
    pPr.set("eaLnBrk", "1")
    pPr.set("hangingPunct", "1")
    _set_line_spacing(pPr, _LINE_SPACING_PCT)
    _add_runs(p, "\u258c" + title, size=font_size, color=color)
    return p


def add_bullet(
    tf: TextFrame,
    text: str,
    *,
    level: int = 0,
    font_size: Length | None = None,
    color: RGBColor | None = None,
) -> _Paragraph:
    """Add a bullet paragraph.

    Parameters
    ----------
    level : int
        ``0`` for dash ``-`` (HY견고딕),
        ``1`` for arrow ``Ø`` (Wingdings).
    color : RGBColor, optional
        Override the default ``#404040``.
    """
    if level == 0:
        marl, indent = _L0_MARL, _L0_INDENT
        bu_char, bu_font = _L0_BU_CHAR, _L0_BU_FONT
        bu_pitch, bu_charset = _L0_BU_PITCH, _L0_BU_CHARSET
        sz = font_size or _L0_SIZE
        clr = color or _L0_COLOR
    else:
        marl, indent = _L1_MARL, _L1_INDENT
        bu_char, bu_font = _L1_BU_CHAR, _L1_BU_FONT
        bu_pitch, bu_charset = _L1_BU_PITCH, _L1_BU_CHARSET
        sz = font_size or _L1_SIZE
        clr = color or _L1_COLOR

    p = _next_para(tf)
    pPr = p._element.get_or_add_pPr()
    pPr.set("marL", marl)
    pPr.set("indent", indent)
    pPr.set("eaLnBrk", "1")
    pPr.set("hangingPunct", "1")
    _set_line_spacing(pPr, _LINE_SPACING_PCT)
    _set_bullet(pPr, bu_char, bu_font, bu_pitch, bu_charset)
    _add_runs(p, text, size=sz, color=clr)
    return p


def add_spacer(tf: TextFrame) -> _Paragraph:
    """Add an empty separator line."""
    p = _next_para(tf)
    pPr = p._element.get_or_add_pPr()
    pPr.set("marL", _L0_MARL)
    _set_line_spacing(pPr, _LINE_SPACING_PCT)
    return p


def add_caption(
    slide: Slide,
    text: str,
    *,
    left: Length,
    top: Length,
    width: Length,
    height: Length,
    font_size: Length = _CAPTION_SIZE,
    color: RGBColor | None = None,
) -> None:
    """Add a small caption text box (typically under a figure)."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    clr = color or RGBColor(0x00, 0x00, 0x00)
    _add_runs(p, text, size=font_size, color=clr)

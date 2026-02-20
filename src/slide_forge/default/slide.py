import re

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.presentation import Presentation
from pptx.slide import Slide
from pptx.text.text import TextFrame, _Paragraph
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Length, Pt

# ── Default fonts ─────────────────────────────────────────────
FONT_ASCII = "Arial"
FONT_EA = "HY\uacac\uace0\ub515"  # HY견고딕

# ── Layout / Master indices ───────────────────────────────────
_BLANK_LAYOUT_NAME = "\ube48 \ud654\uba74"  # 빈 화면
_COVER_MASTER_IDX = 0  # Master 0: full background image (앞/뒤 표지)
_CONTENT_MASTER_IDX = 1  # Master 1: header lines + logos (내용)

# ── Slide type tag ───────────────────────────────────────────
_SLIDE_TYPE_ATTR = "_slide_forge_type"
_COVER = "cover"
_CONTENT = "content"

# ── Cover slide ──────────────────────────────────────────────
_COVER_TITLE_LEFT = Emu(561257)
_COVER_TITLE_TOP = Emu(2636912)
_COVER_TITLE_WIDTH = Emu(8010140)
_COVER_TITLE_HEIGHT = Emu(1186800)
_COVER_TITLE_SIZE = Pt(20)
_COVER_COLOR = RGBColor(0x00, 0x20, 0x60)

_COVER_INFO_LEFT = Emu(3242805)
_COVER_INFO_TOP = Emu(5229200)
_COVER_INFO_WIDTH = Emu(5328592)
_COVER_INFO_HEIGHT = Emu(696857)
_COVER_INFO_SIZE = Pt(14)

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

# ── Bullet margin ────────────────────────────────────────────
_MARGIN_BASE = 266700
_MARGIN_STEP = 182563  # per-level increment

# ── Per-level defaults ───────────────────────────────────────
_L0_INDENT = "-174625"
_L0_SIZE = Pt(14)
_L0_COLOR = RGBColor(0x40, 0x40, 0x40)

_L1_INDENT = "-182563"
_L1_SIZE = Pt(12)
_L1_COLOR = RGBColor(0x40, 0x40, 0x40)

# ── Bullet styles ────────────────────────────────────────────
_BULLET_STYLES: dict[str, dict[str, str]] = {
    "dash": {"char": "-", "font": FONT_EA, "pitch": "18", "charset": "-127"},
    "arrow": {"char": "\u00d8", "font": "Wingdings", "pitch": "2", "charset": "2"},
    "square": {"char": "n", "font": "Wingdings", "pitch": "2", "charset": "2"},
    "circle": {"char": "l", "font": "Wingdings", "pitch": "2", "charset": "2"},
    "check": {"char": "\u00fc", "font": "Wingdings", "pitch": "2", "charset": "2"},
}

_DEFAULT_BULLET = {0: "dash", 1: "arrow", 2: "square", 3: "circle", 4: "check"}

# ── Caption ──────────────────────────────────────────────────
_CAPTION_SIZE = Emu(133350)  # ≈ 10.5 pt

# ── Inline color tags ────────────────────────────────────────
_COLOR_TAG_RE = re.compile(r"\[(#[0-9A-Fa-f]{6}|\w+)\](.*?)\[/\1\]")

_COLOR_MAP: dict[str, RGBColor] = {
    "red": RGBColor(0xC0, 0x00, 0x00),
    "green": RGBColor(0x00, 0xB0, 0x50),
    "blue": RGBColor(0x00, 0x70, 0xC0),
    "orange": RGBColor(0xFF, 0x7F, 0x00),
    "purple": RGBColor(0x70, 0x30, 0xA0),
    "navy": RGBColor(0x07, 0x2A, 0x5E),
    "teal": RGBColor(0x00, 0x80, 0x80),
    "gray": RGBColor(0x80, 0x80, 0x80),
    "grey": RGBColor(0x80, 0x80, 0x80),
}

# ── Arrow token ──────────────────────────────────────────────
_ARROW_CHAR = "\uf0e0"  # Wingdings right arrow (→)


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


def _set_sym_font(run, typeface: str = "Wingdings") -> None:
    """Append ``<a:sym typeface="…"/>`` so ``\\uf0e0`` renders as →."""
    rPr = run._r.get_or_add_rPr()
    for existing in rPr.findall(qn("a:sym")):
        rPr.remove(existing)
    sym = etree.SubElement(rPr, qn("a:sym"))
    sym.set("typeface", typeface)
    sym.set("pitchFamily", "2")
    sym.set("charset", "2")


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


def _set_auto_number(pPr, num_type: str = "arabicPeriod") -> None:
    """Add ``<a:buAutoNum type="…"/>`` for numbered bullets."""
    buAutoNum = etree.SubElement(pPr, qn("a:buAutoNum"))
    buAutoNum.set("type", num_type)


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

    ``->`` is automatically replaced with the Wingdings right-arrow
    token (``\\uf0e0``).
    """
    text = text.replace("->", _ARROW_CHAR)
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
            if _ARROW_CHAR in chunk:
                _set_sym_font(run)


def _next_para(tf: TextFrame) -> _Paragraph:
    """Re-use the empty first paragraph or append a new one."""
    paras = tf.paragraphs
    if len(paras) == 1 and not paras[0].text and not paras[0].runs:
        return paras[0]
    return tf.add_paragraph()


# ─── internal: slide type validation ─────────────────────────


def _require(slide: Slide, expected: str) -> None:
    """Raise :class:`TypeError` if *slide* is not the expected type."""
    actual = getattr(slide, _SLIDE_TYPE_ATTR, None)
    if actual is None:
        raise TypeError(
            "이 슬라이드는 create_slide() 또는 create_cover_slide()로 "
            "생성되지 않았습니다."
        )
    if actual == expected:
        return
    if expected == _COVER:
        raise TypeError(
            "이 함수는 표지 슬라이드(create_cover_slide)에서만 사용할 수 있습니다.\n"
            "  내용 슬라이드 → add_slide_title(), add_content_box() 등을 사용하세요."
        )
    raise TypeError(
        "이 함수는 내용 슬라이드(create_slide)에서만 사용할 수 있습니다.\n"
        "  표지 슬라이드 → add_cover_title(), add_cover_info()를 사용하세요."
    )


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
    slide = prs.slides.add_slide(_get_blank_layout(prs, _CONTENT_MASTER_IDX))
    setattr(slide, _SLIDE_TYPE_ATTR, _CONTENT)
    return slide


def create_cover_slide(prs: Presentation) -> Slide:
    """Add a **cover** slide (Master 0: full background image, 앞/뒤 표지)."""
    slide = prs.slides.add_slide(_get_blank_layout(prs, _COVER_MASTER_IDX))
    setattr(slide, _SLIDE_TYPE_ATTR, _COVER)
    return slide


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
    """Add the top-of-slide title text box (content slides only)."""
    _require(slide, _CONTENT)
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
    """Create the main content area and return its :class:`TextFrame`
    (content slides only).

    Pass the returned object to :func:`add_section`, :func:`add_bullet`,
    and :func:`add_spacer` to populate the slide.
    """
    _require(slide, _CONTENT)
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
    bullet: str | None = None,
    font_size: Length | None = None,
    color: RGBColor | None = None,
) -> _Paragraph:
    """Add a bullet paragraph.

    Parameters
    ----------
    level : int
        Indentation depth.  ``0`` is top-level, ``1+`` is nested.
        Margin increases by ``_MARGIN_STEP`` per level.
    bullet : str, optional
        Bullet style name.  Built-in styles:

        * ``"dash"``   — ``-`` (HY견고딕)  *default for level 0*
        * ``"arrow"``  — ``Ø`` → (Wingdings)  *default for level 1*
        * ``"square"`` — ``■`` (Wingdings)  *default for level 2*
        * ``"circle"`` — ``●`` (Wingdings)  *default for level 3*
        * ``"check"``  — ``✓`` (Wingdings)  *default for level 4+*
        * ``"number"`` — auto-numbered (1. 2. 3.)
        * ``"none"``   — no bullet marker

        If *None*, defaults to ``"dash"`` for level 0 and ``"arrow"``
        otherwise.
    color : RGBColor, optional
        Override the default ``#404040``.
    """
    if bullet is None:
        bullet = _DEFAULT_BULLET.get(level, "check")

    indent = _L0_INDENT if level == 0 else _L1_INDENT
    sz = font_size or (_L0_SIZE if level == 0 else _L1_SIZE)
    clr = color or (_L0_COLOR if level == 0 else _L1_COLOR)
    marl = str(_MARGIN_BASE + level * _MARGIN_STEP)

    p = _next_para(tf)
    pPr = p._element.get_or_add_pPr()
    pPr.set("marL", marl)
    pPr.set("indent", indent)
    pPr.set("eaLnBrk", "1")
    pPr.set("hangingPunct", "1")
    _set_line_spacing(pPr, _LINE_SPACING_PCT)

    if bullet == "number":
        _set_auto_number(pPr)
    elif bullet != "none" and bullet in _BULLET_STYLES:
        s = _BULLET_STYLES[bullet]
        _set_bullet(pPr, s["char"], s["font"], s["pitch"], s["charset"])

    _add_runs(p, text, size=sz, color=clr)
    return p


def add_spacer(tf: TextFrame) -> _Paragraph:
    """Add an empty separator line."""
    p = _next_para(tf)
    pPr = p._element.get_or_add_pPr()
    pPr.set("marL", str(_MARGIN_BASE))
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


# ─── cover slide helpers ─────────────────────────────────────


def _set_cover_pPr(pPr, *, spc_before: int = 0) -> None:
    """Apply ground-truth paragraph properties for cover shapes."""
    pPr.set("marL", "0")
    pPr.set("marR", "0")
    pPr.set("indent", "0")
    pPr.set("eaLnBrk", "1")
    pPr.set("fontAlgn", "base")
    pPr.set("latinLnBrk", "1")
    pPr.set("hangingPunct", "1")
    # 150 % line spacing
    lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
    etree.SubElement(lnSpc, qn("a:spcPct")).set("val", "150000")
    # space before
    spcBef = etree.SubElement(pPr, qn("a:spcBef"))
    etree.SubElement(spcBef, qn("a:spcPct")).set("val", str(spc_before))
    # space after = 0
    spcAft = etree.SubElement(pPr, qn("a:spcAft"))
    etree.SubElement(spcAft, qn("a:spcPct")).set("val", "0")
    # no bullet
    etree.SubElement(pPr, qn("a:buNone"))


# ─── cover slide API ────────────────────────────────────────


def add_cover_title(
    slide: Slide,
    text: str,
    *,
    left: Length = _COVER_TITLE_LEFT,
    top: Length = _COVER_TITLE_TOP,
    width: Length = _COVER_TITLE_WIDTH,
    height: Length = _COVER_TITLE_HEIGHT,
    font_size: Length = _COVER_TITLE_SIZE,
    color: RGBColor = _COVER_COLOR,
) -> None:
    """Add the centred presentation title (cover slides only).

    Use ``\\n`` in *text* for line breaks.  Any number of consecutive
    newlines is normalised to exactly **two** soft returns so the
    visual gap is always consistent.
    """
    _require(slide, _COVER)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    # match ground-truth: auto-fit + word-wrap
    bodyPr = tf._txBody.find(qn("a:bodyPr"))
    bodyPr.set("wrap", "square")
    for old in bodyPr.findall(qn("a:spAutoFit")) + bodyPr.findall(qn("a:noAutofit")):
        bodyPr.remove(old)
    etree.SubElement(bodyPr, qn("a:spAutoFit"))
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    pPr = p._element.get_or_add_pPr()
    _set_cover_pPr(pPr, spc_before=50000)
    parts = [s for s in re.split(r"\n+", text) if s]
    for i, part in enumerate(parts):
        if i > 0:
            sz_full = str(int(font_size) // 127)   # EMU → hundredths-of-pt
            sz_half = str(int(font_size) // 254)    # half-size for tighter gap
            for sz_val in (sz_full, sz_half):
                br = etree.SubElement(p._element, qn("a:br"))
                brPr = etree.SubElement(br, qn("a:rPr"))
                brPr.set("lang", "en-US")
                brPr.set("sz", sz_val)
        _add_runs(p, part, size=font_size, color=color)


def add_cover_info(
    slide: Slide,
    date: str,
    presenter: str,
    *,
    left: Length = _COVER_INFO_LEFT,
    top: Length = _COVER_INFO_TOP,
    width: Length = _COVER_INFO_WIDTH,
    height: Length = _COVER_INFO_HEIGHT,
    font_size: Length = _COVER_INFO_SIZE,
    color: RGBColor = _COVER_COLOR,
) -> None:
    """Add date and presenter info (cover slides only)."""
    _require(slide, _COVER)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    bodyPr = tf._txBody.find(qn("a:bodyPr"))
    bodyPr.set("wrap", "square")
    for old in bodyPr.findall(qn("a:spAutoFit")) + bodyPr.findall(qn("a:noAutofit")):
        bodyPr.remove(old)
    etree.SubElement(bodyPr, qn("a:spAutoFit"))
    tf.clear()

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    _set_cover_pPr(p._element.get_or_add_pPr())
    _add_runs(p, f"날짜 : {date}", size=font_size, color=color)

    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.RIGHT
    _set_cover_pPr(p._element.get_or_add_pPr())
    _add_runs(p, f"발표자 : {presenter}", size=font_size, color=color)

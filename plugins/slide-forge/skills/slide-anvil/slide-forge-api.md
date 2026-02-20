# slide-forge Python API Reference

## Running slide-forge

slide-forge is a Python library. Write a `.py` file with **PEP 723 inline metadata** and run it with `uv run`:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["slide-forge"]
#
# [tool.uv.sources]
# slide-forge = { path = "../../" }
# ///

from slide_forge import (
    get_presentation, create_slide, create_cover_slide,
    add_slide_title, add_content_box,
    add_section, add_bullet, add_spacer,
    add_shape, add_line,
)
from slide_forge.default.slide import add_table, add_chart, add_figure, add_cover_title, add_cover_info

prs = get_presentation()

# ... build slides ...

prs.save("output.pptx")
```

```bash
# Run the script (uv resolves dependencies automatically)
uv run create_slides.py
```

The script uses the built-in Slide Forge template (`template.pptx`) which provides two slide masters:
- **Master 0** (cover): full background image for front/back covers
- **Master 1** (content): header lines + logos for content slides

---

## Basic Structure

### get_presentation()

Returns a `Presentation` object loaded from the built-in Slide Forge template.

```python
prs = get_presentation()
```

### create_slide(prs)

Add a **content** slide (Master 1: header lines + logos).

```python
slide = create_slide(prs)
```

### create_cover_slide(prs)

Add a **cover** slide (Master 0: full background image).

```python
slide = create_cover_slide(prs)
```

---

## Cover Slide

> **Note:** Slide Forge standard style does not use cover slides (see [rules.md](../../references/rules.md)). These functions are available for custom use cases outside the standard workflow.

Cover slides use dedicated functions. Do **not** mix cover and content functions on the same slide.

### add_cover_title(slide, text)

Add the centred presentation title. Use `\n` for line breaks.

```python
cover = create_cover_slide(prs)
add_cover_title(cover, "로봇 역동역학 기반\n이상 모사 모델 개발")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | required | Title text (`\n` for line breaks) |
| `left` | int | 561257 | Left position (EMU) |
| `top` | int | 2636912 | Top position (EMU) |
| `width` | int | 8010140 | Width (EMU) |
| `height` | int | 1186800 | Height (EMU) |
| `font_size` | int | 20 | Font size (pt) |
| `color` | Color | "002060" | Text colour |

### add_cover_info(slide, date, presenter)

Add date and presenter info (right-aligned).

```python
add_cover_info(cover, "2025.06.20", "홍길동")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `date` | str | required | Date string |
| `presenter` | str | required | Presenter name |
| `font_size` | int | 14 | Font size (pt) |
| `color` | Color | "002060" | Text colour |

---

## Content Slide

### add_slide_title(slide, text)

Add the top-of-slide title text box. Content slides only.

```python
slide = create_slide(prs)
add_slide_title(slide, "MCD 기반 이상 탐지 성능 평가")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | required | Title text |
| `font_size` | int | 24 | Font size (pt) |
| `color` | Color | "072A5E" | Text colour |
| `left`, `top`, `width`, `height` | int | (preset) | Position/size (EMU) |

### add_content_box(slide)

Create the main content area and return its `TextFrame`. Pass this to `add_section()`, `add_bullet()`, and `add_spacer()`.

```python
tf = add_content_box(slide)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `left` | int | 166261 | Left position (EMU) |
| `top` | int | 724090 | Top position (EMU) |
| `width` | int | 8870234 | Width (EMU) |
| `height` | int | 3599447 | Height (EMU) |

**Returns:** `TextFrame` — pass to `add_section`, `add_bullet`, `add_spacer`.

### add_section(tf, title)

Add a **▌Section Header** paragraph (the subtitle bar).

```python
add_section(tf, "SOTA 방법론 탐색 및 학습")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | required | Section header text (▌ is auto-prepended) |
| `font_size` | int | 18 | Font size (pt) |
| `color` | Color | "404040" | Text colour |

### add_bullet(tf, text, *, level, bullet, font_size, color)

Add a bullet paragraph.

```python
# Level 0 (dash bullet, 14pt)
add_bullet(tf, "진동 데이터 기반 이상 탐지 모델 구축")

# Level 1 (arrow bullet, 12pt)
add_bullet(tf, "RMS, Peak, Kurtosis, FFT 스펙트럼 특징 추출", level=1)

# Numbered bullet
add_bullet(tf, "정상 데이터로 MCD 모델 학습", level=1, bullet="number")

# No bullet marker
add_bullet(tf, "참고: 이 결과는 예비 실험임", level=1, bullet="none")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | required | Bullet text |
| `level` | int | 0 | Indentation depth (0 = top-level) |
| `bullet` | str \| None | None | Bullet style (see below). `None` = auto |
| `font_size` | int \| None | None | Override font size (pt) |
| `color` | Color \| None | None | Override text colour |

**Bullet styles:**
| Style | Symbol | Default for level |
|-------|--------|-------------------|
| `"dash"` | `-` | 0 |
| `"arrow"` | `→` | 1 |
| `"square"` | `■` | 2 |
| `"circle"` | `●` | 3 |
| `"check"` | `✓` | 4+ |
| `"number"` | 1. 2. 3. | (manual) |
| `"none"` | (no marker) | (manual) |

### add_spacer(tf)

Add an empty separator line.

```python
add_spacer(tf)
```

---

## Color System

### Color Type

The `Color` type is accepted by all color parameters:

```python
from pptx.dml.color import RGBColor

# All of these are valid Color values:
color = RGBColor(0x1B, 0x37, 0x65)   # RGBColor object
color = "1B3765"                      # 6-char hex (no # prefix)
color = "#1B3765"                     # with # prefix (also OK)
color = "27,55,101"                   # R,G,B decimal string
color = "navy"                        # named colour
```

### Named Colours

| Name | Hex | RGB |
|------|-----|-----|
| `"red"` | C00000 | (192, 0, 0) |
| `"green"` | 00B050 | (0, 176, 80) |
| `"blue"` | 0070C0 | (0, 112, 192) |
| `"orange"` | FF7F00 | (255, 127, 0) |
| `"purple"` | 7030A0 | (112, 48, 160) |
| `"navy"` | 072A5E | (7, 42, 94) |
| `"teal"` | 008080 | (0, 128, 128) |
| `"gray"` / `"grey"` | 808080 | (128, 128, 128) |

### Inline Color Tags

Use `[color]text[/color]` syntax inside any text string to colorize spans:

```python
add_bullet(tf, "정상: [green]92.3%[/green], 이상: [red]7.7%[/red]")
add_bullet(tf, "Custom hex: [#FF6600]주의[/#FF6600]")
```

Supported tags: named colours (`[red]`, `[green]`, `[blue]`, `[orange]`, `[purple]`, `[navy]`, `[teal]`, `[gray]`) and hex codes (`[#RRGGBB]`).

### Arrow Shorthand

`->` in any text string is automatically converted to the Wingdings right-arrow glyph (`→`):

```python
add_bullet(tf, "Block Size 증가 -> 정확도 향상, 실시간성 저하", level=1)
```

---

## Shapes & Lines

### add_shape(slide, shape_type, *, ...)

Add a shape to a slide.

```python
from pptx.util import Emu

# Simple rectangle
add_shape(slide, "rectangle",
    left=457200, top=914400, width=2743200, height=1371600,
    fill="1B3765")

# Rounded rectangle with text and shadow
add_shape(slide, "rounded_rectangle",
    left=457200, top=914400, width=2743200, height=1371600,
    fill="FFFFFF", line_color="5B9BD5", line_width=2,
    shadow={"blur": 6, "offset": 2, "angle": 135, "opacity": 0.15},
    text="Module A", font_size=14, color="1B3765", bold=True)

# Transparent shape
add_shape(slide, "oval",
    left=914400, top=914400, width=1828800, height=1828800,
    fill="5B9BD5", transparency=50)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `shape_type` | str | required | Shape name (see below) |
| `left`, `top`, `width`, `height` | int | required | Position/size (EMU) |
| `fill` | Color \| None | None | Fill colour. None = transparent |
| `transparency` | int | 0 | Fill transparency 0–100 |
| `line_color` | Color \| None | None | Border colour. None = no border |
| `line_width` | int | 1 | Border width (pt) |
| `line_dash` | str \| None | None | Dash style (see below) |
| `shadow` | dict \| None | None | Shadow settings (see below) |
| `text` | str \| None | None | Text inside shape |
| `font_size` | int | 12 | Text size (pt) |
| `color` | Color \| None | None | Text colour |
| `bold` | bool | False | Bold text |
| `align` | PP_ALIGN | CENTER | Horizontal alignment |
| `valign` | str | "middle" | `"top"`, `"middle"`, `"bottom"` |

**Shape types:** `"rectangle"`, `"oval"`, `"rounded_rectangle"`, `"triangle"`, `"diamond"`, `"hexagon"`, `"chevron"`

**Shadow dict:**
```python
shadow = {
    "blur": 3,          # blur radius (pt)
    "offset": 2,        # distance (pt)
    "angle": 135,       # direction (degrees, 135 = bottom-right)
    "color": "000000",  # shadow colour
    "opacity": 0.15,    # 0.0–1.0
}
```

### add_line(slide, *, ...)

Add a straight line.

```python
# Horizontal line
add_line(slide, left=457200, top=2286000, width=8229600,
    color="5B9BD5", line_width=2)

# Dashed vertical line
add_line(slide, left=4572000, top=914400, width=0, height=3657600,
    color="E7E6E6", line_width=1, dash="dash")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `left`, `top` | int | required | Start point (EMU) |
| `width` | int | required | Horizontal extent (EMU). 0 = vertical line |
| `height` | int | 0 | Vertical extent (EMU). 0 = horizontal line |
| `color` | Color | "404040" | Line colour |
| `line_width` | int | 1 | Thickness (pt) |
| `dash` | str \| None | None | Dash style |

**Dash styles:** `"solid"`, `"dash"`, `"dot"`, `"dash_dot"`, `"long_dash"`, `"long_dash_dot"`

---

## Tables

### add_table(slide, data, *, ...)

Add a styled table.

```python
from slide_forge.default.slide import add_table

data = [
    ["Joint", "R²", "MAE"],        # header row
    ["J1", "93.5%", "0.012"],
    ["J2", "23.2%", "0.089"],
    ["J3", "91.8%", "0.015"],
]

add_table(slide, data,
    left=457200, top=3200400, width=8229600,
    first_row=True,
    caption="Table 1. Per-joint prediction accuracy")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | list[list[str]] | required | 2-D list of cell text |
| `left`, `top`, `width` | int | required | Position/width (EMU) |
| `height` | int \| None | None | Total height (auto if None) |
| `col_widths` | list[int] \| None | None | Per-column widths (EMU) |
| `first_row` | bool | True | Highlight first row as header |
| `first_col` | bool | False | Highlight first column |
| `header_size` | int | 14 | Header font size (pt) |
| `body_size` | int | 12 | Body font size (pt) |
| `header_fill` | Color | "BFBFBF" | Header row fill |
| `first_col_fill` | Color | "E0E0E0" | First column fill |
| `text_color` | Color | "404040" | Text colour |
| `border_color` | Color | "000000" | Border colour |
| `border_width` | int | 1 | Border width (pt) |
| `align` | PP_ALIGN | CENTER | Text alignment |
| `caption` | str \| None | None | Caption below table |

---

## Charts

### add_chart(slide, chart_type, *, ...)

Add a chart.

```python
from slide_forge.default.slide import add_chart

# Bar chart (category type)
add_chart(slide, "column",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series={"Sales": [4500, 5500, 6200, 7100]},
    left=457200, top=3200400, width=5486400, height=2743200,
    title="Quarterly Sales",
    caption="Fig 1. Revenue by quarter")

# Multi-series line chart
add_chart(slide, "line_markers",
    categories=["Jan", "Feb", "Mar", "Apr"],
    series={
        "Model A": [85.2, 87.1, 89.5, 91.0],
        "Model B": [78.3, 82.4, 84.0, 86.5],
    },
    left=457200, top=3200400, width=5486400, height=2743200,
    colors=["072A5E", "00B050"])

# Pie chart
add_chart(slide, "pie",
    categories=["Normal", "Anomaly", "Unknown"],
    series={"": [92.3, 5.4, 2.3]},
    left=5943600, top=3200400, width=2743200, height=2743200,
    legend=True)

# Scatter chart
add_chart(slide, "scatter",
    series={
        "Experiment": [(1.0, 85.2), (2.0, 87.1), (3.0, 91.0), (4.0, 89.5)],
    },
    left=457200, top=3200400, width=5486400, height=2743200)

# Bubble chart
add_chart(slide, "bubble",
    series={
        "Models": [(1.0, 85.2, 50), (2.0, 91.0, 80), (3.0, 78.5, 30)],
    },
    left=457200, top=3200400, width=5486400, height=2743200)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chart_type` | str | required | Chart type name (see below) |
| `categories` | list[str] \| None | None | Category labels (required for category/pie) |
| `series` | dict \| list | required | Series data (format varies by type) |
| `left`, `top`, `width`, `height` | int | required | Position/size (EMU) |
| `title` | str \| None | None | Chart title |
| `legend` | bool | True | Show legend |
| `colors` | list[Color] \| None | None | Per-series colours |
| `number_format` | str \| None | None | Number format (e.g. `"#,##0"`) |
| `caption` | str \| None | None | Caption below chart |

**Chart types (26 total):**

*Category charts* (need `categories` + `series` as `{name: [values]}`):
`"bar"`, `"bar_stacked"`, `"bar_stacked_100"`, `"column"`, `"column_stacked"`, `"column_stacked_100"`, `"line"`, `"line_markers"`, `"line_stacked"`, `"area"`, `"area_stacked"`, `"area_stacked_100"`, `"radar"`, `"radar_filled"`, `"radar_markers"`

*Pie / Doughnut* (need `categories` + `series`):
`"pie"`, `"pie_exploded"`, `"doughnut"`, `"doughnut_exploded"`

*Scatter* (`series` as `{name: [(x, y), ...]}`):
`"scatter"`, `"scatter_lines"`, `"scatter_smooth"`, `"scatter_lines_no_markers"`, `"scatter_smooth_no_markers"`

*Bubble* (`series` as `{name: [(x, y, size), ...]}`):
`"bubble"`

---

## Figures

### add_figure(slide, image_path, *, ...)

Add an image with optional caption.

```python
from slide_forge.default.slide import add_figure

add_figure(slide, "results/confusion_matrix.png",
    left=457200, top=3200400, width=4572000,
    caption="Fig 2. Confusion matrix for anomaly detection")

# With explicit height (disables auto aspect ratio)
add_figure(slide, "architecture.png",
    left=457200, top=3200400, width=4572000, height=2743200)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image_path` | str | required | Path to image file (PNG, JPEG, etc.) |
| `left`, `top` | int | required | Top-left corner position (EMU) |
| `width` | int | required | Image width (EMU) |
| `height` | int \| None | None | Height (None = auto aspect ratio) |
| `caption` | str \| None | None | Caption below image |

---

## Section Header Bar (▌ Accent)

The section header with ▌ accent is built using `add_section()` inside a content box. For custom section headers using shapes:

```python
from pptx.util import Emu

HEADER_Y = 731520
HEADER_H = 411480
ACCENT_W = 73152

# Section header bar (full width, light gray background)
add_shape(slide, "rectangle",
    left=365760, top=HEADER_Y, width=8412480, height=HEADER_H,
    fill="E7E6E6")

# Left accent stripe (navy)
add_shape(slide, "rectangle",
    left=365760, top=HEADER_Y, width=ACCENT_W, height=HEADER_H,
    fill="1B3765")

# Subtitle text inside the bar
add_shape(slide, "rectangle",
    left=365760 + ACCENT_W + 137160, top=HEADER_Y,
    width=8412480 - ACCENT_W - 137160, height=HEADER_H,
    text="로봇 역동역학 기반 이상 모사 모델(RIDGE) 개발의 필요성",
    font_size=14, color="1B3765", bold=True, align=PP_ALIGN.LEFT)
```

**Key rules:**
- Use `"rectangle"`, not `"rounded_rectangle"` (accent bar won't cover rounded corners)
- The accent stripe sits at the same x/y as the bar, overlapping its left edge

---

## Quick Reference

### Colour Palette Constants

```python
# Core
NAVY = "1B3765"
LIGHT_BLUE = "5B9BD5"
WHITE = "FFFFFF"
OFF_WHITE = "F5F5F5"
LIGHT_GRAY = "E7E6E6"
BLACK = "000000"
DARK_GRAY = "666666"
BODY_GRAY = "333333"

# Data visualization
PURPLE = "7030A0"
CORAL = "C84545"
GREEN = "00B050"
ORANGE = "FFA500"
YELLOW = "FFC000"

# Pastel fills (for diagrams/process boxes)
PASTEL_BLUE = "B4C7E7"
PASTEL_PURPLE = "D5BDDB"
PASTEL_GREEN = "C5E0B4"
PASTEL_ORANGE = "FFD699"
```

### Unit System

| Context | Unit | Example |
|---------|------|---------|
| Position (`left`, `top`, `width`, `height`) | EMU (English Metric Units) | `914400` = 1 inch |
| Font size (`font_size`) | pt (points) | `14` = 14pt |
| Line width (`line_width`) | pt (points) | `2` = 2pt |
| Shadow blur/offset | pt (points) | `3` = 3pt |

**EMU conversions:**
```python
from pptx.util import Inches, Cm, Pt, Emu

Inches(1)   # = 914400 EMU
Cm(1)       # = 360000 EMU
Pt(1)       # = 12700 EMU
Emu(914400) # direct EMU value
```

### Complete Example

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["slide-forge"]
#
# [tool.uv.sources]
# slide-forge = { path = "../../" }
# ///

from pptx.util import Inches, Emu
from slide_forge import (
    get_presentation, create_slide,
    add_slide_title, add_content_box,
    add_section, add_bullet, add_spacer,
    add_shape, add_line,
)
from slide_forge.default.slide import add_table, add_chart, add_figure

prs = get_presentation()

# ── Slide 1: 주요 결과 ───────────────────────────────────
slide1 = create_slide(prs)
add_slide_title(slide1, "MCD 기반 이상 탐지 성능 평가")

tf = add_content_box(slide1)
add_section(tf, "주요 결과")
add_bullet(tf, "정상 데이터 1,198,500건(96.3%), 이상 데이터 46,500건(3.7%)")
add_bullet(tf, "Precision: [green]92.3%[/green], Recall: 88.0%, F1-Score: 90.1%", level=1)
add_bullet(tf, "Joint 1/3/6에 대해 높은 정확도 (R² > 93%)", level=1)
add_bullet(tf, "Joint 2/4 정확도 상대적 저조 -> 개선 필요", level=1)

# Chart in lower area
add_chart(slide1, "column",
    categories=["J1", "J2", "J3", "J4", "J5", "J6"],
    series={"R²": [93.5, 23.2, 91.8, 45.6, 78.9, 95.1]},
    left=Inches(0.5), top=Inches(3.5),
    width=Inches(4.5), height=Inches(2.5),
    title="Per-Joint R² Score",
    legend=False)

# ── Slide 2: 한계점 ─────────────────────────────────────
slide2 = create_slide(prs)
add_slide_title(slide2, "한계점 및 향후 과제")

tf2 = add_content_box(slide2)
add_section(tf2, "한계점")
add_bullet(tf2, "하중 효과를 반영하지 못한 한계점 존재")
add_bullet(tf2, "실제 하중 조건에서의 검증 실험 필요", level=1)

prs.save("output.pptx")
```

---

## Common Pitfalls

1. **All positions are in EMU, not inches** — use `Inches(1)`, `Cm(1)`, or `Emu(914400)` for conversion. Passing raw numbers like `1` means 1 EMU (invisible).

2. **`font_size` and `line_width` are in pt** — these are the exceptions to the EMU rule. `font_size=14` means 14pt, not 14 EMU.

3. **Cover vs Content functions** — `add_cover_title()` / `add_cover_info()` only work on `create_cover_slide()` slides. `add_slide_title()` / `add_content_box()` only work on `create_slide()` slides. Mixing them raises `TypeError`.

4. **`add_content_box()` returns a `TextFrame`** — you must store the return value and pass it to `add_section()`, `add_bullet()`, and `add_spacer()`.

5. **Colour format** — hex strings work with or without `#` prefix. Named colours (`"red"`, `"navy"`, etc.) are also accepted. Never use 8-character hex (RGBA) — use the `transparency` parameter instead.

6. **Shape `fill=None` means transparent** — to get a white-filled shape, explicitly use `fill="FFFFFF"`.

7. **`add_chart` series format varies by chart type**:
   - Category/Pie: `{"name": [v1, v2, ...]}`
   - Scatter: `{"name": [(x1, y1), (x2, y2), ...]}`
   - Bubble: `{"name": [(x, y, size), ...]}`

8. **`add_figure` height=None preserves aspect ratio** — only pass `height` when you need a specific size.

9. **Import paths** — core functions are in `slide_forge` (top-level). Extended functions (`add_table`, `add_chart`, `add_figure`, `add_cover_title`, `add_cover_info`) are in `slide_forge.default.slide`.

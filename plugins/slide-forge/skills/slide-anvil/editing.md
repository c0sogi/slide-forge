# Editing Presentations

## Template-Based Workflow

When using an existing presentation as a template:

1. **Analyze existing slides**:
   ```bash
   uv run slide-forge thumbnail template.pptx
   uv run python -m markitdown template.pptx
   ```
   Review `thumbnails.jpg` to see layouts, and markitdown output to see placeholder text.

2. **Plan slide mapping**: For each content section, choose a template slide.

   **USE VARIED LAYOUTS** — monotonous presentations are a common failure mode. Don't default to basic title + bullet slides. Actively seek out:
   - Multi-column layouts (2-column, 3-column)
   - Image + text combinations
   - Full-bleed images with text overlay
   - Quote or callout slides
   - Section dividers
   - Stat/number callouts
   - Icon grids or icon + text rows

   **Avoid:** Repeating the same text-heavy layout for every slide.

   Match content type to layout style (e.g., key points → bullet slide, team info → multi-column, testimonials → quote slide).

3. **Add/duplicate slides** (before unpacking):
   - Add a blank slide: `uv run slide-forge add-slide template.pptx`
   - Duplicate an existing slide: `uv run slide-forge add-slide template.pptx --source 3`
   - Repeat for each slide you need. The copy is appended at the end.

4. **Unpack**: `uv run slide-forge unpack template.pptx unpacked/`

5. **Build presentation** (do this yourself, not with subagents):
   - Delete unwanted slides (remove from `<p:sldIdLst>`)
   - Reorder slides in `<p:sldIdLst>`
   - **Complete all structural changes before step 6**

6. **Edit content**: Update text in each `slide{N}.xml`.
   **Use subagents here if available** — slides are separate XML files, so subagents can edit in parallel.

7. **Clean**: `uv run slide-forge clean unpacked/`

8. **Pack**: `uv run slide-forge pack unpacked/ output.pptx --original template.pptx`

---

## Commands

| Command | Purpose |
|---------|---------|
| `uv run slide-forge unpack` | Extract and pretty-print PPTX |
| `uv run slide-forge add-slide` | Add a content or cover slide |
| `uv run slide-forge clean` | Remove orphaned files |
| `uv run slide-forge pack` | Repack with validation |
| `uv run slide-forge thumbnail` | Create visual grid of slides |
| `uv run slide-forge render` | PPTX → PDF → PNG via PowerPoint COM |

### unpack

```bash
uv run slide-forge unpack input.pptx unpacked/
```

Extracts PPTX, pretty-prints XML, escapes smart quotes.

### add-slide

```bash
uv run slide-forge add-slide presentation.pptx
uv run slide-forge add-slide presentation.pptx --type cover
uv run slide-forge add-slide presentation.pptx --source 3
uv run slide-forge add-slide presentation.pptx --source 3 --output updated.pptx
```

Adds a blank slide (content or cover) using the slide-forge template, or duplicates an existing slide with `--source N` (1-based index). The new slide is appended at the end.

### clean

```bash
uv run slide-forge clean unpacked/
```

Removes slides not in `<p:sldIdLst>`, unreferenced media, orphaned rels.

### pack

```bash
uv run slide-forge pack unpacked/ output.pptx --original input.pptx
```

Validates, repairs, condenses XML, re-encodes smart quotes.

### thumbnail

```bash
uv run slide-forge thumbnail input.pptx [output_prefix] [--cols N]
```

Creates `thumbnails.jpg` with slide filenames as labels. Default 3 columns, max 12 per grid.

**Use for template analysis only** (choosing layouts). For visual QA, use `uv run slide-forge render` to create full-resolution individual slide images — see SKILL.md.

### render

```bash
uv run slide-forge render output.pptx [output_dir] [--dpi 150]
```

Converts PPTX to individual slide PNG images using MS PowerPoint COM (PPTX → PDF) + PyMuPDF (PDF → PNG). Creates `slide-01.png`, `slide-02.png`, etc.

**Requires**: `pip install pywin32 pymupdf`

---

## Slide Operations

Slide order is in `ppt/presentation.xml` → `<p:sldIdLst>`.

**Reorder**: Rearrange `<p:sldId>` elements.

**Delete**: Remove `<p:sldId>`, then run `uv run slide-forge clean`.

**Add/Duplicate**: Use `uv run slide-forge add-slide` (blank) or `uv run slide-forge add-slide --source N` (duplicate). Never manually copy slide files—the command handles relationships and rId mappings that manual copying misses.

---

## Editing Content

**Subagents:** If available, use them here (after completing step 5). Each slide is a separate XML file, so subagents can edit in parallel. In your prompt to subagents, include:
- The slide file path(s) to edit
- **"Use the Edit tool for all changes"**
- The formatting rules and common pitfalls below

For each slide:
1. Read the slide's XML
2. Identify ALL placeholder content—text, images, charts, icons, captions
3. Replace each placeholder with final content

**Use the Edit tool, not sed or Python scripts.** The Edit tool forces specificity about what to replace and where, yielding better reliability.

### Formatting Rules

- **Bold all headers, subheadings, and inline labels**: Use `b="1"` on `<a:rPr>`. This includes:
  - Slide titles
  - Section headers within a slide
  - Inline labels like (e.g.: "Status:", "Description:") at the start of a line
- **Never use unicode bullets (•)**: Use proper list formatting with `<a:buChar>` or `<a:buAutoNum>`
- **Bullet consistency**: Let bullets inherit from the layout. Only specify `<a:buChar>` or `<a:buNone>`.

---

## Common Pitfalls

### Template Adaptation

When source content has fewer items than the template:
- **Remove excess elements entirely** (images, shapes, text boxes), don't just clear text
- Check for orphaned visuals after clearing text content
- Run visual QA to catch mismatched counts

When replacing text with different length content:
- **Shorter replacements**: Usually safe
- **Longer replacements**: May overflow or wrap unexpectedly
- Test with visual QA after text changes
- Consider truncating or splitting content to fit the template's design constraints

**Template slots ≠ Source items**: If template has 4 team members but source has 3 users, delete the 4th member's entire group (image + text boxes), not just the text.

### Multi-Item Content

If source has multiple items (numbered lists, multiple sections), create separate `<a:p>` elements for each — **never concatenate into one string**.

**WRONG** — all items in one paragraph:
```xml
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

**CORRECT** — separate paragraphs with bold headers:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 2</a:t></a:r>
</a:p>
<!-- continue pattern -->
```

Copy `<a:pPr>` from the original paragraph to preserve line spacing. Use `b="1"` on headers.

### Smart Quotes

Handled automatically by unpack/pack. But the Edit tool converts smart quotes to ASCII.

**When adding new text with quotes, use XML entities:**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

| Character | Name | Unicode | XML Entity |
|-----------|------|---------|------------|
| `"` | Left double quote | U+201C | `&#x201C;` |
| `"` | Right double quote | U+201D | `&#x201D;` |
| `'` | Left single quote | U+2018 | `&#x2018;` |
| `'` | Right single quote | U+2019 | `&#x2019;` |

### Other

- **Whitespace**: Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces
- **XML parsing**: Use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)

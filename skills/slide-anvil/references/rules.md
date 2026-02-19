# Slide Forge Rules -- Canonical Reference

This is the **single source of truth** for all enforceable Slide Forge rules.
- For examples, rhetorical strategies, and pattern catalog: see [style-guide.md](style-guide.md)
- For Phase 1 prose/compressed examples: see [phase1-examples.md](phase1-examples.md)
- **If rules.md and style-guide.md ever diverge, rules.md wins.**

---

## Deck Structure

- Slide 1 is always a Table of Contents (목차).
- No front cover or back cover slides.

## Headers

- Every slide has a Major Title at the absolute top (TOC-indexable, can repeat across slides).
- Every slide has exactly one subtitle line starting with `▌` at the top of the text area.
- The `▌` symbol must NOT appear as a bullet prefix -- it is a section header only.

## Bullet Plan Syntax

- Nested bullets use 4 leading spaces per level.
- Level 1 (4 spaces): `-` only (new claim/takeaway).
- Level 2 (8 spaces): `→` only (support for the immediately previous `-`).
- Level 3 (12 spaces): `-` only (new sub-claim under a `→`).
- Level 4 (16 spaces): `→` only (support for the Level 3 `-`).
- General rule: odd levels (1, 3, 5...) use `-`, even levels (2, 4, 6...) use `→`. Each level adds 4 spaces.
- Do not use en-dash (–), dot bullets (•), or other markers.

### Planning vs Rendered Bullet Markers

In planning text (Phase 1 plans), use ASCII hyphen-minus (`-`) for odd-level bullets.
In rendered PPTX slides, the visual bullet marker may appear as en-dash (–) per
style-guide.md's Level 2 description. This is a presentation-layer distinction:
the planning syntax rule (`-` and `→` only) governs plan text; the rendered
appearance is controlled by PptxGenJS bullet styling or template formatting.

### Planning-to-Render Mapping

The 6-level planning syntax maps to 3 visual tiers in rendered slides:
- Section header (▌ subtitle) = slide title area (16-18pt bold)
- Odd planning levels (1, 3, 5) = main bullets (12-14pt)
- Even planning levels (2, 4, 6) = sub-bullets (10-12pt)

## Line-Break Discipline

- No line breaks inside a single sentence.
- If a line feels too long, split into a `-` line plus `→` sub-lines (not manual wrapping).

## PPTX Encoding Discipline

- Do not implement indentation by inserting literal spaces into slide text.
- Use real bullet levels/indentation (PptxGenJS bullet options or template placeholders).

## Writing Style

### Sentence Endings -- Nominalized

Bullets end with **Sino-Korean nouns**, NOT polite verb endings (-습니다/-합니다/-입니다) or literary endings (-하였다/-이다).

Common ending nouns: ~수행, ~구축, ~확인, ~개발, ~학습, ~진행, ~필요, ~가능, ~존재, ~분석, ~적용, ~고도화, ~추출, ~불가, ~저하, ~선정, ~도입

Exception: Sub-bullets (`→`) that explain reasoning may use slightly more natural Korean, but still avoid polite endings.

### Korean/English Mixing (30-40% English)

- **Technical nouns stay in English**: LSTM, MCD, PCA, Domain Adaptation, Threshold
- **Korean particles attach directly**: "LSTM을", "MCD에서", "Threshold를"
- **First mention**: Korean meaning + English in parentheses -- "이상 탐지(Anomaly Detection)"
- **After first mention**: English alone is fine
- **Variable/parameter names**: explain meaning first -- "클램핑 토크(T_CLAMP)", "위치(pos)"
- **Function/class names**: NEVER use in slides -- describe behavior instead

### Arrow (→) Notation

Implies "therefore" / "leads to" -- not decorative. Used for:
- Logical implication: "학습 = 테스트 가정 → 실제 환경에서 성능 저하"
- Process step result: "3D 공간 재구성 → 3D Reconstruction"
- Trade-off: "Block Size 증가 → 정확도 향상, 실시간성 저하"
- Derived conclusion: "→ Domain Adaptation은 필수적"

### Information Density

- 8-15 lines per slide, 150-300 words
- 3-6 main bullets, each with 1-3 sub-bullets
- Sparse slides (2-3 bullets) are a fail -- add interpretation, context, trade-offs

## Layout Rules

- **Default**: Top 40-60% = text, Bottom 40-60% = visuals (side-by-side if 2-3 visuals)
- No overflow outside text boxes.
- No overlap between shapes and text.
- Typography sizes consistent per level.

### Typography Sizes

| Element | Size (pt) | Weight |
|---------|-----------|--------|
| Slide title | 20-24 | Bold |
| Section header (▌ bar) | 16-18 | Bold |
| Main bullet | 12-14 | Regular |
| Sub-bullet | 10-12 | Regular |
| Table cell | 9-11 | Regular |
| Chart labels | 8-10 | Regular |
| Citations/footnotes | 8-9 | Regular |

### Font Families

| Context | Font |
|---------|------|
| Korean text | Malgun Gothic (맑은 고딕) |
| English text | Calibri |
| Equations | Times New Roman |
| Code/variables | Consolas |

### Color Palette

**Core colors:**
- Navy `1B3765` (titles, headers, emphasis)
- Light blue `5B9BD5` (arrows, dividers, secondary)
- Black `000000` (body text)
- Dark gray `666666` (captions, secondary text)
- Body gray `333333` (sub-bullet text)
- White `FFFFFF` (slide background)

**Data visualization:**
- Chart colors: `1B3765`, `5B9BD5`, `7030A0`, `C84545`, `00B050`, `FFA500`

**Pastel fills (for diagrams/process boxes):**
- Blue `B4C7E7`, Purple `D5BDDB`, Green `C5E0B4`, Orange `FFD699`

## Anti-Patterns (Must Catch)

1. **Number Dumping**: Numbers without "So what?" interpretation -- always need `→` sub-line explaining significance
2. **Jargon Bombardment**: 3+ unexplained English terms per slide -- every term needs Korean meaning on first use
3. **Thin Slides**: Under 8 lines of text, large empty space -- add interpretation, context, trade-offs
4. **Text-in-Boxes as Diagrams**: If moving box text to bullets loses no info, it is not a diagram -- use real data charts, process flows, or architecture diagrams

## Authenticity Markers

Real lab presentations have:
- Specific numbers (not rounded): `R² = 93.5%`, not `약 90%`
- Exact dates/versions: `25.05.27~25.06.22`, `Python 3.12.11`, `PyTorch 2.9.0+cpu`
- Honest limitations: `한계점 존재`, `개선 필요`
- Trade-offs acknowledged: `정확도 향상되지만 실시간성 저하`
- Real names with explanation: `클램핑 토크(T_CLAMP)`, `MODEL-4 w/ load`
- Academic citations at slide bottom (8-9pt)

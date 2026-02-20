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

### Subtitle Form -- Concise Noun Phrase (Hard Rule)

Subtitles (▌ lines) must be **concise noun phrases** (2-8 Korean words or equivalent), NOT descriptive sentences or verbose clauses.

**The subtitle names the TOPIC, not the MESSAGE.** The subtitle answers "이 슬라이드는 무엇에 대한 것인가?" — NOT "이 슬라이드에서 말하고자 하는 바가 뭔가?". The slide's claim or conclusion belongs in a concluding `→` line after the build-up, not the subtitle.

**Allowed subtitle forms:**
- Topic label: `▌하위 집단 분석 결과`
- Topic with focus marker: `▌검증 환경: T-LESS 벤치마크`
- Concise scope: `▌파라미터 민감도 분석`
- Short comparison: `▌DT vs 비전 단독 성능 비교`

**Banned subtitle forms:**
- Content summary crammed into subtitle: ~~`▌하위집단 분석: 다중 인스턴스에서 DT 효과 극대화`~~ → `▌하위 집단 분석 결과` (claim goes to concluding `→` line)
- Sentence/clause with verb structure: ~~`▌비전 단독의 구조적 한계를 DT 기하 사전 정보로 돌파`~~
- Long compound with em-dash extension: ~~`▌5가지 DT 기준선 — 기하 신호별 기여 분리를 위한 가설 검정 프레임`~~
- Concatenation with `+`: ~~`▌Soft Gating with Safety Retention + 복합 기하 스코어링`~~
- Sentence ending with ~검증/~돌파/~해소/~수행: ~~`▌외형 기반 인식의 한계가 가장 극명한 조건에서 검증`~~

**Self-check:** Read the subtitle. (1) If it has a subject-object-verb structure, it is too long. (2) If it contains the slide's conclusion or claim, the message is misplaced — move it to a concluding `→` line in the body. Compress to a topic label.

## Bullet Plan Syntax

- Nested bullets use 4 leading spaces per level.
- Level 1 (4 spaces): `-` only (descriptive claim/observation, written long with nominalized ending).
- Level 2 (8 spaces): `-` (detail, example, specification) or `→` (conclusion/implication only).
- Level 3 (12 spaces): `-` only (new sub-claim).
- Level 4 (16 spaces): `-` (detail) or `→` (conclusion/implication only).
- General rule: odd levels always use `-`. Even levels default to `-`; use `→` **only** for conclusions or logical implications ("therefore"). Each level adds 4 spaces.
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
- If a line feels too long, split into a `-` line plus `-` or `→` sub-lines as appropriate (not manual wrapping).

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

### Arrow (→) Notation — Use Sparingly

Arrows imply "therefore" / "leads to" — they are **NOT** decorative and must **NOT** be used mechanically for every sub-bullet. Arrow overuse is the #1 formatting mistake.

**Allowed uses (→):**
- Derived conclusion at the end of a bullet group: "→ Domain Adaptation은 필수적"
- Logical implication within a sentence: "학습 = 테스트 가정 → 실제 환경에서 성능 저하"
- Trade-off result: "Block Size 증가 → 정확도 향상, 실시간성 저하"
- Essential "So what?" interpretation after data

**Must use `-` instead of `→` for:**
- Examples and enumerations
- Definitions or specifications
- Additional details that don't conclude anything
- Any sub-bullet where removing `→` doesn't change the meaning

**Self-check:** Read the sub-bullet without the arrow. If it still makes sense and doesn't lose a "therefore" relationship, it should be `-`, not `→`.

### Information Density

- 8-15 lines per slide, 150-300 words
- 3-6 main bullets, each with 1-3 sub-bullets
- Sparse slides (2-3 bullets) are a fail -- add interpretation, context, trade-offs

### Slide-Level Message ("So What?")

Every content slide must have a clear, identifiable key message:
- If someone asks "So what?" after reading the slide, the answer must be findable IN the slide itself.
- Fact-listing without argument is insufficient — each slide must make a point, not just present information.
- The slide should provoke discussion: "Is this the right approach?", "What does this imply for deployment?"
- The presenter should NOT need to be present for the slide's message to be understood.

**Build-Up → Conclusion Structure:**
- L1 bullets should be **descriptive and long** (nominalized endings), building up context — observations, data, comparisons, analysis.
- The slide's "So What?" answer must appear **at least once**, typically as the **final `→` line** after the build-up. This is where the slide delivers its takeaway.
- Do NOT compress L1 bullets into short claims. L1 bullets carry rich, descriptive content. The concluding arrow at the end synthesizes the build-up into a single insight.
- Self-check: read the slide without the final `→` conclusion. If the slide becomes a fact-dump with no point, the structure is correct — the conclusion was doing its job. If there is no such conclusion anywhere, the slide fails the "So What?" test.

### Intra-Slide Cohesion (L1 Bullet Connections)

L1 bullets within a single slide must form a **narrative arc**, not a list of independent facts. The audience should feel a logical thread connecting each L1 bullet to the next.

**Required:** Each L1 bullet (except the first) must relate to the previous one through at least one of:
- **Cause → Effect**: "이런 원인이 있다" → "그 결과 이런 현상이 발생"
- **Observation → Interpretation**: "데이터에서 이것이 관찰됨" → "이것이 의미하는 바는..."
- **Premise → Consequence**: "이 조건을 가정하면" → "이런 결과가 도출"
- **Problem → Solution → Limitation**: natural progression within a topic
- **General → Specific**: broad claim followed by supporting detail

**Banned:** L1 bullets that read like independent encyclopedia entries — each one could be on a separate slide with no loss of coherence. If removing any L1 bullet doesn't break the slide's narrative, the bullets are disconnected.

**Self-check:** Read L1 bullets in sequence. If you can shuffle their order without the slide feeling different, they lack a connecting thread. Restructure so each bullet builds on or responds to the previous one.

### Inter-Slide Transitions

Slides must not feel like independent articles. Each slide (except TOC) must connect to the previous one:
- **Implicit bridge**: the subtitle or first bullet naturally follows from the previous slide's conclusion.
- **Explicit bridge**: referencing prior findings — e.g., "Slide 03의 격차를 해소하기 위한 접근" or "앞선 분석에서 드러난 한계를 기반으로..."
- The audience must feel: "이 슬라이드가 나올 수밖에 없구나."

## Layout Rules

- **Default**: Top 40-60% = text, Bottom 40-60% = visuals (side-by-side if 2-3 visuals).
- **Left-right text/visual split is a violation** unless the slide is explicitly a side-by-side comparison. Text on left + chart/image on right = layout FAIL.
- No overflow outside text boxes.
- **No overlap between shapes and text** — any element touching or crossing another element's boundary is a hard FAIL, even partial overlap.
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
5. **Arrow Overuse**: Using `→` for every sub-bullet mechanically — arrows are reserved for conclusions and implications only, not examples or details
6. **Colon Enumeration**: Bullets that follow "라벨: 한 줄 설명" pattern mechanically -- the slide reads like a dictionary, not an argument. Every bullet is "X: Y" with no reasoning, relationships, or implications between items. Fix: restructure as claim → evidence → implication. See [style-guide.md Anti-Pattern 6](style-guide.md#anti-patterns) for examples.
7. **Question-Form Titles/Bullets**: ANY subtitle or Level-1 bullet containing a question mark (`?`) is a hard FAIL — no exceptions. This includes but is not limited to "왜 ~인가?", "~란 무엇인가?", "어떻게 ~할 것인가?", "~충분한가?", "~보완하는가?", "~필요한가?". The presenter's job is to deliver answers, not to pose questions. **Detection: search the entire plan for `?` in subtitles and L1 bullets.** Fix: rewrite as a **concise noun phrase** that names the topic. See [style-guide.md Anti-Pattern 7](style-guide.md#anti-patterns) for examples.
8. **Verbose Descriptive Titles**: Subtitles written as full sentences or long clauses with verb structures -- e.g., "비전 단독의 구조적 한계를 DT 기하 사전 정보로 돌파". Subtitles must be **concise noun phrases (2-8 words)**, not miniature abstracts. Sentence-form titles make the deck unreadable at TOC level and compete with content for attention. Fix: compress to a topic label (e.g., "DT 기하 정보 기반 접근"). See Headers > Subtitle Form rule.
9. **Concatenation Titles**: Using `+`, `및/과` chains, or em-dash (`—`) extensions to cram multiple concepts into one subtitle -- e.g., "Soft Gating with Safety Retention + 복합 기하 스코어링". A subtitle names ONE topic. If two concepts must appear, split into two slides or pick the dominant one. Fix: choose the primary topic as the subtitle.
10. **Subtitle-as-Summary**: The subtitle tries to summarize the slide's content or cram the slide's conclusion into the title area -- e.g., "하위집단 분석: 다중 인스턴스에서 DT 효과 극대화". The subtitle should NAME the topic (`▌하위 집단 분석 결과`), not deliver the message. The slide's claim belongs in a concluding `→` line after the build-up, not the subtitle. Detection: if the subtitle answers "이 슬라이드에서 말하고자 하는 바가 뭔가?" instead of "이 슬라이드는 무엇에 대한 것인가?", it is a summary, not a label. Fix: strip the conclusion out of the subtitle and place it as a `→` conclusion after the descriptive L1 build-up.
11. **L1 Bullet Disconnection**: Top-level bullets within a single slide read like independent listings with no connecting thread -- each one could be moved to a separate slide without loss. The slide feels like a collection of loosely related facts, not a coherent argument. Detection: shuffle the L1 bullets; if the slide reads the same in any order, the bullets are disconnected. Fix: restructure L1 bullets as a narrative arc (observation → interpretation → implication, or problem → evidence → conclusion). Add transitional phrases or logical sequencing between bullets. See [style-guide.md Anti-Pattern 11](style-guide.md#anti-patterns) for examples.

## Authenticity Markers

Real lab presentations have:
- Specific numbers (not rounded): `R² = 93.5%`, not `약 90%`
- Exact dates/versions: `25.05.27~25.06.22`, `Python 3.12.11`, `PyTorch 2.9.0+cpu`
- Honest limitations: `한계점 존재`, `개선 필요`
- Trade-offs acknowledged: `정확도 향상되지만 실시간성 저하`
- Real names with explanation: `클램핑 토크(T_CLAMP)`, `MODEL-4 w/ load`
- Academic citations at slide bottom (8-9pt)

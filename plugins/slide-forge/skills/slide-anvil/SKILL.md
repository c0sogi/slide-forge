---
name: slide-anvil
description: "Create or edit PowerPoint (.pptx) presentations in Slide Forge lab style. Use this only if you cannot spawn agents"
---

# Slide Anvil — PPTX Creation & Editing Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `uv run python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |
| Full content & visual specs | Read [references/style-guide.md](references/style-guide.md) |

---

## Core Principle

**Content is everything.** The goal is to produce slides that read like they were written by a lab researcher — dense, technical, specific, and honest. Branding elements (logos, decorative headers) are secondary and optional. If the text content doesn't feel like a real lab report, the presentation has failed regardless of how it looks.

---

## Rules Reference

All writing, structural, and layout rules: [references/rules.md](references/rules.md)
Full examples and pattern catalog: [references/style-guide.md](references/style-guide.md)

---

## Creation Workflow (Required Phases)

**Never jump straight into code.** Plan content first, then generate slides, then QA.

### Phase 1: Content Planning (Before Any Code)

**This is NOT a one-shot outline.** Phase 1 is an iterative refinement loop. You must cycle through drafting, self-critique, and revision until the content passes your own quality bar. Expect 2-3 rounds minimum.

#### Step 1A: Narrative Draft (서술식 초안)

For each slide, **write the content as flowing prose first** — full sentences, in Korean, as if you were explaining it to a colleague. This is your raw material.

**Why prose first?** Bullet points written directly tend to be shallow and generic. Writing prose forces you to actually understand and reason through the content, producing specific details and logical connections that survive the compression into bullets.

For rhetorical strategy examples (prose BAD/GOOD comparisons and compressed bullet versions), see [references/phase1-examples.md](references/phase1-examples.md).

#### Step 1B: Bullet Compression (불릿 압축)

Compress the narrative draft from Step 1A into the Bullet Plan Syntax defined in [references/rules.md](references/rules.md).

**Process:**
1. Extract core claims and supporting evidence from the prose
2. Convert to the hierarchical bullet structure: `-` (claim) → `→` (support) → `-` (sub-claim) → `→` (sub-support)
3. Preserve the rhetorical strategy from the prose — different slides use different strategies:
   - 논증형 (argument chain): 문제 → 기존 해법 실패 → 새 접근 필연성
   - 의사결정형 (design rationale): 선택지 → 선택 이유 → 안 했으면 어떻게 됐을까
   - 인사이트형 (interpretation): 기대 → 결과 → 해석 → 한계
4. Ensure every bullet ends with a nominalized noun ending (명사형 종결)

**Compression rules:**
- Main bullet (`-`): one complete claim, 15-40 Korean characters
- Sub-bullet (`→`): evidence, mechanism, or interpretation, 10-25 characters
- No information loss: every key insight from the prose must survive compression
- No polite endings (습니다/합니다) — use noun endings (~수행, ~구축, ~확인, etc.)

For detailed BAD/GOOD compression examples by rhetorical strategy, see [references/phase1-examples.md](references/phase1-examples.md).

#### Step 1C: Visual Specification + Critical Evaluation

For each slide, specify the visual element, then **challenge it**:

1. **Specify**: Visual type, data, labels, layout
2. **Challenge (반드시 자문)**:
   - "이 그림이 텍스트에 없는 새로운 정보를 전달하는가?" → 텍스트를 그대로 반복하는 그림은 쓸모없다
   - "청중이 3초 만에 핵심 메시지를 파악할 수 있는가?" → 복잡하면 단순화하거나 분할
   - "이 시각 자료 없이 슬라이드가 성립하는가?" → Yes면 다른 시각 자료를 선택
   - "비교/추이/구조/분포 중 어떤 관계를 보여주는 것인가?" → 목적이 불명확하면 재설계
   - **"박스 안의 텍스트를 불릿으로 옮기면 정보가 줄어드는가?"** → No면 그것은 다이어그램이 아니라 장식된 텍스트. 실제 데이터 차트, 프로세스 플로우, 아키텍처 구조도 등으로 교체.
3. **Revise or replace** if the visual fails any challenge

For visual specification examples with self-checks, see [references/phase1-examples.md](references/phase1-examples.md).

#### Step 1D: Story Check (전체 흐름 검증)

All slides complete? Read 1→N in sequence and check:

- Does each slide build on the previous one?
- Are unfamiliar concepts explained before being used? (concept slide → application slide)
- Is there a clear progression (background → method → results → future)?
- **Would a professor reading only the slide titles understand the research structure?**

#### Iteration Rule

**Repeat Steps 1A-1D until you can answer "yes" to all of these:**

- [ ] Every bullet contains a specific detail (number, name, version) — not just a general description
- [ ] Every number is followed by its interpretation ("So what?") — never naked numbers
- [ ] Every English term has Korean meaning on first use — count: 3+ unexplained terms per slide = fail
- [ ] Every visual adds insight beyond what the text says
- [ ] The narrative flows logically without unexplained jumps
- [ ] No bullet ends with a polite verb (습니다/합니다/됩니다)
- [ ] Each slide has 8-15 lines of text — fewer than 8 = too thin, add interpretation
- [ ] A domain expert would find nothing obviously wrong or oversimplified

Only then proceed to Phase 2.

### Phase 2: Code Generation + Slide-by-Slide Review

Only after Phase 1 is complete, write PptxGenJS code following [pptxgenjs.md](pptxgenjs.md).

**After writing the code for each slide**, pause and run a critical review. Do NOT batch all slides and review later — review each slide immediately after writing it.

#### Per-Slide Self-Review Checklist

For every slide you just coded, ask these questions **in order**:

**1. 이해 가능성 (Comprehensibility)**
- "이 슬라이드만 단독으로 봤을 때, 청중이 무슨 내용인지 이해할 수 있는가?"
- "전문 용어를 처음 사용하는 곳에서 설명 없이 쓰지는 않았는가?" → 슬라이드 내 미설명 영문 용어를 세어보라. 3개 이상이면 즉시 수정.
- "불릿 하나하나가 명확한 하나의 메시지를 전달하는가, 아니면 여러 내용이 뒤섞여 있는가?"
- "숫자를 제시한 후 '그래서 이게 왜 중요한가?'에 대한 해석이 있는가?" → 없으면 해석 추가. 숫자만 던지는 것은 발표가 아니라 데이터 덤프.

**2. 필수성 (Necessity)**
- "이 문장을 삭제하면 슬라이드의 핵심 메시지가 훼손되는가?" → No면 삭제
- "이 시각 자료를 제거해도 내용 전달에 지장이 없는가?" → Yes면 교체
- "장식용 요소(의미 없는 박스, 불필요한 구분선)가 있는가?" → 있으면 제거

**3. 중복 검사 (Redundancy)**
- "이전 슬라이드에서 이미 말한 내용을 반복하고 있지는 않은가?"
- "같은 슬라이드 내에서 표현만 다르고 의미가 같은 불릿이 있지는 않은가?"
- "텍스트와 시각 자료가 완전히 같은 정보를 보여주고 있지는 않은가?" → 시각 자료는 텍스트를 보충해야지, 복사해서는 안 됨

**4. 깊이 검사 (Depth)**
- "이 불릿이 너무 피상적이지는 않은가?" — "모델 성능 향상" 같은 빈 문장 대신 "F1-Score 85.3% → 91.9% (Block Size 256 적용)"
- "숫자를 나열한 뒤 '이 숫자가 의미하는 바'를 설명했는가?" — "+24.3pp 우위" 자체는 의미가 없음. "전 구간에서 일관된 우위 → 특정 조건이 아닌 구조적 차이"처럼 해석 필수
- "구체적 수치, 조건, 근거가 빠져 있지는 않은가?"
- "전문가가 읽었을 때 '당연한 소리'라고 느낄 내용만 있지는 않은가?"

**5. 내러티브 연결 (Narrative Flow)**
- "이전 슬라이드의 결론이 이 슬라이드의 도입으로 자연스럽게 이어지는가?"
- "이 슬라이드가 전체 발표의 어디쯤에 해당하는지 청중이 감지할 수 있는가?"
- "이 슬라이드의 마지막 불릿이 다음 슬라이드로의 자연스러운 전환점이 되는가?"

#### Fix-Before-Continue Rule

위 체크리스트에서 **하나라도 문제가 발견되면 즉시 수정** 후 다음 슬라이드로 넘어간다. 문제를 모아뒀다가 나중에 고치지 않는다 — 앞 슬라이드의 문제가 뒤 슬라이드 내용에 영향을 주기 때문이다.

### Phase 3: QA

Follow the QA section below — render, inspect, fix, repeat.

---

## Reading Content

```bash
uv run python -m markitdown presentation.pptx
uv run python scripts/thumbnail.py presentation.pptx
uv run python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Follow [Creation Workflow](#creation-workflow-required-phases) above** — Phase 1 (plan) → Phase 2 (code) → Phase 3 (QA).

For PptxGenJS API reference, read [pptxgenjs.md](pptxgenjs.md). Use when no template or reference presentation is available.

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
uv run python -m markitdown output.pptx
```

Check:
- Missing content, typos, wrong order
- **Polite endings that slipped in** (search for 습니다, 합니다, 됩니다)
- **Flat bullet lists** without hierarchy (should have main + sub levels)
- **Vague/generic text** that could apply to any project (should be specific)
- Leftover placeholder text: `uv run python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum"`

### Visual QA

**You MUST render slides to images and read every image file.** Never skip this — code alone cannot tell you if the output looks correct.

```bash
uv run python scripts/render_slides.py output.pptx output_slides/
```

Then **read each PNG file** (e.g., `output_slides/slide-01.png`) and inspect visually. Use subagents for fresh eyes — even for 2-3 slides.

#### Visual Inspection Checklist (per slide image)

**레이아웃 문제:**
- 텍스트가 박스/슬라이드 밖으로 넘치지 않는가?
- 요소들이 겹치지 않는가? (텍스트 위에 도형, 라인이 글자를 가로지름)
- 상하 구도가 지켜지는가? (위 = 텍스트, 아래 = 시각 자료)
- 여백이 충분한가? (슬라이드 가장자리 0.5" 이상)

**시각 자료 품질:**
- 차트/다이어그램이 실제로 렌더링되었는가? (빈 공간이면 코드 오류)
- 라벨이 읽히는 크기인가? (너무 작으면 확대해도 읽히지 않음)
- 색상이 Slide Forge 팔레트를 따르는가?
- **시각 자료가 텍스트 내용을 보충하는가, 단순 반복하는가?**

**타이포그래피:**
- 폰트 크기가 일관적인가? (같은 계층의 불릿이 같은 크기)
- 타이틀이 너무 크거나 작지 않은가?
- 볼드/일반이 적절히 구분되는가?

#### Verification Loop (반복 필수)

```
1. 코드 생성 완료 → PPTX 생성 → 이미지 렌더링
2. 모든 슬라이드 이미지를 읽고(Read) 위 체크리스트로 검사
3. 발견된 문제 목록 작성 (0개면 더 비판적으로 다시 검사)
4. 코드 수정 → PPTX 재생성 → 이미지 재렌더링
5. 수정된 슬라이드 이미지를 다시 읽고(Read) 재검사
6. 새로운 문제가 0개일 때까지 반복
```

**절대 이미지를 읽지 않고 "문제 없음"이라 선언하지 말 것.** 이미지 파일을 Read tool로 직접 열어서 눈으로 확인해야만 Visual QA가 완료된다.

---

## Converting to Images

```bash
uv run python scripts/render_slides.py output.pptx
uv run python scripts/render_slides.py output.pptx ./my_slides --dpi 200
```

Creates `slide-01.png`, `slide-02.png`, etc.

---

## Dependencies

```bash
uv add pywin32 pymupdf pillow python-pptx defusedxml
uv run pip install "markitdown[pptx]"
npm install pptxgenjs          # for creating from scratch
npm install react react-dom react-icons sharp  # for icons (optional)
```

---

## Platform Compatibility

Not all scripts work on all platforms. Choose the right tool for your environment:

| Script | Platform | Requires | Purpose |
|--------|----------|----------|---------|
| `render_slides.py` | **Windows only** | MS PowerPoint + `pywin32`, `pymupdf` | Full-fidelity slide → PNG (via COM) |
| `thumbnail.py` | **Linux / WSL** | LibreOffice (`soffice`), `poppler-utils` (`pdftoppm`), `pillow` | Quick thumbnail grid for template analysis |
| `add_slide.py` | Any | `defusedxml` (indirect) | Duplicate/create slides in unpacked dir |
| `clean.py` | Any | `defusedxml` | Remove orphaned files from unpacked dir |
| `office/pack.py` | Any | `defusedxml` | Repack unpacked dir → .pptx |
| `office/unpack.py` | Any | `defusedxml` | Unpack .pptx → editable XML |
| `office/validate.py` | Any | `defusedxml` | XSD schema validation + auto-repair |
| PptxGenJS (Node.js) | Any | `node`, `pptxgenjs` | Create .pptx from scratch via JS |

**Visual QA fallback when PowerPoint is unavailable:**
- Use `thumbnail.py` (requires LibreOffice) for approximate rendering
- Or open the .pptx in LibreOffice Impress and manually export to PDF/images
- Note: LibreOffice rendering may differ from PowerPoint (fonts, spacing, SmartArt)

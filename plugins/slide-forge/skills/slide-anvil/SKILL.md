---
name: slide-anvil
description: "Create or edit PowerPoint (.pptx) presentations in Slide Forge lab style. Use this only if you cannot spawn agents"
---

# Slide Anvil — PPTX Creation & Editing Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `uv run python -m markitdown presentation.pptx` |
| Create or rebuild PPTX | Read [slide-forge-api.md](slide-forge-api.md) |
| Full content & visual specs | Read [references/style-guide.md](../../references/style-guide.md) |

---

## Core Principle

**Content is everything.** The goal is to produce slides that read like they were written by a lab researcher — dense, technical, specific, and honest. Branding elements (logos, decorative headers) are secondary and optional. If the text content doesn't feel like a real lab report, the presentation has failed regardless of how it looks.

---

## Usage Modes

This skill operates in two modes depending on whether agents can be spawned:

| Mode | When | What You Do |
|------|------|-------------|
| **Normal (Agent Mode)** | Storyteller + Critics are available | Smith uses only **Phase 2 (Build) + Phase 3 (QA)** from this skill. Content comes from `.slide-forge/narrative/slide-plan.md` and `visual-spec.md`. |
| **Fallback (Enhanced Smith)** | Agents cannot be spawned | You self-execute the full pipeline: content planning → self-critique → build → QA. See [Enhanced Smith Fallback](#enhanced-smith-fallback-workflow) below. |

In **Normal mode**, skip directly to [Phase 2: Code Generation](#phase-2-code-generation--slide-by-slide-review). Your inputs are:
- `.slide-forge/narrative/slide-plan.md` — bullet plan
- `.slide-forge/narrative/visual-spec.md` — visual specifications
- `.slide-forge/sources/images/` — image files

Your outputs go to `.slide-forge/build/`.

---

## Rules Reference

All writing, structural, and layout rules: [references/rules.md](../../references/rules.md)
Full examples and pattern catalog: [references/style-guide.md](../../references/style-guide.md)

---

## Creation Workflow (Required Phases)

**Never jump straight into code.** Plan content first, then generate slides, then QA.

> **Normal (Agent) Mode:** Skip Phase 1 entirely — the Storyteller handles content planning. Start from [Phase 2](#phase-2-code-generation--slide-by-slide-review), reading from `.slide-forge/narrative/`.

### Phase 1: Content Planning (Fallback Mode Only)

**This phase applies only in Enhanced Smith fallback mode** (when Storyteller is unavailable). In normal agent mode, the Storyteller produces `slide-plan.md` and `visual-spec.md` — skip directly to Phase 2.

Save all Phase 1 outputs to `.slide-forge/narrative/`:
- `narrative-full.md` — prose draft (narrative format: see [references/narrative-format.md](../../references/narrative-format.md))
- `slide-plan.md` — compressed bullet plan
- `visual-spec.md` — visual specifications

**One pass, then hand off to critics.** Draft the content carefully in a single pass (Steps 1A→1B→1C→1D), run the mechanical self-check, then submit to critics. Do NOT self-iterate 2-3 times — the external critic loop (Crucible → Gauge → Assayer → Wanderer) handles iterative refinement. Your job is to produce a solid first draft, not a polished final version.

#### Step 1A: Narrative Draft (서술식 초안)

For each slide, **write the content as flowing prose first** — full sentences, in Korean, as if you were explaining it to a colleague. This is your raw material.

**Why prose first?** Bullet points written directly tend to be shallow and generic. Writing prose forces you to actually understand and reason through the content, producing specific details and logical connections that survive the compression into bullets.

For rhetorical strategy examples (prose BAD/GOOD comparisons and compressed bullet versions), see [references/phase1-examples.md](../../references/phase1-examples.md).

#### Step 1B: Bullet Compression (불릿 압축)

Compress the narrative draft from Step 1A into the Bullet Plan Syntax defined in [references/rules.md](../../references/rules.md).

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

For detailed BAD/GOOD compression examples by rhetorical strategy, see [references/phase1-examples.md](../../references/phase1-examples.md).

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

For visual specification examples with self-checks, see [references/phase1-examples.md](../../references/phase1-examples.md).

#### Step 1D: Story Check (전체 흐름 검증)

All slides complete? Read 1→N in sequence and check:

- Does each slide build on the previous one?
- Are unfamiliar concepts explained before being used? (concept slide → application slide)
- Is there a clear progression (background → method → results → future)?
- **Would a professor reading only the slide titles understand the research structure?**

#### Mechanical Self-Check (Before Submitting to Critics)

Run these **countable/verifiable** checks once. Do NOT re-draft — fix only what fails here, then submit to critics.

- [ ] No bullet ends with a polite verb (습니다/합니다/됩니다) — search and replace
- [ ] Each slide has 8-15 lines of text — fewer than 8 = add one more sub-bullet with interpretation
- [ ] Per slide: count unexplained English terms. 3+ = add Korean meaning on first use
- [ ] No "라벨: 한 줄 설명" colon-enumeration pattern (3+ in a slide = restructure)
- [ ] No question-form subtitles ("왜 ~인가?") — rewrite as assertive statement
- [ ] Every number has at least one `→` sub-line with interpretation

These are mechanical — you can verify them by scanning the text. Semantic quality (depth, narrative flow, persuasiveness) is judged by external critics, not by you.

Proceed to Phase 2 after this check passes.

### Phase 2: Code Generation + Slide-by-Slide Review

Only after content planning is complete (Phase 1 in fallback, or Storyteller artifacts in normal mode), write Python script following [slide-forge-api.md](slide-forge-api.md).

**Inputs:** Read `slide-plan.md` and `visual-spec.md` from `.slide-forge/narrative/`.
**Outputs:** Save script and PPTX to `.slide-forge/build/`.

```bash
# Save script to .slide-forge/build/create_slides.py, then run:
uv run .slide-forge/build/create_slides.py
```

**After writing all slide code**, run a quick mechanical scan. Semantic quality review is the critics' job — do not duplicate it here.

#### Post-Code Mechanical Scan

Scan the generated code/text for these **mechanically verifiable** issues only:

- [ ] Bullet text matches slide-plan.md — no content was lost or invented during code translation
- [ ] Bullet levels are encoded as real indentation levels (not literal leading spaces)
- [ ] No polite verb endings slipped in (습니다/합니다/됩니다)
- [ ] Visual elements have correct data (labels, values match visual-spec.md)
- [ ] No placeholder text remains (XXXX, lorem, TBD without gray dashed border)

Fix any failures, then proceed to Phase 3. Do NOT review for depth, narrative, or persuasiveness — that is Slide-Assayer's responsibility.

### Phase 3: QA

Follow the QA section below — render to `.slide-forge/build/rendered/`, inspect, fix, repeat.

---

## Enhanced Smith Fallback Workflow (에이전트 스폰 불가 시)

When agents cannot be spawned (no Storyteller, Crucible, Gauge, Assayer, Wanderer available), this skill runs the full pipeline in self-execution mode with role switching.

**Prerequisites:**
- Create `.slide-forge/` directory structure before starting
- Write `config.json` with topic, audience, purpose

**Role Switching (6 steps):**

1. **Storyteller Mode**: Execute Phase 0 (source collection + analysis) + Phase 1 (prose draft → bullet compression → visual spec → flow check). Save all outputs to `.slide-forge/narrative/`.

2. **Crucible Role**: Challenge your own strategic choices as if reviewing a stranger's plan. Ask "why this and not something else?" for each major decision (slide ordering, rhetorical strategy, visual choices). Output DEEPEN or PROCEED.

3. **Enhanced Smith Response**: Respond to every reflection prompt with one of:
   - **Maintain**: defend current choice with concrete reasoning
   - **Adopt**: accept alternative and revise
   - **Synthesize**: combine elements of both
   Revise `.slide-forge/narrative/` files if any changes were adopted.

4. **Gauge Role**: Validate `slide-plan.md` against all structural rules in [rules.md](../../references/rules.md). Output PASS or FAIL with concrete fix instructions.

5. **Assayer Role**: Validate narrative depth, comprehensibility, information loss (narrative-full.md vs slide-plan.md). Output PASS or FAIL with rewrite directives.

6. **Smith Mode**: Execute Phase 2 (Build PPTX) + Phase 3 (QA). Save to `.slide-forge/build/`.

7. **Gauge + Assayer + Wanderer Role**: Validate build output (extracted text via `markitdown` + rendered slide images). For Wanderer role: evaluate comprehension as a naive reader — do NOT re-read your own plan, narrative, or source materials.

8. **(FAIL)** Smith Mode: Fix issues, rebuild. Max 3 iterations per phase.

**Bias mitigation for self-execution:**
- When switching to Crucible role, forget your authorial intent. Ask "why this and not something else?" as if reviewing a stranger's plan.
- When switching to Gauge, Assayer, or Wanderer role, do NOT re-read your own plan or code.
- When switching to Wanderer role, actively forget your narrative intent. Ask "Can I understand this slide having never seen the source material?" If you think "I know what I meant here," that is the Wanderer finding a comprehension gap.
- Work ONLY from extracted evidence: `markitdown` output and rendered slide images.
- Pretend you see these slides for the first time. If you think "I know what I meant here," the slide is unclear — flag it.
- Apply the same PASS/FAIL threshold as if reviewing someone else's work.

---

## Reading Content

```bash
uv run python -m markitdown presentation.pptx
uv run slide-forge thumbnail presentation.pptx
```

---

## Creating / Rebuilding

All PPTX creation and editing uses the declarative Python API. Modify the `create_slides.py` script and re-run — no XML unpacking needed.

**Follow [Creation Workflow](#creation-workflow-required-phases) above** — Phase 1 (plan) → Phase 2 (code) → Phase 3 (QA).

For slide-forge API reference, read [slide-forge-api.md](slide-forge-api.md).

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
uv run python -m markitdown .slide-forge/build/output.pptx
```

Check:
- Missing content, typos, wrong order vs slide-plan.md
- **Polite endings that slipped in** (search for 습니다, 합니다, 됩니다)
- **Flat bullet lists** without hierarchy (should have main + sub levels)
- **Vague/generic text** that could apply to any project (should be specific)
- Leftover placeholder text: `uv run python -m markitdown .slide-forge/build/output.pptx | grep -iE "xxxx|lorem|ipsum"`

### Visual QA

**You MUST render slides to images and read every image file.** Never skip this — code alone cannot tell you if the output looks correct.

```bash
uv run slide-forge render .slide-forge/build/output.pptx .slide-forge/build/rendered/
```

Then **read each PNG file** (e.g., `.slide-forge/build/rendered/slide-01.png`) and inspect visually. Use subagents for fresh eyes — even for 2-3 slides.

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

#### Verification (1 Round)

```
1. 코드 생성 완료 → PPTX 생성 → 이미지 렌더링
2. 모든 슬라이드 이미지를 읽고(Read) 위 체크리스트로 검사
3. 발견된 레이아웃/타이포 문제만 수정 → PPTX 재생성
4. 외부 critics (Gauge + Assayer + Wanderer)에게 제출
```

**1회 렌더링 + 1회 수정까지만.** 추가 반복은 critic 피드백 후에 수행한다. Smith가 자체적으로 무한 루프를 돌지 않는다.

**절대 이미지를 읽지 않고 "문제 없음"이라 선언하지 말 것.** 이미지 파일을 Read tool로 직접 열어서 눈으로 확인해야만 Visual QA가 완료된다.

---

## Converting to Images

```bash
uv run slide-forge render .slide-forge/build/output.pptx .slide-forge/build/rendered/
uv run slide-forge render .slide-forge/build/output.pptx .slide-forge/build/rendered/ --dpi 200
```

Creates `slide-01.png`, `slide-02.png`, etc. in `.slide-forge/build/rendered/`.

---

## Dependencies

```bash
uv add pywin32 pymupdf pillow python-pptx defusedxml
uv run pip install "markitdown[pptx]"
# slide-forge library (PEP 723 scripts auto-install via uv run)
```

---

## Platform Compatibility

Not all commands work on all platforms. Choose the right tool for your environment:

| Command | Platform | Requires | Purpose |
|---------|----------|----------|---------|
| `uv run slide-forge render` | **Windows only** | MS PowerPoint + `pywin32`, `pymupdf` | Full-fidelity slide → PNG (via COM) |
| `uv run slide-forge thumbnail` | **Linux / WSL** | LibreOffice (`soffice`), `poppler-utils` (`pdftoppm`), `pillow` | Quick thumbnail grid for template analysis |
| `uv run slide-forge unpack` | Any | `defusedxml` | Unpack .pptx for diagnostic XML inspection |
| `uv run slide-forge validate` | Any | `defusedxml`, `lxml` | XSD schema validation + auto-repair |
| slide-forge (Python API) | Any | `python-pptx` | Create .pptx from scratch via Python |

**Visual QA fallback when PowerPoint is unavailable:**
- Use `uv run slide-forge thumbnail` (requires LibreOffice) for approximate rendering
- Or open the .pptx in LibreOffice Impress and manually export to PDF/images
- Note: LibreOffice rendering may differ from PowerPoint (fonts, spacing, SmartArt)

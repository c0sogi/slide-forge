---
description: Reforge an existing PowerPoint presentation following Slide Forge conventions
---

# Reforge Presentation

Reforge (edit or improve) an existing PowerPoint presentation following Slide Forge conventions.

## Input

$ARGUMENTS

## Procedure

**Step 1: Scope Assessment (Required First Step)**

Before choosing a workflow, assess the scope of the requested changes:

| Change Type | Examples | Action |
|-------------|----------|--------|
| **Structural** | Add/delete slides, reorder, restructure narrative | Full pipeline from Phase 1a (Storyteller) |
| **Content** | Update data, fix text, replace visuals | Smith direct (Phase 2 only) |
| **Ambiguous** | Unclear scope | Ask user to clarify |

Ask: "이 변경은 구조적 변경(슬라이드 추가/삭제/순서변경)인가, 내용 수정(데이터 갱신/텍스트 교정)인가?"

**Step 2: Choose orchestration mode**
- If you can spawn agents (Task tool available): read the **slide-foundry** skill and follow its orchestration procedure (including the Reforge section).
- If you cannot spawn agents: read the **slide-anvil** skill and self-execute using the Enhanced Smith Fallback.

**Step 3: Execute the workflow**

For **structural changes** with agents (slide-foundry):
1. **Phase 0 — Setup**: Create/reuse `.slide-forge/` workspace
2. **Phase 1a — Storytelling**: Spawn `slide-storyteller` → analyzes existing deck + writes revised narrative
3. Spawn `slide-crucible` on revised `narrative-full.md` → strategic reflection
4. Storyteller compresses → revised `slide-plan.md` + `visual-spec.md`
5. **Phase 1b — Quality Gate**: Spawn `slide-gauge` + `slide-assayer` → PASS/FAIL
6. **Phase 2 — Build**: Spawn `slide-smith` → rebuilds PPTX
7. **Phase 3 — Build Quality Gate**: gauge + assayer + wanderer on build → PASS/FAIL

For **content changes** with agents:
1. Skip Storyteller entirely
2. **Artifact Freshness Check**: Run `markitdown` on existing PPTX, compare slide count and titles against `slide-plan.md`. If mismatch detected, warn user and optionally reroute to structural path. (See slide-foundry SKILL.md [Artifact Freshness Check] for details.)
3. Smith reads existing `.slide-forge/narrative/` artifacts
4. Smith modifies `create_slides.py` and rebuilds the PPTX
5. **Phase 3 — Build Quality Gate**: gauge + assayer + wanderer on result → PASS/FAIL

Without agents (slide-anvil Enhanced Smith Fallback):
1. Analyze existing presentation (`markitdown` for text, `thumbnail` for layouts)
2. Apply scope-appropriate workflow (structural → full pipeline, content → edit only)
3. Visual QA (render → inspect → fix)

## Output

Deliver the updated `.slide-forge/build/output.pptx` file and rendered slide images for verification.

## Pre-Flight Checks

Before starting the workflow:
1. Verify source materials are accessible (file paths exist, URLs respond)
2. Confirm output path is writable
3. If source materials are ambiguous or insufficient, ask the user for clarification before proceeding

## Completion Gate

Before delivering to the user:
1. Scope assessment was performed and documented
2. For structural changes: Crucible strategic reflection was completed (Storyteller responded to all reflection prompts)
3. All three Phase 3 critics (Gauge + Assayer + Wanderer) must have returned PASS, OR iteration cap was reached with a "Known Issues" section attached
4. At least one full visual QA pass was completed (rendered images inspected)
5. Final PPTX opens without corruption

## Edit-Specific Validation

1. Before editing: extract current slide text and thumbnail grid for baseline comparison
2. After editing: diff extracted text against baseline to verify intended changes and catch unintended modifications
3. Preserve all slides not targeted for editing — verify untouched slide count matches

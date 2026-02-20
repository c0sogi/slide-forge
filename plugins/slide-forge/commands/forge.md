---
description: Forge a new PowerPoint presentation in Slide Forge lab style from source materials
---

# Forge Presentation

Forge a new Slide Forge-style PowerPoint presentation based on the user's request.

## Input

$ARGUMENTS

## Procedure

**Step 1: Choose orchestration mode**
- If you can spawn agents (Task tool available): read the **slide-foundry** skill and follow its orchestration procedure.
- If you cannot spawn agents: read the **slide-anvil** skill and self-execute all phases using the Enhanced Smith Fallback.

**Step 2: Execute the workflow**

With agents (slide-foundry):
1. **Phase 0 — Setup**: Create `.slide-forge/` workspace + `config.json`
2. **Phase 1a — Storytelling**: Spawn `slide-storyteller` → proactive source collection + academic-quality narrative writing
3. Spawn `slide-crucible` on `narrative-full.md` → strategic reflection (DEEPEN/PROCEED)
4. If DEEPEN: Storyteller responds to reflection prompts, revises narrative
5. Storyteller compresses narrative → `slide-plan.md` + `visual-spec.md`
6. **Phase 1b — Narrative Quality Gate**: Spawn `slide-gauge` + `slide-assayer` → PASS/FAIL
7. If FAIL: Storyteller revises → re-critique (max 3 iterations)
8. **Phase 2 — Build**: Spawn `slide-smith` with `slide-plan.md` + `visual-spec.md` → builds PPTX
9. **Phase 3 — Build Quality Gate**: Spawn gauge + assayer + wanderer on extracted text + rendered images → PASS/FAIL
10. If FAIL: Smith revises → re-critique (max 3 iterations)

Without agents (slide-anvil Enhanced Smith Fallback):
- Storyteller Mode → Crucible Role → Response → Gauge/Assayer → Smith Mode → QA (Gauge + Assayer + Wanderer)

## Output

Deliver the final `.slide-forge/build/output.pptx` file and rendered slide images for verification.

## Pre-Flight Checks

Before starting the workflow:
1. Verify source materials are accessible (file paths exist, URLs respond)
2. Confirm output path is writable
3. If source materials are ambiguous or insufficient, ask the user for clarification before proceeding

## Completion Gate

Before delivering to the user:
1. Crucible strategic reflection was completed (Storyteller responded to all reflection prompts)
2. All three Phase 3 critics (Gauge + Assayer + Wanderer) must have returned PASS, OR iteration cap was reached with a "Known Issues" section attached
3. At least one full visual QA pass was completed (rendered images inspected)
4. Final PPTX opens without corruption

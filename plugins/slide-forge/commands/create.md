---
description: Create a new PowerPoint presentation in Slide Forge lab style from source materials
---

# Create Presentation

Create a new Slide Forge-style PowerPoint presentation based on the user's request.

## Input

$ARGUMENTS

## Procedure

**Step 1: Choose orchestration mode**
- If you can spawn agents (Task tool available): read the **slide-foundry** skill and follow its orchestration procedure.
- If you cannot spawn agents: read the **slide-anvil** skill and self-execute all phases.

**Step 2: Execute the workflow**

With agents (slide-foundry):
1. Spawn `slide-smith` with user request + source materials → produces slide plan
2. Spawn `slide-gauge` + `slide-assayer` on the plan → get PASS/FAIL verdicts
3. If FAIL: pass merged feedback to slide-smith → revise → re-critique
4. After plan PASS: slide-smith builds PPTX → extract text + render images
5. Spawn critics on extracted text + rendered images → get PASS/FAIL
6. Iterate until both PASS or **iteration cap reached (default: 3)**

Without agents (slide-anvil):
- Phase 0: Read sources → Phase 1: Plan → Phase 2: Build → Phase 3: QA

## Output

Deliver the final `.pptx` file and rendered slide images for verification.

## Pre-Flight Checks
Before starting the workflow:
1. Verify source materials are accessible (file paths exist, URLs respond)
2. Confirm output path is writable
3. If source materials are ambiguous or insufficient, ask the user for clarification before proceeding

## Completion Gate
Before delivering to the user:
1. Both critics (Gauge + Assayer) must have returned PASS, OR iteration cap was reached with a "Known Issues" section attached
2. At least one full visual QA pass was completed (rendered images inspected)
3. Final PPTX opens without corruption (validate.py passes if available)

---
description: Reforge an existing PowerPoint presentation following Slide Forge conventions
---

# Reforge Presentation

Reforge (edit or improve) an existing PowerPoint presentation following Slide Forge conventions.

## Input

$ARGUMENTS

## Procedure

**Step 1: Choose orchestration mode**
- If you can spawn agents (Task tool available): read the **slide-foundry** skill and follow its orchestration procedure.
- If you cannot spawn agents: read the **slide-anvil** skill and self-execute all phases.

**Step 2: Execute the workflow**

With agents (slide-foundry):
1. Spawn `slide-smith` with user request + existing PPTX → analyzes and plans edits
2. Spawn `slide-gauge` + `slide-assayer` on the edit plan → get PASS/FAIL verdicts
3. If FAIL: pass merged feedback to slide-smith → revise → re-critique
4. After plan PASS: slide-smith executes edits (unpack → edit → clean → pack) → extract text + render images
5. Spawn critics on extracted text + rendered images → get PASS/FAIL
6. Iterate until both PASS or **iteration cap reached (default: 3)**

Without agents (slide-anvil):
1. Analyze existing presentation (`markitdown` for text, `thumbnail.py` for layouts)
2. Plan changes → Unpack → Edit slides → Clean → Pack
3. Visual QA (render → inspect → fix → repeat)

## Output

Deliver the updated `.pptx` file and rendered slide images for verification.

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

## Edit-Specific Validation
1. Before editing: extract current slide text and thumbnail grid for baseline comparison
2. After editing: diff extracted text against baseline to verify intended changes and catch unintended modifications
3. Preserve all slides not targeted for editing -- verify untouched slide count matches

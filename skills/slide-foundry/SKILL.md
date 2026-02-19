---
name: slide-foundry
description: "Create or edit PowerPoint (.pptx) presentations in Slide Forge style by delegating to other agents. Use this only if you can spawn agents."
---

# Slide Foundry — Orchestration Skill

## Purpose
This is a **skill** that orchestrates Slide Forge-style PowerPoint creation/editing using:
- `slide-smith` (agent): plans, builds, revises the deck.
- `slide-gauge` (agent): enforces formatting/structure rules (syntax).
- `slide-assayer` (agent): enforces content quality, narrative coherence, and reader comprehension (semantics).

If the runtime cannot spawn agents, this skill **must self-execute** the same procedure by role-playing Slide-Smith / Slide-Gauge / Slide-Assayer sequentially, with the same pass/fail gates.

## When to Use
Use this skill whenever the user requests:
- new PPT/PPTX generation, or
- editing/improving an existing deck, or
- enforcing Slide Forge slide conventions, or
- iterative critique-driven refinement.

## Orchestration Entry Points

This skill is invoked via:
- `/slide-forge:create` command (new presentation)
- `/slide-forge:edit` command (editing existing presentation)
- Automatic detection when user requests PPTX work

The **caller** (the agent processing the user's request) acts as supervisor:
1. Reads this skill's procedure
2. Spawns agents via the Task tool: `Task(subagent_type="slide-smith", prompt="...")`
3. Collects artifacts (PPTX file, extracted text, rendered images) from slide-smith
4. Spawns critics with artifacts: `Task(subagent_type="slide-gauge", prompt="[artifacts]")` and `Task(subagent_type="slide-assayer", prompt="[artifacts]")` — these can run in parallel
5. Merges critic feedback and passes back to slide-smith for revision
6. Repeats until both critics PASS or iteration cap reached

## Inputs / Outputs Contract
Inputs may include:
- user prompt + constraints,
- source docs/figures/data,
- existing PPTX (if editing).

Outputs must include:
- the PPTX file,
- and (for critique) **extractable evidence**:
  - text extraction (e.g., markitdown output) and/or
  - rendered slide images (PNG) for visual QA.

## Orchestration Procedure (Agent-Spawn Available)
This skill runs an iterative actor-critic loop. The supervisor (caller) should:
1. Spawn `slide-smith` with:
   - user request,
   - source materials,
   - and this skill's hard constraints.
2. Slide-Smith produces:
   - a slide plan in the Slide Forge bullet syntax,
   - then a first PPTX draft,
   - plus extraction/render evidence.
3. Spawn `slide-gauge` on the plan + extracted text + slide images.
   - Output must be **PASS** or **FAIL**, with concrete diffs and rule references.
4. Spawn `slide-assayer` on the same artifacts.
   - Output must be **PASS** or **FAIL**, with actionable rewrite guidance.
5. If either critic returns **FAIL**, Slide-Smith must revise and re-submit.
6. Stop only when **both critics PASS**, or when iteration cap is reached.
   - Default cap: 3 iterations (raise if requested).
   - If cap reached: ship best version plus an explicit "Known Issues" section.

## Fallback Procedure (No Agent Spawning)
If agent spawning is unavailable, the skill must self-run in three internal passes per iteration:

Iteration loop (max 3 by default):
A. **Slide-Smith pass**:
   - produce/modify slide plan using the Slide Forge syntax,
   - implement PPTX changes,
   - export evidence (text extraction + slide renders).
B. **Slide-Gauge pass**:
   - validate all hard constraints and formatting rules,
   - produce PASS/FAIL + fix list (must be mechanically checkable).
C. **Slide-Assayer pass**:
   - validate reader-comprehension, narrative flow, depth ("so what"), jargon control,
   - produce PASS/FAIL + rewrite directives.

Only commit final output when both B and C are PASS, or cap reached.

**Bias mitigation for self-execution:**
- When switching to Gauge or Assayer role, do NOT re-read your own plan or code.
- Work ONLY from extracted evidence: `markitdown` output and rendered slide images.
- Pretend you see these slides for the first time. If you think "I know what I meant here," the slide is unclear — flag it.
- Apply the same PASS/FAIL threshold as if reviewing someone else's work.

## Phase-Specific Critic Inputs

| Phase | Critic receives | Required |
|-------|----------------|----------|
| Phase 1 (Plan) | Text plan in Slide Forge bullet syntax | Plan text only |
| Phase 2 (Post-build) | Extracted text (`markitdown`) + Rendered slide images (PNG) | Both required |
| Phase 3 (QA fix) | Updated extracted text + Updated rendered images | Both required |

**Rules:**
- Never send critics raw source code (PptxGenJS `.js` files). Always send extractable evidence.
- If rendering is unavailable, send extracted text only and note that visual QA is deferred.
- Always include the full slide plan alongside extracted text for context.

**Input preparation checklist (supervisor responsibility):**
- Phase 1: Extract the plan text. Send to both critics with a note: "Phase 1 -- plan text only, no images."
- Phase 2+: Run `markitdown` AND `render_slides.py`. Send BOTH outputs to critics. If rendering is unavailable, send text only with a note that visual QA is deferred.
- Never send raw PptxGenJS source code to critics.

## Feedback Delivery Format (Critic → Actor)

When passing Critic output back to the Actor for revision, use this structure:

```
## Iteration N Feedback

### Slide-Gauge: [PASS|FAIL]
[Full Slide-Gauge output — verdict, slide-by-slide issues, fix instructions, minimum patch]

### Slide-Assayer: [PASS|FAIL]
[Full Slide-Assayer output — verdict, prioritized issues, slide-by-slide critique, flow repair]

### Required Actions (merged, deduplicated, with issue IDs)
1. [G-01] [Slide N]: [concrete action] — NEW
2. [A-03] [Slide M]: [concrete action] — RECURRING (from iteration N-1)
...

### Regression Alert (if any)
Items that were PASS in iteration N-1 but FAIL in iteration N:
- [G-02] [Slide K]: [what regressed and likely cause]
```

Issue ID format:
- `G-##` for Slide-Gauge issues, `A-##` for Slide-Assayer issues.
- IDs persist across iterations. Reuse the same ID when the same issue recurs.
- Tag each item: `NEW` (first appearance), `RECURRING` (seen before, not fixed), `REGRESSED` (was PASS, now FAIL).

Rules:
- Pass **both** Critic outputs to the Slide-Smith unabridged. Do not summarize or filter — the Slide-Smith needs full context to avoid regressions.
- Append a **merged action list** that deduplicates overlapping issues and orders them by slide number.
- If a Slide-Assayer fix would require a Slide-Gauge violation, note it in the merged list with the resolution: "restructure (split slide / adjust heading)" — never compromise Syntax rules.
- The Slide-Smith must address **every item** in the merged action list before re-submitting.

## Iteration Termination

- **Success**: both Critics return PASS → ship the deck.
- **Cap reached** (default 3 iterations): ship the best version. Attach a "Known Issues" section listing all unresolved FAIL items from the final Critic pass.
- **No progress**: if the same issue IDs (`G-##` or `A-##`) remain tagged `RECURRING` across 2 consecutive iterations with no meaningful change in the fix attempt, escalate to the user rather than looping further.
- **Regression detected**: if a previously PASS item becomes FAIL (tagged `REGRESSED`), prioritize it above all `NEW` issues in the next iteration. If 3+ items regress in a single iteration, pause and escalate to the user — the revision strategy may need rethinking.

## Critic Priority Rules (How Conflicts Resolve)
- Syntax violations must be fixed first (structure is non-negotiable).
- Semantic improvements must not break syntax rules.
- If a semantic fix would force a syntax violation, restructure content (split slides, adjust headings) rather than violating the format.

## Minimal Acceptance Checklist (Quick Gate)
Before declaring "done", verify all rules in [rules.md](../slide-anvil/references/rules.md) are met.

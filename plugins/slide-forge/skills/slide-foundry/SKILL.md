---
name: slide-foundry
description: "Create or edit PowerPoint (.pptx) presentations in Slide Forge style by delegating to Storyteller, Smith, and Critics."
---

# Slide Foundry — Orchestration Skill

## Purpose

This is a **skill** that orchestrates Slide Forge-style PowerPoint creation/editing using:
- `slide-storyteller` (agent): researches, collects sources, writes academic-quality narrative, compresses to bullet plan.
- `slide-smith` (agent): builds PPTX from the bullet plan and visual spec.
- `slide-crucible` (agent): challenges strategic choices and provokes reflection on alternatives (strategy).
- `slide-gauge` (agent): enforces formatting/structure rules (syntax).
- `slide-assayer` (agent): enforces content quality, narrative coherence, and reader comprehension (semantics).
- `slide-wanderer` (agent): simulates a naive reader evaluating audience comprehension without source context (Phase 3 only).

If the runtime cannot spawn agents, redirect to the `slide-anvil` skill which includes the [Enhanced Smith Fallback](../slide-anvil/SKILL.md#enhanced-smith-fallback-workflow) procedure.

## When to Use

Use this skill whenever the user requests:
- new PPT/PPTX generation, or
- editing/improving an existing deck, or
- enforcing Slide Forge slide conventions, or
- iterative critique-driven refinement.

## Orchestration Entry Points

This skill is invoked via:
- `/slide-forge:forge` command (new presentation)
- `/slide-forge:reforge` command (editing existing presentation)
- Automatic detection when user requests PPTX work

The **caller** (the agent processing the user's request) acts as supervisor and coordinates all agents through the `.slide-forge/` shared workspace.

## Shared Workspace (`.slide-forge/`)

All agents communicate through files in the `.slide-forge/` directory. The supervisor creates this directory in Phase 0.

```
.slide-forge/
├── config.json                    # Session config (topic, audience, purpose)
├── sources/                       # Storyteller's collected materials
│   ├── user-provided/             # User's source files
│   ├── web/                       # Web search results
│   ├── images/                    # Collected images
│   └── source-index.json          # Source registry
├── narrative/                     # Storyteller's outputs
│   ├── narrative-full.md          # Integrated narrative (meta + outline + prose)
│   ├── slide-plan.md              # Bullet-compressed plan
│   └── visual-spec.md             # Per-slide visual specs
├── build/                         # Smith's outputs
│   ├── create_slides.py           # Generated Python script
│   ├── output.pptx                # Generated PPTX
│   ├── extracted-text.md          # markitdown extracted text (Phase 3)
│   ├── figures/                   # Code-generated visualization PNGs
│   └── rendered/                  # Rendered slide images
└── feedback/                      # Critics' outputs
    ├── crucible-report.md         # Strategic reflection
    ├── gauge-report.md            # Syntax/structure report
    ├── assayer-report.md          # Semantic/depth report
    ├── wanderer-report.md         # Naive reader comprehension report (Phase 3 only)
    ├── merged-actions.md          # Merged fix instructions
    └── smith-escalation.md        # Smith's escalation report (when content changes needed)
```

## Reference Files

Agents reference rules, style guides, and API docs via relative links in their definitions. When spawning agents, include the relevant **absolute paths** so the agent can read them directly without searching:

| Reference | Path | Used by |
|-----------|------|---------|
| Rules (canonical) | `plugins/slide-forge/references/rules.md` | Storyteller, Gauge, Assayer |
| Style guide | `plugins/slide-forge/references/style-guide.md` | Gauge, Assayer |
| Narrative format | `plugins/slide-forge/references/narrative-format.md` | Storyteller |
| Phase 1 examples | `plugins/slide-forge/references/phase1-examples.md` | Storyteller |
| Slide-forge API | `plugins/slide-forge/skills/slide-anvil/slide-forge-api.md` | Smith (via `slide-anvil` skill) |

Include the relevant paths in the spawn prompt. Example:
```
Reference files:
- Rules: plugins/slide-forge/references/rules.md
- Narrative format: plugins/slide-forge/references/narrative-format.md
- Phase 1 examples: plugins/slide-forge/references/phase1-examples.md
```

Smith loads the `slide-anvil` skill which links to `slide-forge-api.md`. As a fallback, the Supervisor SHOULD also include the absolute path `plugins/slide-forge/skills/slide-anvil/slide-forge-api.md` in Smith's spawn prompt, in case the skill fails to load at runtime.

## Spawn Prompt Quick Reference

Use this table when constructing spawn prompts. Each row lists exactly what to include. Detailed phase logic remains in the Orchestration Procedure below. If this table and the procedure conflict, the **procedure section is authoritative**.

| Agent | Phase | Input files | Reference files | Key instruction | Exclude |
|-------|-------|-------------|-----------------|-----------------|---------|
| Storyteller | 1a (narrative) | `config.json`, source file paths | `rules.md`, `narrative-format.md`, `phase1-examples.md` | "Execute Phase 0 + 1a. Stop after `narrative-full.md`." | -- |
| Storyteller | 1a (post-Crucible, DEEPEN) | `crucible-report.md` | `rules.md`, `narrative-format.md`, `phase1-examples.md` | "Read crucible report. Execute Phase 1b + 1c + 1d." | -- |
| Storyteller | 1a (post-Crucible, PROCEED) | `crucible-report.md` | `rules.md`, `narrative-format.md`, `phase1-examples.md` | "Execute Phase 1c + 1d." | -- |
| Storyteller | 1b (revision) | `merged-actions.md` | `rules.md`, `narrative-format.md`, `phase1-examples.md` | "Fix flagged issues. Do NOT rewrite unflagged slides." | -- |
| Storyteller | 3 (escalation) | `smith-escalation.md`, `slide-plan.md`, `visual-spec.md` | -- | "Revise only affected slides." | -- |
| Crucible | 1a | `narrative-full.md` | -- | -- | -- |
| Gauge | 1b | `slide-plan.md` | `rules.md`, `style-guide.md` | "Phase 1 -- plan text only, no images." | -- |
| Gauge | 3 | `extracted-text.md`, rendered images, `slide-plan.md` | `rules.md`, `style-guide.md` | -- | -- |
| Assayer | 1b | `narrative-full.md`, `slide-plan.md` | `rules.md`, `style-guide.md` | "Phase 1 -- narrative + plan text, no images." | -- |
| Assayer | 3 | `extracted-text.md`, rendered images, `slide-plan.md` | `rules.md`, `style-guide.md` | -- | -- |
| Wanderer | 3 | `extracted-text.md`, rendered images | -- | "Naive reader. Evaluate from slides alone." | `slide-plan.md`, `narrative-full.md`, `visual-spec.md`, all source files |
| Smith | 2 (build) | `slide-plan.md`, `visual-spec.md`, `sources/images/` | (via `slide-anvil` skill; fallback: `slide-forge-api.md`) | -- | -- |
| Smith | 3 (revision) | `merged-actions.md`, `slide-plan.md`, `visual-spec.md` | (via `slide-anvil` skill; fallback: `slide-forge-api.md`) | "Fix flagged issues. Do NOT rebuild unflagged slides." | -- |

**Wanderer isolation rule**: Wanderer's spawn prompt must be constructed independently -- never copy from Gauge/Assayer and edit. See [Wanderer Input Safeguard](#phase-3-build-quality-gate) in Phase 3.

**Reforge note**: For content-only reforge (`/reforge` with content changes but no template change), the Supervisor skips Phase 1 and spawns Smith directly at Phase 2. The Smith rows above apply. See the Reforge section in the Orchestration Procedure for the full content-only reforge flow.

---

## Inputs / Outputs Contract

Inputs may include:
- user prompt + constraints,
- source docs/figures/data,
- existing PPTX (if editing).

Outputs must include:
- the PPTX file (`.slide-forge/build/output.pptx`),
- rendered slide images (`.slide-forge/build/rendered/`),
- and (for critique) **extractable evidence**:
  - text extraction (`markitdown` output)
  - rendered slide images (PNG) for visual QA.

---

## Orchestration Procedure

### Phase 0: Setup

1. Check if `.slide-forge/` already exists:
   - **Exists**: Ask the user: "이어서 진행하시겠습니까, 새로 시작하시겠습니까?"
   - **New**: Create the directory structure above.
2. Write `.slide-forge/config.json` with topic, audience, purpose, source paths from user input.
3. Copy user-provided source files to `.slide-forge/sources/user-provided/`.

### Phase 1a: Storytelling + Strategic Reflection

1. **[Spawn Storyteller — Phase 0 + 1a]** Spawn `slide-storyteller` with:
   - user request,
   - `.slide-forge/config.json` path,
   - source file paths,
   - reference paths: `rules.md`, `narrative-format.md`, `phase1-examples.md` (see [Reference Files](#reference-files)).
   - Instruction: "Execute Phase 0 (source collection) and Phase 1a (narrative writing). Stop after writing `narrative-full.md`. Do NOT proceed to bullet compression."
2. **[Artifact Validation Gate]**: Verify `narrative-full.md` exists and contains at least one `## Slide` header.
3. Spawn `slide-crucible` with path to `.slide-forge/narrative/narrative-full.md`.
   - Output is **DEEPEN** or **PROCEED**, saved to `.slide-forge/feedback/crucible-report.md`.
4. If **DEEPEN**: **[Spawn Storyteller — Phase 1b + 1c + 1d]** Spawn `slide-storyteller` with:
   - reference paths: `rules.md`, `narrative-format.md`, `phase1-examples.md` (see [Reference Files](#reference-files)).
   - Instruction: "Read crucible report at `.slide-forge/feedback/crucible-report.md`. Execute Phase 1b (reflection response), Phase 1c (bullet compression), Phase 1d (visual spec)."
   - Storyteller must respond to every reflection prompt (Maintain/Adopt/Synthesize) and revise narrative if needed. Re-run crucible only if the narrative changed substantially (max 1 re-run).
5. If **PROCEED**: **[Spawn Storyteller — Phase 1c + 1d]** Spawn `slide-storyteller` with:
   - reference paths: `rules.md`, `narrative-format.md`, `phase1-examples.md` (see [Reference Files](#reference-files)).
   - Instruction: "Crucible returned PROCEED. Note the reasoning in `.slide-forge/feedback/crucible-report.md`, then execute Phase 1c (bullet compression) and Phase 1d (visual spec)."
6. **[Artifact Validation Gate]**: Verify `slide-plan.md` exists with at least one `[Major Title]` + `▌` block. Verify `visual-spec.md` exists.

### Phase 1b: Narrative Quality Gate

7. Spawn `slide-gauge` with path to `.slide-forge/narrative/slide-plan.md`.
   - Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
   - Note to agent: "Phase 1 — plan text only, no images."
   - Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/gauge-report.md`.
8. Spawn `slide-assayer` with paths to `.slide-forge/narrative/narrative-full.md` and `slide-plan.md` (can run in parallel with gauge).
   - Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
   - Note to agent: "Phase 1 — narrative + plan text, no images."
   - Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/assayer-report.md`.
9. If either critic returns **FAIL**: merge feedback into `.slide-forge/feedback/merged-actions.md`, **[Spawn Storyteller — Phase 1b revision]** with:
   - path to `.slide-forge/feedback/merged-actions.md`,
   - reference paths: `rules.md`, `narrative-format.md`, `phase1-examples.md` (see [Reference Files](#reference-files)),
   - Instruction: "Read merged critic feedback. Execute Phase 1b critic revision: fix flagged issues in `slide-plan.md`, `visual-spec.md`, and `narrative-full.md` as needed. Do NOT rewrite unflagged slides."
   - Re-submit to gauge + assayer. Max 3 iterations.

#### Phase 1b Cap Behavior

If Phase 1b reaches the iteration cap (3 iterations) without both critics returning PASS:
- **Proceed to Phase 2** with the best available version of `slide-plan.md` and `visual-spec.md`.
- Attach a "Phase 1b Known Issues" note to `config.json` listing all unresolved FAIL items from the final Gauge/Assayer reports.
- Smith receives these known issues as context and should avoid exacerbating them.
- Phase 3 critics will independently re-evaluate the built PPTX — some Phase 1b issues may resolve during build, others may persist and appear in Phase 3 feedback.

### Phase 2: Build

10. After Phase 1b PASS: Spawn `slide-smith` with paths to:
    - `.slide-forge/narrative/slide-plan.md`
    - `.slide-forge/narrative/visual-spec.md`
    - `.slide-forge/sources/images/`
11. Smith builds PPTX, renders, performs self-QA (1 round).
12. **[Artifact Validation Gate]**: Verify `output.pptx` exists in `.slide-forge/build/`. Verify PNG count in `rendered/` equals `expected_slide_count` from `config.json`. If fewer, Smith must re-render before proceeding.

### Phase 3: Build Quality Gate

13. Run `markitdown` on `.slide-forge/build/output.pptx` and save output to `.slide-forge/build/extracted-text.md`.
    ```bash
    uv run python -m markitdown .slide-forge/build/output.pptx > .slide-forge/build/extracted-text.md
    ```
14. Spawn Phase 3 critics **in parallel**, passing `.slide-forge/build/extracted-text.md` as the extracted text source:

    **Gauge and Assayer** (can run in parallel):
    - `slide-gauge` with `extracted-text.md` + rendered image paths + `slide-plan.md` (context).
      Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
      Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/gauge-report.md`.
    - `slide-assayer` with `extracted-text.md` + rendered image paths + `slide-plan.md` (context).
      Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
      Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/assayer-report.md`.

    **Wanderer** (runs in parallel with above, but uses a DIFFERENT input set):

    Construct this spawn prompt FROM SCRATCH -- do NOT copy from the Gauge/Assayer block above.

    - `slide-wanderer` with ONLY these inputs:
      1. `extracted-text.md`
      2. Rendered image paths (`rendered/slide-*.png`)
    - NO reference files. NO `slide-plan.md`. NO `narrative-full.md`. NO `visual-spec.md`. NO source files.
    - Note to agent: "You are a naive reader. Do NOT read `narrative-full.md`, `slide-plan.md`, or any source documents. Evaluate audience comprehension from the slides alone."
    - Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/wanderer-report.md`.
15. **[Critic Synchronization Barrier]**: Before merging, the Supervisor MUST verify that ALL parallel critics have completed and their report files exist:
    - Confirm `gauge-report.md`, `assayer-report.md`, and `wanderer-report.md` all exist in `.slide-forge/feedback/`.
    - Confirm each report file is non-empty and contains a verdict line (`PASS` or `FAIL`).
    - If any report is missing or incomplete, wait for the critic to finish before proceeding. Do NOT merge with partial reports — this produces incorrect deduplication and tagging.
16. If any critic returns **FAIL**: merge feedback into `.slide-forge/feedback/merged-actions.md`, pass to Smith for revision.
17. **[Escalation Check]**: After Smith revision, check if `.slide-forge/feedback/smith-escalation.md` exists and is non-empty.
    - **No escalation**: re-submit to critics (step 14).
    - **Escalation exists**: **[Spawn Storyteller — Phase 3 targeted revision]** with:
      - paths to `smith-escalation.md`, `slide-plan.md`, `visual-spec.md`
      - Instruction: "Read escalation report. Revise only affected slides in `slide-plan.md` and `visual-spec.md`. Do NOT rewrite unaffected slides."
      - After Storyteller revision, re-spawn Smith to rebuild from revised plan.
      - Delete `smith-escalation.md`, then re-submit to critics (step 14).
18. Max 3 iterations total (escalation counts as part of the iteration, not a separate loop). See [Iteration Counter Definition](#iteration-counter-definition) for what constitutes one iteration.

### Phase 4: Delivery

19. When all three Phase 3 critics PASS (or iteration cap reached — see [Advisory Downgrade Gate Rule](#advisory-downgrade-gate-rule)):
    - Deliver `.slide-forge/build/output.pptx` to the user.
    - If cap was reached, attach a "Known Issues" section from the final critic reports.

**Important notes:**
- `slide-crucible` runs only in Phase 1a (strategic reflection). It does NOT participate in Phase 1b/2/3 iteration loops.
- `slide-wanderer` runs only in Phase 3 (post-build). It does NOT participate in Phase 1b. It must NOT receive `narrative-full.md`, `slide-plan.md`, or source documents.
- Phase 3 escalation to Storyteller is limited to targeted slide revisions — it does not re-trigger Crucible or Phase 1b critics.
- Always pass file **paths** to agents, not file contents, to avoid stale-read issues.
- After any agent writes to `.slide-forge/`, instruct the next agent to read the file directly (not from cached prompt content).
- Always include **reference file paths** (from the [Reference Files](#reference-files) section) when spawning agents. Agents cannot resolve relative links in their own definitions — they need absolute paths to read rules, style guides, and format specs.

---

## Artifact Validation Gates

Lightweight checks the supervisor runs before phase transitions:

| Transition | Validation |
|------------|-----------|
| Phase 1a: narrative → Crucible | `narrative-full.md` exists, contains `## Slide` header(s). **Completeness**: count `## Slide` headers — record as `expected_slide_count` in `config.json`. |
| Phase 1a: compression → Phase 1b | `slide-plan.md` exists with `[Major Title]` + `▌` block(s). `visual-spec.md` exists. **Completeness**: count `[Major Title]` blocks in `slide-plan.md` — must match `expected_slide_count` from narrative. |
| Phase 1b → Phase 2 | Gauge PASS + Assayer PASS (or Phase 1b iteration cap reached — see [Phase 1b Cap Behavior](#phase-1b-cap-behavior)) |
| Phase 2 → Phase 3 | `output.pptx` exists in `.slide-forge/build/`. **Completeness**: count PNGs in `rendered/` — must equal number of `[Major Title]` blocks in `slide-plan.md`. If count mismatches, Smith must re-render before proceeding. |
| Phase 3 → Phase 4 | Gauge PASS + Assayer PASS + Wanderer PASS (or all blocking items resolved — see [Advisory Downgrade Gate Rule](#advisory-downgrade-gate-rule)) |

### Slide Count Derivation

The Supervisor derives and tracks `expected_slide_count` to prevent incomplete artifacts from passing gates:

1. **Source of truth**: Count `## Slide` headers in `narrative-full.md` after Phase 1a completes. Store in `config.json` as `expected_slide_count`.
2. **Phase 1a → 1b**: Count `[Major Title]` blocks in `slide-plan.md`. Must equal `expected_slide_count`. If fewer, Storyteller omitted slides — block transition and request completion.
3. **Phase 2 → 3**: Count PNG files in `rendered/`. Must equal `expected_slide_count`. If fewer, Smith's render was partial — block transition and request re-render.
4. **Phase 3 critics**: Each critic should verify they received evidence for all slides. If `extracted-text.md` contains fewer slide sections than expected, flag it in their report.

---

## Stale-Read Prevention Protocol

Agents may cache file contents from their prompt context. To prevent this:
1. Always pass **file paths** to agents, not inline file content.
2. Instruct each agent: "Read the file at [path] directly — do not rely on any previously seen content."
3. When `config.json` has a `phases` field with timestamps, verify the timestamp is current before passing to the next agent.

---

## Phase-Specific Critic Inputs

| Phase | Gauge receives | Assayer receives | Wanderer receives |
|-------|---------------|-----------------|-------------------|
| Phase 1b (Plan) | `slide-plan.md` (text only) | `narrative-full.md` + `slide-plan.md` (text only) | *(does not run in Phase 1b)* |
| Phase 3 (Post-build) | `extracted-text.md` + Rendered images (PNG) + `slide-plan.md` (context) | `extracted-text.md` + Rendered images (PNG) + `slide-plan.md` (context) | `extracted-text.md` + Rendered images (PNG) only — NO `narrative-full.md`, NO `slide-plan.md`, NO source docs |

**Rules:**
- Never send critics raw source code (`.py` script files). Always send extractable evidence.
- If rendering is unavailable, send extracted text only and note that visual QA is deferred.
- Always include `slide-plan.md` alongside extracted text for context in Phase 3.
- Never send raw Python source code to critics.

> **IMPORTANT**: When spawning Wanderer in Phase 3, the Supervisor MUST NOT copy the Gauge/Assayer spawn prompt and reuse it for Wanderer. Gauge and Assayer receive `slide-plan.md` as context; Wanderer must NOT. Construct the Wanderer spawn prompt independently using only `extracted-text.md` and rendered image paths.

---

## Feedback Delivery Format

### Crucible Feedback (Phase 1a — Strategic Reflection)

When passing Crucible output back to the Storyteller, use this structure:

```
## Strategic Reflection Feedback

### Slide-Crucible: [DEEPEN|PROCEED]
[Full Crucible output — implicit strategy, challenges, reflection prompts, alternative sketch]

### Response Required
Storyteller must respond to EVERY reflection prompt below:
1. [prompt] → Storyteller: [reasoning]
2. [prompt] → Storyteller: [reasoning]
...

### Plan Revision Summary
[What changed and why, or explicit defense of current approach]
```

The Storyteller's response is part of the narrative artifact — it documents the strategic reasoning behind the deck. This reasoning is visible to Gauge and Assayer for context but is not subject to their PASS/FAIL criteria. Wanderer does NOT receive this reasoning (it must remain a naive reader).

### Feedback Delivery and Merge (Phase 1b/3 -- Quality Iteration)

When passing Critic output back to the Actor (Storyteller in Phase 1b, Smith in Phase 3) for revision, use this structure. In Phase 1b, only Gauge and Assayer sections are present. In Phase 3, all three critics are included:

```
## Iteration N Feedback

### Slide-Gauge: [PASS|FAIL]
[Full Slide-Gauge output -- verdict, slide-by-slide issues, fix instructions, minimum patch]

### Slide-Assayer: [PASS|FAIL]
[Full Slide-Assayer output -- verdict, prioritized issues, slide-by-slide critique, flow repair]

### Slide-Wanderer: [PASS|FAIL] (Phase 3 only)
[Full Slide-Wanderer output -- verdict, comprehension summary, slide-by-slide notes, concept introduction map]
```

Rules:
- Pass **all** Critic outputs to the Actor unabridged. Do not summarize or filter -- the Actor needs full context to avoid regressions.
- If a Slide-Assayer fix would require a Slide-Gauge violation, note it in the merged list with the resolution: "restructure (split slide / adjust heading)" -- never compromise Syntax rules.
- **Wanderer conflict downgrade**: If a Wanderer fix would conflict with a Gauge or Assayer constraint, downgrade the Wanderer item to advisory (include in "Advisory" section, not blocking). Gauge and Assayer fixes always take priority.
- The Actor must address **every item** in the merged action list before re-submitting.

#### Feedback Merge Procedure

The Supervisor follows these three steps to produce `merged-actions.md`. The goal is a prioritized action list, not a perfectly deduplicated merge -- the Actor (Smith/Storyteller) handles overlapping items naturally when fixing.

**Step 1 -- Collect and label**: Read each critic report. Copy every actionable item (anything requiring a fix) into a flat list. Label each with a sequential number, its source, and the slide number:
```
#1 [Slide N] [G]: [issue + fix instruction from Gauge]
#2 [Slide N] [A]: [issue + fix instruction from Assayer]
#3 [Slide N] [W]: [issue + fix instruction from Wanderer]  (Phase 3 only)
```
Sequential numbers (`#1`, `#2`, ...) reset each iteration. They exist only to make cross-iteration comparison possible (see Step 2 and Termination Rules).

**Step 2 -- Apply priority rules**: Review the collected list and apply these three rules:
1. **Wanderer conflicts**: If a Wanderer item [W] on a slide would contradict a Gauge or Assayer item on the same slide, move the [W] item to an "Advisory" section at the bottom. Gauge and Assayer always win.
2. **Iteration tagging** (iteration 2+ only): Compare against the previous `merged-actions.md`. Match items across iterations by **slide number + source label** (e.g., an item on Slide 3 from [G] in iteration 1 corresponds to an item on Slide 3 from [G] in iteration 2 if it addresses the same underlying issue). Mark matched items as RECURRING (existed before, not fixed) or REGRESSED (was passing, now failing). New items need no tag.
3. **Sort**: REGRESSED items first, then RECURRING, then new items. Within each group, sort by slide number.

**Step 3 -- Write output**: Save to `.slide-forge/feedback/merged-actions.md` using this template:

```
## [Phase] Iteration [N] -- Merged Actions

### Required Actions
#1 [Slide 2] [G]: [fix instruction]
#2 [Slide 3] [A]: [fix instruction] -- RECURRING
#3 [Slide 5] [W]: [fix instruction]
...

### Regression Alert
(Items that were passing but now fail. If none: "None.")
- #4 [Slide 4] [G]: [what regressed] -- REGRESSED

### Advisory (not blocking)
(Wanderer items downgraded due to conflict with Gauge/Assayer. Omit section if none.)
- #5 [Slide 7] [W]: [issue] -- conflicts with Gauge rule on same slide
```

Before overwriting, rename the existing `merged-actions.md` to `merged-actions-iter-[N-1].md` to preserve history for iteration tagging.

**Important**: The unabridged critic reports remain in their individual files (`gauge-report.md`, `assayer-report.md`, `wanderer-report.md`). The Actor receives BOTH the individual reports AND `merged-actions.md`. The merged list tells the Actor what to fix and in what order; the individual reports provide full context for each fix.

Save the merged feedback to `.slide-forge/feedback/merged-actions.md`.

---

## Iteration Termination

### Iteration Counter Definition

An **iteration** is defined as one complete **critic execution round** — the cycle where all applicable critics run and produce reports. Activities between critic rounds (Smith rebuilds, Storyteller targeted revisions, escalation handling) are part of the current iteration, not separate iterations.

Example for Phase 3:
- Iteration 1: critics run → FAIL → Smith fixes → escalation → Storyteller revises → Smith rebuilds (all part of iteration 1)
- Iteration 2: critics re-run → FAIL → Smith fixes (all part of iteration 2)
- Iteration 3: critics re-run → PASS or cap reached

The counter increments only when critics are re-spawned (steps 7-8 in Phase 1b, step 14 in Phase 3).

### Termination Rules

- **Success**: all Phase 3 Critics (Gauge + Assayer + Wanderer) return PASS → ship the deck.
- **Cap reached** (default 3 iterations per phase): ship the best version. Attach a "Known Issues" section listing all unresolved FAIL items from the final Critic pass (including downgraded advisory items).
- **No progress**: if items with the same slide number and source label (e.g., `[Slide 3] [G]`) remain tagged `RECURRING` across 2 consecutive iterations with no meaningful change in the fix attempt, escalate to the user rather than looping further.
- **Regression detected**: if a previously PASS item becomes FAIL (tagged `REGRESSED`), prioritize it above all `NEW` issues in the next iteration. If 3+ items regress in a single iteration, pause and escalate to the user — the revision strategy may need rethinking.

### Advisory Downgrade Gate Rule

When all **blocking** items in `merged-actions.md` are resolved but **advisory** items remain (downgraded W-## items), the phase outcome depends on the critics' raw verdicts:
- If Gauge returns PASS and Assayer returns PASS, the phase is **PASS_WITH_ADVISORIES** — proceed to the next phase. Advisory items are included in the delivery as "Known Issues" but do not block progress.
- If Gauge or Assayer returns FAIL (regardless of Wanderer), the phase remains **FAIL** — continue iterating.
- Wanderer's verdict alone does not block phase transition if all its blocking items were downgraded to advisory during deconfliction. The Supervisor treats the Wanderer contribution as resolved once its blocking items are either fixed or downgraded.

## Critic Priority Rules (How Conflicts Resolve)

- Syntax violations (Gauge) must be fixed first (structure is non-negotiable).
- Semantic improvements (Assayer) must not break syntax rules.
- Comprehension fixes (Wanderer) must not break syntax rules or contradict Assayer's semantic standards.
- If a semantic or comprehension fix would force a syntax violation, restructure content (split slides, adjust headings) rather than violating the format.
- Priority order: Gauge (syntax) > Assayer (semantics) > Wanderer (comprehension).

---

## Reforge: Conditional Storyteller Invocation

When editing an existing presentation (`/slide-forge:reforge`), the supervisor first performs a **scope assessment**:

| Change Type | Examples | Storyteller? |
|-------------|----------|:------------:|
| Structural | Add/delete slides, reorder, restructure narrative arc | Yes (full pipeline from Phase 1a) |
| Content | Update data, fix text, replace visuals | No (Smith direct from Phase 2) |
| Ambiguous | Unclear scope | Ask user to clarify |

The first step in reforge is always: "이 변경은 구조적 변경(슬라이드 추가/삭제/순서변경)인가, 내용 수정(데이터 갱신/텍스트 교정)인가?"

- **Structural**: Run the full pipeline from Phase 1a.
- **Content**: Skip to Phase 2, but first run the **Artifact Freshness Check** below.

### Artifact Freshness Check (Content-Only Reforge)

Before Smith starts a content-only reforge, the Supervisor MUST verify that existing `.slide-forge/narrative/` artifacts match the current PPTX:

1. **Extract baseline**: Run `markitdown` on the existing PPTX to get current slide text.
2. **Compare slide count**: Count slides in the `markitdown` output and compare against `[Major Title]` blocks in `slide-plan.md`. If counts differ, the artifacts are stale.
3. **Compare slide titles**: Check that the title of each slide in the extracted text approximately matches the corresponding `[Major Title]` in `slide-plan.md`. Minor wording differences are acceptable; completely different titles indicate staleness.
4. **On mismatch**:
   - Warn the user: "기존 narrative artifacts와 현재 PPTX 사이에 불일치가 감지되었습니다. 구조적 변경 경로로 전환하시겠습니까?"
   - If user confirms: reroute to the **Structural** path (full pipeline from Phase 1a).
   - If user declines: proceed with content-only reforge, but note the mismatch as a known risk in `config.json`. Smith should use the extracted text as the primary reference, with `slide-plan.md` as secondary context only.
5. **On match**: proceed normally — Smith reads `slide-plan.md` and applies edits.

This check prevents Smith from working with stale plans that no longer reflect the actual deck content (e.g., after manual edits in PowerPoint).

---

## Fallback Procedure (No Agent Spawning)

If agent spawning is unavailable, redirect to the `slide-anvil` skill which includes the **Enhanced Smith Fallback Workflow**. See [slide-anvil SKILL.md](../slide-anvil/SKILL.md#enhanced-smith-fallback-workflow).

The Enhanced Smith fallback self-executes the same pipeline in role-switching steps:
1. Storyteller Mode → 2. Crucible Role → 3. Response → 4. Gauge Role → 5. Assayer Role → 6. Smith Mode → 7. Gauge + Assayer + Wanderer → 8. Fix loop

The same PASS/FAIL gates, iteration caps, and feedback formats defined above apply in fallback mode.

---

## Minimal Acceptance Checklist (Quick Gate)

Before declaring "done", verify all rules in [rules.md](../../references/rules.md) are met.

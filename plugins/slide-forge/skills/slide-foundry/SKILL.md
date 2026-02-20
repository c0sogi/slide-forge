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

### Phase 2: Build

10. After Phase 1b PASS: Spawn `slide-smith` with paths to:
    - `.slide-forge/narrative/slide-plan.md`
    - `.slide-forge/narrative/visual-spec.md`
    - `.slide-forge/sources/images/`
11. Smith builds PPTX, renders, performs self-QA (1 round).
12. **[Artifact Validation Gate]**: Verify `output.pptx` exists in `.slide-forge/build/`. Verify `rendered/` contains at least 1 PNG.

### Phase 3: Build Quality Gate

13. Run `markitdown` on `.slide-forge/build/output.pptx` and save output to `.slide-forge/build/extracted-text.md`.
    ```bash
    uv run python -m markitdown .slide-forge/build/output.pptx > .slide-forge/build/extracted-text.md
    ```
14. Spawn all three Phase 3 critics **in parallel**, passing `.slide-forge/build/extracted-text.md` as the extracted text source:
    - `slide-gauge` with `extracted-text.md` + rendered image paths + `slide-plan.md` (context).
      Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
      Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/gauge-report.md`.
    - `slide-assayer` with `extracted-text.md` + rendered image paths + `slide-plan.md` (context).
      Reference paths: `rules.md`, `style-guide.md` (see [Reference Files](#reference-files)).
      Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/assayer-report.md`.
    - `slide-wanderer` with `extracted-text.md` + rendered image paths only.
      **WANDERER INPUT SAFEGUARD — STOP AND VERIFY before spawning:**
      1. The spawn prompt for Wanderer MUST contain ONLY these file paths: `extracted-text.md` and rendered image paths (`rendered/slide-*.png`).
      2. The spawn prompt MUST NOT contain any of these: `slide-plan.md`, `narrative-full.md`, `visual-spec.md`, `source-index.json`, or any path under `.slide-forge/sources/`.
      3. If you are copy-pasting from the Gauge/Assayer spawn prompt above, DELETE `slide-plan.md` from the file list before sending.
      Note to agent: "You are a naive reader. Do NOT read `narrative-full.md`, `slide-plan.md`, or any source documents. Evaluate audience comprehension from the slides alone."
      Output: **PASS** or **FAIL**, saved to `.slide-forge/feedback/wanderer-report.md`.
15. If any critic returns **FAIL**: merge feedback into `.slide-forge/feedback/merged-actions.md`, pass to Smith for revision.
16. **[Escalation Check]**: After Smith revision, check if `.slide-forge/feedback/smith-escalation.md` exists and is non-empty.
    - **No escalation**: re-submit to critics (step 13).
    - **Escalation exists**: **[Spawn Storyteller — Phase 3 targeted revision]** with:
      - paths to `smith-escalation.md`, `slide-plan.md`, `visual-spec.md`
      - Instruction: "Read escalation report. Revise only affected slides in `slide-plan.md` and `visual-spec.md`. Do NOT rewrite unaffected slides."
      - After Storyteller revision, re-spawn Smith to rebuild from revised plan.
      - Delete `smith-escalation.md`, then re-submit to critics (step 13).
17. Max 3 iterations total (escalation counts as part of the iteration, not a separate loop).

### Phase 4: Delivery

18. When all three Phase 3 critics PASS (or iteration cap reached):
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
| Phase 1a: narrative → Crucible | `narrative-full.md` exists, contains `## Slide` header(s) |
| Phase 1a: compression → Phase 1b | `slide-plan.md` exists with `[Major Title]` + `▌` block(s). `visual-spec.md` exists |
| Phase 1b → Phase 2 | Gauge PASS + Assayer PASS |
| Phase 2 → Phase 3 | `output.pptx` exists in `.slide-forge/build/`. `rendered/` has 1+ PNG |
| Phase 3 → Phase 4 | Gauge PASS + Assayer PASS + Wanderer PASS |

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

### Gauge/Assayer/Wanderer Feedback (Phase 1b/3 — Quality Iteration)

When passing Critic output back to the Actor (Storyteller in Phase 1b, Smith in Phase 3) for revision, use this structure. In Phase 1b, only Gauge and Assayer sections are present. In Phase 3, all three critics are included:

```
## Iteration N Feedback

### Slide-Gauge: [PASS|FAIL]
[Full Slide-Gauge output — verdict, slide-by-slide issues, fix instructions, minimum patch]

### Slide-Assayer: [PASS|FAIL]
[Full Slide-Assayer output — verdict, prioritized issues, slide-by-slide critique, flow repair]

### Slide-Wanderer: [PASS|FAIL] (Phase 3 only)
[Full Slide-Wanderer output — verdict, comprehension summary, slide-by-slide notes, concept introduction map]

### Required Actions (merged, deduplicated, with issue IDs)
1. [G-01] [Slide N]: [concrete action] — NEW
2. [A-03] [Slide M]: [concrete action] — RECURRING (from iteration N-1)
3. [W-01] [Slide K]: [concrete action] — NEW
...

### Regression Alert (if any)
Items that were PASS in iteration N-1 but FAIL in iteration N:
- [G-02] [Slide K]: [what regressed and likely cause]
```

Issue ID format:
- `G-##` for Slide-Gauge issues, `A-##` for Slide-Assayer issues, `W-##` for Slide-Wanderer issues.
- IDs persist across iterations. Reuse the same ID when the same issue recurs.
- Tag each item: `NEW` (first appearance), `RECURRING` (seen before, not fixed), `REGRESSED` (was PASS, now FAIL).

Rules:
- Pass **all** Critic outputs to the Actor unabridged. Do not summarize or filter — the Actor needs full context to avoid regressions.
- Append a **merged action list** that deduplicates overlapping issues and orders them by slide number.
- **Deconfliction rule**: If Wanderer and Assayer flag the same slide for the same issue type (jargon, comprehension, transitions), keep only the Assayer item (higher priority). Wanderer items are unique only when they identify comprehension gaps that Assayer cannot detect (e.g., concept prerequisite ordering, visual self-explanatoriness, cognitive load).
- If a Slide-Assayer fix would require a Slide-Gauge violation, note it in the merged list with the resolution: "restructure (split slide / adjust heading)" — never compromise Syntax rules.
- **Wanderer conflict downgrade**: If a Wanderer fix (W-##) would conflict with a Gauge or Assayer constraint, downgrade the W-## item to advisory (include in "Known Issues" but not blocking). Gauge and Assayer fixes always take priority.
- The Actor must address **every item** in the merged action list before re-submitting.
- Save the merged feedback to `.slide-forge/feedback/merged-actions.md`.

### Feedback Merge Algorithm (Step-by-Step)

The Supervisor MUST follow this mechanical procedure when merging critic reports into `merged-actions.md`. Do not improvise — follow the steps in order.

**Inputs**: `gauge-report.md`, `assayer-report.md`, `wanderer-report.md` (Phase 3 only). In Phase 1b, only `gauge-report.md` and `assayer-report.md` are present — skip all Wanderer-related comparisons in Steps 2-3. If this is iteration 2+, also read the previous `merged-actions.md` for tagging in Step 4.

**Step 1 — Extract**: Read each critic report. For each issue found, create a raw entry:
```
[Source]-[NN] | Slide [N] | [issue description] | [fix instruction]
```
Where `[Source]` is `G` (Gauge), `A` (Assayer), or `W` (Wanderer). Number issues sequentially per source (G-01, G-02, ..., A-01, A-02, ..., W-01, W-02, ...).

**Step 2 — Deduplicate**: Compare all entries pairwise. Two entries are duplicates if they target the same slide AND describe the same issue type. When duplicates are found:
- If Gauge + Assayer overlap: keep the Gauge item (syntax priority), drop the Assayer item, note "merged with A-##".
- If Gauge + Wanderer overlap: keep the Gauge item, drop the Wanderer item, note "merged with W-##".
- If Assayer + Wanderer overlap on the same issue type (jargon, comprehension, transitions): keep the Assayer item (higher priority per Deconfliction Rule), drop the Wanderer item, note "merged with W-##".
- If Wanderer flags something that neither Gauge nor Assayer flagged (concept prerequisite ordering, visual self-explanatoriness, cognitive load): keep the Wanderer item — this is Wanderer's unique contribution.

**Step 3 — Deconflict**: Check each remaining Wanderer item (W-##) against all Gauge and Assayer constraints:
- If applying the W-## fix would violate a Gauge rule or contradict an Assayer fix: downgrade W-## to advisory. Mark it `[ADVISORY]` and move it to a "Known Issues" subsection at the bottom. It is not blocking.
- If no conflict exists: keep W-## as a required action.

**Step 4 — Tag iteration status** (skip for iteration 1):
- Compare each item against the previous `merged-actions.md`:
  - Item not present before: tag `NEW`
  - Item present before and not fixed: tag `RECURRING`
  - Item was PASS in previous iteration but is now FAIL: tag `REGRESSED`
- First iteration items are all tagged `NEW`.

**Step 5 — Sort**: Sort all required actions by:
1. Priority: `REGRESSED` first, then `RECURRING`, then `NEW`
2. Within each priority group: by slide number ascending
3. Within the same slide: Gauge items first, then Assayer, then Wanderer

**Step 6 — Format output**: Write `merged-actions.md` using this template. Note: `merged-actions.md` contains the merged action list only. The unabridged critic reports remain in their individual files (`gauge-report.md`, `assayer-report.md`, `wanderer-report.md`) and are passed separately to the Actor in the spawn prompt.

```
## Iteration [N] — Merged Actions

### Required Actions
1. [G-01] [Slide 2]: [concrete fix instruction] — NEW
2. [A-03] [Slide 3]: [concrete fix instruction] — RECURRING (iteration 1, 2)
3. [W-01] [Slide 5]: [concrete fix instruction] — NEW
...

### Regression Alert
Items that were PASS in iteration [N-1] but FAIL now:
- [G-02] [Slide 4]: [what regressed and likely cause]
(If no regressions: "None.")

### Known Issues (Advisory — not blocking)
- [W-03] [Slide 7]: [issue description] — downgraded: conflicts with [G-01]
(If no advisory items: omit this section.)

### Merge Log
- A-05 merged with W-02 (same slide, same issue type: jargon)
- W-04 downgraded to advisory (fix conflicts with Gauge rule: subtitle length)
(If no merges or downgrades: omit this section.)
```

**Step 7 — Save**: Write the completed output to `.slide-forge/feedback/merged-actions.md`. If a previous version exists, overwrite it entirely (the iteration number and tags preserve history).

---

## Iteration Termination

- **Success**: all Phase 3 Critics (Gauge + Assayer + Wanderer) return PASS → ship the deck.
- **Cap reached** (default 3 iterations per phase): ship the best version. Attach a "Known Issues" section listing all unresolved FAIL items from the final Critic pass (including downgraded W-## advisory items).
- **No progress**: if the same issue IDs (`G-##`, `A-##`, or `W-##`) remain tagged `RECURRING` across 2 consecutive iterations with no meaningful change in the fix attempt, escalate to the user rather than looping further.
- **Regression detected**: if a previously PASS item becomes FAIL (tagged `REGRESSED`), prioritize it above all `NEW` issues in the next iteration. If 3+ items regress in a single iteration, pause and escalate to the user — the revision strategy may need rethinking.

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
- **Content**: Skip to Phase 2. Smith reads existing `.slide-forge/narrative/` artifacts and applies the requested edits directly.

---

## Fallback Procedure (No Agent Spawning)

If agent spawning is unavailable, redirect to the `slide-anvil` skill which includes the **Enhanced Smith Fallback Workflow**. See [slide-anvil SKILL.md](../slide-anvil/SKILL.md#enhanced-smith-fallback-workflow).

The Enhanced Smith fallback self-executes the same pipeline in role-switching steps:
1. Storyteller Mode → 2. Crucible Role → 3. Response → 4. Gauge Role → 5. Assayer Role → 6. Smith Mode → 7. Gauge + Assayer + Wanderer → 8. Fix loop

The same PASS/FAIL gates, iteration caps, and feedback formats defined above apply in fallback mode.

---

## Minimal Acceptance Checklist (Quick Gate)

Before declaring "done", verify all rules in [rules.md](../../references/rules.md) are met.

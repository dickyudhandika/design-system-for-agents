---
name: ds4a
description: >-
  Design System for Agents — a reusable design library with swappable tones.
  Detects a project's existing design system (or starts from a neutral Base
  UI-style baseline), resolves core + tone + project overlay into DESIGN.md,
  reviews generated code, and merges approved rules back. Use for `/ds4a init`,
  `/ds4a tone`, `/ds4a review`, `/ds4a merge`, or when the user wants a design
  system for their AI agent.
version: 2.0.0
author: thenom4design
license: MIT
metadata:
  hermes:
    tags: [design-system, tones, design-md, agents, generator, taste, compounding]
    related_skills: [design-system-evolution, design-system-format-conversion, design-md, design-token-audit]
---

# ds4a — Design System for Agents

One library, many tones. The fundamentals (component anatomy, states, a11y,
guardrails) never change; the look (color, type, radius, density) is a tone you
can switch, fork, or override per project.

```
library/core.md  +  library/tones/<tone>.md  +  .ds4a/project.md   →   DESIGN.md
 fundamentals         look (tokens + personality)   this project's deltas   what the agent reads
```

Later layers win on tokens. The library lives in this skill's repo, so every
project reuses the same copy and merges can grow it.

## Commands

Invoke as `/ds4a <subcommand> [args]`. The first word picks the section below.
`/ds4a` alone prints this table. Plain-text forms ("ds4a init") work too. Nothing
runs automatically.

| Command | What it does |
|---|---|
| `/ds4a init [type]` | Detect existing design system → write overlay → resolve → `DESIGN.md` → open preview |
| `/ds4a detect` | Dry run. Report what was found; write nothing |
| `/ds4a tone` | Show the active tone; list tones |
| `/ds4a tone <name>` | Switch the project's tone and re-resolve (overlay kept) |
| `/ds4a tone new <name>` | Fork the current resolved look into `library/tones/<name>.md` |
| `/ds4a resolve` | Regenerate `DESIGN.md` from core + tone + overlay |
| `/ds4a preview` | Build and open `.ds4a/preview.html` for the active tone |
| `/ds4a review` | Three-pass review of generated code; approve/reject each suggestion |
| `/ds4a merge` | Merge approved rules to their target (project, tone, or core) |
| `/ds4a status` | Initialized? active tone, type, library versions, pending review |

`<skill>` below means this skill's directory (the one containing this file).

## Files

```
<skill>/                         (git repo; the reusable library)
├── library/core.md              tone-free contracts + guardrails ({{placeholders}})
├── library/tones/neutral.md     default when no design system is found
├── library/tones/warm-sharp.md  the original ds4a look
├── library/usage.md             which projects used which grown contracts
├── scripts/resolve.py           merge layers → DESIGN.md (+ contrast/parity checks)
├── scripts/build-preview.py     tokens → .ds4a/preview.html
├── scripts/oklch-to-hex.py      shadcn oklch → hex
└── references/                  detection, matrix, review prompt, pitfalls ...

<project>/
├── DESIGN.md                    generated; do not hand-edit
└── .ds4a/
    ├── project.md               overlay: tone, type, token overrides, project notes
    ├── preview.html
    └── pending.md               approved review suggestions awaiting merge
```

The project root is never touched except `DESIGN.md`. Existing files (AGENTS.md,
tokens, globals.css, tailwind config, a hand-written DESIGN.md) are read, never
overwritten. State is re-derived from files each session.

## /ds4a init [type]

1. **Initialized?** `.ds4a/project.md` exists → skip to step 5.
2. **Detect.** Follow `references/detection.md`: find sources, extract tokens,
   normalize. Read-only.
3. **Pick the tone.**
   - Nothing found → `tone: neutral` (structure from core, neutral tokens).
   - Design system found → `tone: neutral` too; found tokens go in the overlay and
     override it. Gaps fall back to neutral, not to a tone with its own taste.
   - The user may name a tone (`/ds4a init dashboard --tone warm-sharp`).
4. **Write `.ds4a/project.md`** from `templates/project-overlay.md`: `tone:`,
   `type:` (ask if missing: dashboard, landing-page, auth-flow, settings,
   data-table, content-site, e-commerce, admin-panel — keywords in
   `references/component-matrix.md`), then only the keys that were found.
5. **Resolve:** `python3 <skill>/scripts/resolve.py --project .`
   Surface its warnings (contrast, matrix parity). A hand-written `DESIGN.md`
   is not overwritten; ask where to write (`--out`).
6. **Log:** append a row to `library/usage.md` (date, project, tone, type, grown
   contracts included).
7. **Preview:** `python3 <skill>/scripts/build-preview.py --project .`, then open
   `.ds4a/preview.html` (`open` on macOS, `xdg-open` on Linux).
8. **Report:**
   ```
   ✓ Source: <sources found | none → neutral baseline>
   ✓ Tone: <name> · type: <type> · <N> overrides in .ds4a/project.md
   ✓ DESIGN.md: <lines> lines (<X>% of full library)
   ✓ Contrast: <pass | warnings>
   → Opened .ds4a/preview.html
   ```

## /ds4a detect

Run step 2 only and print the report format from `references/detection.md`. Write
nothing, not even the overlay.

## /ds4a tone [name | new <name>]

- **No args:** `python3 <skill>/scripts/resolve.py --list-tones` plus the
  project's active tone (`tone:` in the overlay).
- **`<name>`:** set `tone: <name>` in `.ds4a/project.md`, then resolve. Overlay
  token overrides stay and still win — tell the user, and offer to remove them
  to see the tone unmodified.
- **`new <name>`:** copy the active tone file to `library/tones/<name>.md`, apply
  the project's overlay token overrides into its frontmatter, set `name:` and
  `version: 1`, rewrite its Overview, delete tone-specific rules that no longer
  apply. Then point the project at it. The new tone must resolve:
  `resolve.py --tone <name> --check`.

## /ds4a resolve · /ds4a preview · /ds4a status

- **resolve:** run `resolve.py --project .` (add `--check` for a report only).
- **preview:** run `build-preview.py`, open the file. See `references/preview.md`.
- **status:** report whether `.ds4a/project.md` and `DESIGN.md` exist, the tone and
  type, `resolve.py --check` output, versions of core and the active tone, and
  whether `.ds4a/pending.md` has approved suggestions.

## Build (no skill action)

The agent reads `DESIGN.md` and builds. A component the contracts don't cover is
built from the tokens and guardrails; `review` will catch it and propose a
contract.

## /ds4a review

Explicit only. Three passes over generated code, as defined in
`references/review-prompt.md`.

1. **Inputs:** source files (`src/**`, `app/**`, `pages/**`, `components/**`) and
   `DESIGN.md`. For taste lock, also read the active tone's Overview.
2. **Pass 1 — violations** against rules in DESIGN.md (cite rule + `file:line`).
   **Pass 2 — patterns** repeated 3+ times but not codified. **Pass 3 — gaps**
   where the agent guessed.
3. **Quality filter** — every suggestion must be specific, applicable,
   preventive, taste-matched, evidence-backed. Otherwise drop it silently.
4. **Target** each suggestion: `project` (default), `tone:<name>`, or `core`
   (only if it contains no tone values). Table in the review prompt.
5. **Promotion:** a `(grown)` contract in `library/usage.md` for 3+ projects →
   "Promote [X] to core? [y/n]".
6. **Approval:** present one by one (`Suggestion 1/5: card-padding-default
   (token, high, → tone:warm-sharp) Approve? [y/n]`). Write approved ones to
   `.ds4a/pending.md`.

## /ds4a merge

Explicit only. Reads `.ds4a/pending.md` (none → "Run `/ds4a review` first").

| Target | File | Type → place |
|---|---|---|
| `project` | `.ds4a/project.md` | token → frontmatter; prose/guardrail/contract → matching `##` section |
| `tone:<name>` | `library/tones/<name>.md` | token → frontmatter; prose → that tone's section |
| `core` | `library/core.md` | contract → `## Components` as `### Name (grown)`; guardrail → `## Do's and Don'ts`; no raw tone values |

Rules:
- Insert in place; add-only. Skip a rule that conflicts with an existing one and
  say why.
- Bump `version` in the file that changed.
- A new **core** contract uses `{{components.<name>.*}}` placeholders, so add
  those keys to **every** tone, then run `resolve.py --tone <t> --check` for each
  tone. Promotion removes `(grown)` and updates `references/core-components.md`.
- After merging: re-run resolve for the project; offer to delete `pending.md`.
- Report: `Merged N → project, M → tone:<x>, K → core; S skipped.`

## Rules

- Explicit commands only. No auto-review, no auto-merge.
- Core stays tone-free; tone files own every look decision.
- Never overwrite files the user owns; only `DESIGN.md` and `.ds4a/` are written.
- Evidence or silence: no `file:line`, no suggestion.
- More in `references/pitfalls.md`.

## References

- `references/detection.md` — find sources, extract, normalize, derive guardrails
- `references/shadcn-baseline.md` — shadcn theme variable map, radius scale, dark mode
- `references/project-generator-prompt.md` — what `resolve.py` does; project types
- `references/component-matrix.md` — component and layout relevance per project type
- `references/core-components.md` — benchmark behind the 13 core contracts; tiers
- `references/review-prompt.md` — three-pass review, output format, targets
- `references/preview.md` — preview build; legacy showcase and in-framework templates
- `references/pitfalls.md`
- `templates/project-overlay.md` — starting overlay

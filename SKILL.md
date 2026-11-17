---
name: ds4a
description: >-
  Design System for Agents — a reusable design library with swappable tones.
  Detects a project's existing design system (or starts from a neutral Base
  UI-style baseline), resolves core + tone + project overlay into DESIGN.md,
  captures the project's real components as specimens in the preview, writes
  tokens into one generated CSS file, reviews generated code, and merges
  approved rules back. Use for `/ds4a init`, `/ds4a tone`, `/ds4a blend`,
  `/ds4a specimens`, `/ds4a apply`, `/ds4a diff`, `/ds4a merge`, or when the
  user wants a design system for their AI agent.
version: 2.2.0
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
| `/ds4a blend [--adopt]` | Migrate a hand-written `DESIGN.md` into the overlay; verify tokens against code; adopt in place |
| `/ds4a spec <…>` / `/ds4a specimens <…>` | `scan` candidates, `add` a captured component, `remove`, `list` |
| `/ds4a apply [--check]` | Write resolved tokens to `src/styles/ds4a-tokens.css` (or one Tailwind `@theme` block); `--check` reports drift |
| `/ds4a preview` | Build and open `.ds4a/preview.html` for the active tone |
| `/ds4a diff` | Diff generated code against DESIGN.md (violations, patterns, gaps, specimens); approve/reject each suggestion |
| `/ds4a merge` | Merge approved rules to their target (project, tone, core, or preview) |
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
├── scripts/blend.py             hand-written DESIGN.md → overlay, verified against code
├── scripts/specimens.py         scan/add/remove project component specimens
├── scripts/apply.py             resolved tokens → one generated CSS/`@theme` file
├── scripts/oklch-to-hex.py      shadcn oklch → hex
└── references/                  detection, matrix, review prompt, pitfalls ...

<project>/
├── DESIGN.md                    generated; do not hand-edit
└── .ds4a/
    ├── project.md               overlay: tone, type, token overrides, project notes
    ├── preview.html
    ├── specimens/               *.html copies of this project's components
    └── pending.md               approved review suggestions awaiting merge
```

The project root is never touched except `DESIGN.md`. Existing files (AGENTS.md,
tokens, globals.css, tailwind config, a hand-written DESIGN.md) are read, never
overwritten. State is re-derived from files each session.

## /ds4a init [type]

1. **Initialized?** `.ds4a/project.md` exists → skip to step 5.
2. **Detect.** Follow `references/detection.md`: find sources, extract tokens,
   normalize. Read-only. If a hand-written `DESIGN.md` exists, also run the
   drift check in detection.md §8 and report conflicts — never silently pick a
   winner without saying so.
2a. **Existing `DESIGN.md`? Stop and ask before writing anything.** Offer:
    (a) **keep both** — overlay + generated doc beside `DESIGN.md` (previous
    behavior); (b) **adopt** — the generated doc becomes the visual source of
    truth going forward, with conflicts from the drift check resolved in the
    overlay and `DESIGN.md` left as a historical reference (or deleted, user's
    call); (c) **abort**. Never report "init complete" while presenting a
    parallel doc as if it were the system.
    - For adopt, run `/ds4a blend --adopt`: `blend.py` extracts the doc's
      tokens and unique rules into the overlay, compares them with the values
      in code, reports every conflict with both values and sources, backs up
      the old doc, and regenerates `DESIGN.md` in place. `resolve.py --adopt`
      is the direct flag when the overlay is already correct.
    - Where the project contradicts the library (no tabs, no shadows), encode
      that in the overlay instead of leaving it as prose the reader must
      reconcile: `exclude_components: [Tabs]` in the frontmatter drops the
      contract entirely; a section starting with `<!-- replace -->` owns that
      section outright instead of appending to the core text.
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

## /ds4a blend [--adopt]

Explicit only. Migrate a hand-written `DESIGN.md` into the overlay:

1. Read the doc (frontmatter + token tables) and the project's token files
   (CSS custom properties, DTCG JSON, typed token files).
2. Compare values. Report every conflict with both values and their source;
   `--prefer code` (default) keeps the code value, `--prefer doc` keeps the doc.
3. Keep only prose rules that are not already in core+tone. They go into the
   overlay as `### Project notes`.
4. Write the overlay with `--write-overlay`; with an existing hand-written doc,
   resolve to `DESIGN.generated.md` (keep both) instead of overwriting.
5. `--adopt` backs up the old doc to `.ds4a/DESIGN.md.pre-ds4a.md`, regenerates
   `DESIGN.md` from the overlay, and removes a stale `DESIGN.generated.md`.
   Run it only after the user confirms adoption.

## /ds4a specimens [scan | add <name> | remove <name> | list]

The preview renders `.ds4a/specimens/<slug>.html` under **Project specimens**,
above the core contracts. A specimen is a static copy, never a dev-server
iframe, and uses the same CSS custom properties as the page, so tone switching
re-skins it.

- **scan:** find component files under `src/components` (and astro/react/svelte
  equivalents) with no specimen and no matching core contract. Read-only; this
  is also the fourth finding class in `diff`.
- **add `<name>` `--from <file>`:** extract the markup (best effort; React/Vue/
  Svelte/HTML), write a provenance header (`source`, `captured`, optional
  `contract:`), register it in the overlay, rebuild the preview. Use `--html`
  to pass a hand-made snippet, `--contract <Name>` when it is the project's
  version of a core contract.
- **remove `<name>`:** delete the file, unregister it, rebuild.
- **list:** metadata and a warning when the source changed since capture.

## /ds4a apply [--check]

Write the resolved system into exactly one new file the tool owns:

- `src/styles/ds4a-tokens.css` by default; `--tailwind` writes one `@theme`
  block to `src/styles/ds4a-theme.css`.
- Never edits components, stylesheets, or `tailwind.config`; prints the one
  `@import` line for the human to add.
- `--check` compares the file with the overlay and lists hardcoded hex/px in
  source that exactly match a token (migration candidates). Writes nothing;
  `--strict` exits 1 on drift.
- Refuses to overwrite a file that lacks the `Generated by ds4a apply` marker
  unless `--force` is passed after confirmation.

## /ds4a resolve · /ds4a preview · /ds4a status

- **resolve:** run `resolve.py --project .` (add `--check` for a report only).
- **preview:** run `build-preview.py`, open the file. See `references/preview.md`.
- **status:** report whether `.ds4a/project.md` and `DESIGN.md` exist, the tone and
  type, `resolve.py --check` output, versions of core and the active tone, and
  whether `.ds4a/pending.md` has approved suggestions.

## Build (no skill action)

The agent reads `DESIGN.md` and builds. A component the contracts don't cover is
built from the tokens and guardrails; `diff` will catch it and propose a
contract.

## /ds4a diff

Explicit only. Four passes over generated code, as defined in
`references/review-prompt.md`.

1. **Inputs:** source files (`src/**`, `app/**`, `pages/**`, `components/**`) and
   `DESIGN.md`. For taste lock, also read the active tone's Overview.
2. **Pass 1 — violations** against rules in DESIGN.md (cite rule + `file:line`).
   **Pass 2 — patterns** repeated 3+ times but not codified. **Pass 3 — gaps**
   where the agent guessed. **Pass 4 — specimens/coverage** — components and
   tokens the code uses that DESIGN.md doesn't define, plus component files with
   no specimen and no contract (`specimens.py scan`). No repeat threshold; one
   use is enough.
3. **Quality filter** — every suggestion must be specific, applicable,
   preventive, taste-matched, evidence-backed. Otherwise drop it silently.
4. **Target** each suggestion: `project` (default), `tone:<name>`, `core`
   (only if it contains no tone values), or `preview` (a specimen). Table in the
   review prompt.
5. **One-command fix:** a specimen finding carries
   `python3 <skill>/scripts/specimens.py --project . add <slug> --from <file>`
   (add `--contract <Name>` when it is the project's version of a core
   contract). Approving it writes the specimen, registers it in the overlay, and
   rebuilds the preview — the component appears on the page with no ceremony.
6. **Promotion:** a `(grown)` contract in `library/usage.md` for 3+ projects →
   "Promote [X] to core? [y/n]".
7. **Approval:** present one by one (`Suggestion 1/5: card-padding-default
   (token, high, → tone:warm-sharp) Approve? [y/n]`). Write approved ones to
   `.ds4a/pending.md`.

## /ds4a merge

Explicit only. Reads `.ds4a/pending.md` (none → "Run `/ds4a diff` first").

| Target | File | Type → place |
|---|---|---|
| `project` | `.ds4a/project.md` | token → frontmatter; prose/guardrail/contract → matching `##` section |
| `tone:<name>` | `library/tones/<name>.md` | token → frontmatter; prose → that tone's section |
| `core` | `library/core.md` | contract → `## Components` as `### Name (grown)`; guardrail → `## Do's and Don'ts`; no raw tone values |
| `preview` | `.ds4a/specimens/<name>.html` | specimen → file with provenance header; register `<name>` in `specimens:`; rebuild |

Rules:
- Insert in place; add-only. Skip a rule that conflicts with an existing one and
  say why.
- A merged **preview** rule ships its specimen: "approved into the design
  system" means it renders on the page. Use `specimens.py add` for the file and
  registration, then merge the prose rule to its real layer.
- Bump `version` in the file that changed.
- A new **core** contract uses `{{components.<name>.*}}` placeholders, so add
  those keys to **every** tone, then run `resolve.py --tone <t> --check` for each
  tone. Promotion removes `(grown)` and updates `references/core-components.md`.
- After merging: re-run resolve for the project; offer to delete `pending.md`.
- Report: `Merged N → project, M → tone:<x>, K → core, P → preview; S skipped.`

## Rules

- Explicit commands only. No auto-review, no auto-merge.
- Core stays tone-free; tone files own every look decision.
- Never overwrite files the user owns; only `DESIGN.md`, `.ds4a/`, and the one
  `ds4a apply` token file are written.
- Never silently resolve a doc-vs-code conflict: print both values and sources,
  then let the user choose (`blend --prefer code|doc`).
- Specimens are copies, not generated components; never rewrite component source.
- Evidence or silence: no `file:line`, no suggestion.
- More in `references/pitfalls.md`.

## References

- `references/detection.md` — find sources, extract, normalize, derive guardrails
- `references/blend.md` — migrate a hand-written DESIGN.md, adopt in place
- `references/specimens.md` — capture real components, provenance, candidates
- `references/apply.md` — generate the token file, drift and hardcoded-value checks
- `references/shadcn-baseline.md` — shadcn theme variable map, radius scale, dark mode
- `references/project-generator-prompt.md` — what `resolve.py` does; project types
- `references/component-matrix.md` — component and layout relevance per project type
- `references/core-components.md` — benchmark behind the 13 core contracts; tiers
- `references/review-prompt.md` — four-pass review, output format, targets
- `references/preview.md` — preview page sections and features; in-framework templates
- `references/pitfalls.md`
- `templates/project-overlay.md` — starting overlay

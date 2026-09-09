# ds4a Preview — component showcase site (sidebar scheme, self-dogfooding)

## Status
DRAFT

## Goal
One browser-openable page that live-previews all 13 core ds4a components — navigated by a sidebar that IS the ds4a Sidebar contract. The design system documents itself by being built with itself.

## Context
- Repo at `2ea7a49` (v1.2.0), 3 copies 1:1. 13 core contracts in `references/master-library.md` (YAML frontmatter + prose).
- Repo today: pure markdown skill. Zero JS, no package.json, no build infra.
- Related plans: `2026-09-03_223000-core-component-default.md` (COMPLETED — shipped the 13 contracts this showcase displays).
- User wants visual verification — this deliverable is exactly that: contracts viewable in browser, not just prose.
- No NODE_ENV/dev-server risk: proposed approach is static HTML, no server required.

## Decision to confirm (A) — tech approach

| | Option 1: single static HTML | Option 2: Vite + React site |
|---|---|---|
| New infra in repo | none — one file + maybe one folder | package.json, node_modules, build config |
| Open | `open preview/index.html` — works offline, file:// | needs dev server or build |
| Matches repo ethos (portable, agent-agnostic) | ✅ | ❌ pulls JS toolchain into a markdown skill repo |
| Interactivity (modal, tabs, select) | vanilla JS, ~200 lines | React components |
| Maintenance | hand-edited, parity-checked | more moving parts |
| Cost | zero | zero, but heavier |

**Recommend Option 1.** Repo's whole pitch is "portable taste layer, any agent, no toolchain." A static showcase proves the contracts are framework-agnostic — the same argument the FAQ makes. Vanilla JS for the 4 interactive demos (modal, tabs, select, form validation) is small and readable.

## Requirements
- Must have (P0)
  - `preview/index.html` — self-contained (inline CSS/JS, no external requests except optional Google Fonts with system fallbacks).
  - Sidebar nav = live Sidebar contract: 240px fixed, border-right, section headers, active = muted bg + 2px primary left-edge indicator. Dogfooding proof #1.
  - All 13 components live-previewed: Button (3 variants × 3 sizes × states), Input (3 sizes, default/error/disabled), Card (3 variants), Badge (3 variants), Field/Fieldset/Form (validation demo), Select (working dropdown + keyboard), RadioGroup (Radio + RadioCard checkable), Modal (open/close, backdrop, focus return), Tabs (switch + sliding indicator), Table (hover, selected, empty, loading states), Sidebar (the nav itself + spec page).
  - Foundations pages: Colors (token swatches + rules), Typography (Fauna One + Inter scale rendered), Spacing (4px scale visual), Radius (why 0px), Elevation (subtle vs elevated), Motion (durations).
  - Every spec value shown comes FROM the YAML frontmatter values — no invented numbers.
  - Showcase obeys its own pre-flight checklist: one H1 per view, one primary action per view, 4px grid, semantic tokens in CSS vars (`--color-*`), AA contrast, 0px radius everywhere.
- Should have (P1)
  - `ds4a preview` command in SKILL.md: opens `preview/index.html` in the default browser. README gets a Preview section.
  - Spec table under each preview: variants, sizes, tokens (read from the contract).
  - Parity validation: nav items == 13 contract names == component-matrix list.
- Nice to have (P2)
  - GitHub Pages deploy for a live README link (free hosting).
  - `scripts/build-preview.py` that regenerates spec tables from YAML (hand-authored previews stay; tables auto-sync). Skip for now — hand-authored + parity check is enough at 13 components.

## Architecture / Design

```
preview/index.html (single file, ~1800-2200 lines)
├── <style>  tokens as CSS vars  ← 1:1 from master-library.md frontmatter
│            (--color-*, --title-h*, --label-*, --paragraph-*,
│             --radius-*, --space-*, --shadow-*, --duration-*)
├── <style>  component styles per contract (Button, Input, Card, ... Sidebar)
├── <body>
│   ├── sidebar (Sidebar contract: 240px, sections, active indicator)
│   └── main (view swapped by nav click; scroll position resets)
├── <script>  nav switching + focus states
└── <script>  interactive demos: modal, tabs, select, form validation, table states
```

Views (hash-based routing, `#button`, `#colors` — back-button works):

```
┌──────────┬───────────────────────────────────────────┐
│ ds4a     │  Button                    ← H1 (Fauna One)│
│ Preview  │  3 variants · 3 sizes · states             │
│          │                                           │
│ OVERVIEW │  ┌───────────────────────────────────────┐ │
│ FOUNDAT. │  │ [Primary] [Secondary] [Ghost]         │ │
│  Colors  │  │ hover:  ·  disabled: [Primary] ·      │ │
│  Type    │  │ sm/md/lg rows ...                     │ │
│  Spacing │  └───────────────────────────────────────┘ │
│  Radius  │  Specs                                    │
│  Elevat. │  ┌───────────────────────────────────────┐ │
│  Motion  │  │ radius: 0px · padding-md: 10px 16px  │ │
│ ──────── │  │ gap: 8px · variants: primary/...      │ │
│ COMPO-   │  └───────────────────────────────────────┘ │
│ NENTS    │  Rules (3-4 key ones from the contract)   │
│  Button  │                                           │
│  Input ● │  ● = active: muted bg + 2px primary edge  │
│  Card    │                                           │
│  ...13   │                                           │
└──────────┴───────────────────────────────────────────┘
Mobile (<768px): sidebar → hamburger overlay (Modal rules), per Sidebar contract.
```

Component view template (every component gets the same shape):

```
H1 name → one-line role → live preview block(s) → spec table → key rules
```

## Implementation Steps

### Step 1: Shell + tokens + foundations
- What: `preview/index.html` skeleton — CSS vars from frontmatter, sidebar nav (all sections), Overview + 6 foundation views, hash routing.
- Files: `preview/index.html` (new)
- Validation: open in browser; sidebar active states cycle; colors/typography/spacing render with exact frontmatter values.

### Step 2: Component views — static ones (7)
- What: Button, Input, Card, Badge, Field, Fieldset+Form (static), RadioGroup — all variants/sizes/states rendered + spec tables.
- Files: `preview/index.html`
- Validation: visual pass vs contract values; one primary per view; disabled = opacity 0.5.

### Step 3: Component views — interactive ones (5)
- What: Select (dropdown + keyboard), Modal (open/close/backdrop/focus), Tabs (sliding indicator), Table (hover/selected/empty/loading), Sidebar spec view (the nav itself is the live demo).
- Files: `preview/index.html` (+ JS ~200 lines)
- Validation: each interaction works; modal returns focus; tabs animate transform only; table empty state renders "No results".

### Step 4: Skill + README wiring
- What: SKILL.md — `ds4a preview` command (opens the file); References row; README — Preview section + What's-inside row.
- Files: `SKILL.md`, `README.md`
- Validation: parity check — 13 nav items == 13 contracts == matrix; grep checks.

### Step 5: Visual verification + ship
- What: User opens `preview/index.html`, clicks through all views (per your visual-verification preference). Fixes folded in. Commit `feat: ds4a preview — self-dogfooding showcase (v1.2.1)`, push, re-sync installed-skill clone.
- Validation: browser click-through clean; 3-way 1:1 check; parity script passes.

## Tests / Validation
- Parity: script compares nav data array vs `### ` contract headings vs matrix rows — 13 everywhere.
- Token fidelity: CSS var values diffed against frontmatter programmatically (Step 1).
- Self-compliance: pre-flight checklist run on the showcase itself (one H1/view, one primary/view, 0px radius, AA).
- Human: your click-through (Step 5).

## Risks & Open Questions
- **Decision A (above):** static single-file vs Vite+React. Recommend static. Confirm?
- **Decision B:** fonts — Google Fonts link (needs internet) vs system serif fallback only. Recommend: link Google Fonts (Fauna One + Inter), graceful fallback to Georgia/system-sans when offline. Fine?
- **Decision C:** `ds4a preview` command — adds a 4th command to the skill's contract. Recommend yes. Confirm?
- Hand-authored previews can drift from contracts later. Mitigation: Step 4 parity check + P2 generator later. Acceptable?
- Single file will be ~2000 lines — heavy but intentional (zero-dep). If it becomes a maintenance pain, split to `preview/{index.html, styles.css, app.js}` — same folder, still no build. Acceptable?
- GitHub Pages (P2) needs a repo Settings toggle — only if you want the public live link.

## Changelog
- 2026-09-03: Initial draft. Dogfooding showcase, single static HTML, 13 core components + foundations.
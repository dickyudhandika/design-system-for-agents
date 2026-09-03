# ds4a Core Component Default — benchmark-backed basic tier

## Status
COMPLETED

## Goal
Define what "basic components" means via real design-system benchmarks, make that the installed default library, so the review→merge loop grows every library from the same benchmarked floor.

## Context
- Repo at `cc3b9f7` (v1.1.0), all 3 copies 1:1.
- **Gap found:** `component-matrix.md` references 13 components; `master-library.md` has only 9 contracts. Table, Sidebar, Modal, Tabs are ✅ in the matrix (dashboard, admin-panel) but have NO contract — `ds4a init dashboard` promises contracts it cannot include.
- `shadcn-baseline.md` component mapping also references Modal, Tabs, Table, Sidebar, Tooltip, Popover — 5 of which don't exist as contracts.
- Growth loop (Phase 5 merge) adds contracts but has no tier concept — a merged contract and a baseline contract are indistinguishable.
- Related plan: `2026-09-03_214800-readme-v1.1.0-catchup.md` (DRAFT, pending). Its README edits fold into this plan's Step 5 — one README pass, one commit series.
- Existing plan at `.hermes/plans/2026-09-03_214800-readme-v1.1.0-catchup.md` — link noted.

## Benchmark: what is "basic"

Sources verified live (2026-09-03):
1. **UXPin "10 Essential Design System Components"** (uxpin.com/studio/blog/design-system-components/): Button, Text Input, Checkbox/Radio, Toggle, Select, Card, Modal, Navigation (Tabs/Sidebar), Alerts, Data Table.
2. **shadcn/ui registry** (`ui.shadcn.com/r/index.json`): 63 components.
3. **Base UI v1.6.0 exports** (local reference `design-system-library/references/base-ui-v1.md`): 38 components.
4. **Adele/UXPin repo**: 103 systems, no per-system component inventories (only yes/no flags) — rejected as benchmark source.
5. **ds4a current state**: 9 contracts, 13 matrix components.

### Consensus matrix

| Component | UXPin 10 | shadcn | Base UI | ds4a contract | ds4a matrix | Core? |
|---|---|---|---|---|---|---|
| Button | ✅ | ✅ | ✅ | ✅ | ✅ | **core** |
| Input | ✅ | ✅ | ✅ | ✅ | ✅ | **core** |
| Field (+Form/Fieldset) | ✅ | ✅ | ✅ | ✅ | ✅ | **core** |
| Select | ✅ | ✅ | ✅ | ✅ | ✅ | **core** |
| RadioGroup | ✅ (radio) | ✅ | ✅ | ✅ | ✅ | **core** |
| Card | ✅ | ✅ | ❌ | ✅ | ✅ | **core** |
| Badge | atom | ✅ | ❌ | ✅ | ✅ | **core** |
| Modal/Dialog | ✅ | ✅ | ✅ | ❌ | ✅ | **core** — contract missing, write it |
| Tabs | ✅ (nav) | ✅ | ✅ | ❌ | ✅ | **core** — contract missing, write it |
| Table | ✅ | ✅ | ❌ | ❌ | ✅ | **core** — contract missing, write it |
| Sidebar | ✅ (nav) | ✅ | ❌ | ❌ | ✅ | **core** — contract missing, write it |
| Checkbox | ✅ | ✅ | ✅ | ❌ | ❌ | **OPTION B** |
| Switch/Toggle | ✅ | ✅ | ✅ | ❌ | ❌ | **OPTION B** |
| Alert/Toast | ✅ | ✅ | ✅ (toast) | ❌ | ❌ | **OPTION B** |
| Tooltip/Popover | — | ✅ | ✅ | ❌ | ❌ | **OPTION B** |

**Core rule:** core = appears in ds4a matrix AND ≥2 of 3 external benchmarks. All 13 matrix components qualify. Option B components qualify on benchmarks but have no matrix row — adding them means matrix rows + shadcn-mapping rows too.

**Default proposal: Core = the 13 matrix components.** Option B (→16-17) is a separate decision below.

## Requirements
- Must have (P0)
  - 4 missing contracts written: Table, Sidebar, Modal, Tabs (YAML frontmatter entries + prose contracts in ds4a aesthetic — sharp, warm white, 4px grid).
  - Matrix-parity guarantee: every matrix component resolves to a contract. Validation greps this.
  - `references/core-components.md` — benchmark table, core list, tier rules.
  - Tier mechanics in SKILL.md: merged contracts marked `(grown)`; promotion rule; core never demotes.
  - README updates (folds in the v1.1.0 catch-up P0s: shadcn FAQ, What's-inside rows, 401→425 line count, "non-Hermus" typo, validation-link fix).
- Should have (P1)
  - Core-tier line in Scenario A report: "Installed baseline: 13 core contracts."
  - Version: master-library frontmatter `version: alpha` → `version: 1` (merge loop already increments integers).
- Nice to have (P2)
  - Option B components (Checkbox, Switch, Alert, Tooltip) — see open question.

## Architecture / Design

```
master-library.md                     ← +4 contracts (Table, Sidebar, Modal, Tabs)
  └─ ## Components
       ├─ 13 core contracts (9 existing + 4 new)
       └─ grown contracts appended by merge, header marked "(grown)"
references/core-components.md          ← NEW: benchmark + tier rules + promotion rule
references/component-matrix.md         ← unchanged (already correct)
references/shadcn-baseline.md          ← unchanged (13 mapping rows now all resolve)
SKILL.md                               ← tier mechanics + core report + references row
README.md                              ← v1.1.0 catch-up + core tier section
```

**Tier rules (the "grow from default" mechanics):**
1. **Core** = the 13 benchmarked contracts above. Shipped with baseline. Always in `.ds4a/library.md` after init.
2. **Grown** = any contract added via `ds4a merge`. Header gets `(grown)` marker. Version bumps per existing merge rules.
3. **Promotion**: when a grown contract has been included in 3+ separate project DESIGN.md generations, review output suggests: "Promote [X] to core?" — user yes/no. Promotion = remove `(grown)` marker + add to core-components.md list.
4. **No demotion** — merge loop is add-only (existing Phase 5 rule).
5. Per-type extraction unchanged: matrix governs which core contracts land in a project DESIGN.md.

## Implementation Steps

### Step 1: Write 4 missing contracts in master-library.md
- What: `### Table`, `### Sidebar`, `### Modal`, `### Tabs` prose contracts (~25-30 lines each, ds4a style: variant/size tables, token refs, a11y notes) + matching YAML `components:` entries (table, sidebar, modal, tabs).
- Files: `references/master-library.md`
- Validation: matrix components list == contract `###` list (grep parity, 13 == 13); YAML frontmatter parses; line count ~591 → ~730.

### Step 2: Create references/core-components.md
- What: benchmark table (copied from this plan, sources cited), core tier list, tier rules 1-5 above, promotion rule.
- Files: `references/core-components.md` (NEW, ~80 lines)
- Validation: 13 components listed; every one links to its `master-library.md` contract heading.

### Step 3: SKILL.md tier mechanics
- What: Phase 5 merge — grown marker rule; Phase 4 review — promotion suggestion rule; Phase 1 Scenario A report line "13 core contracts"; References section row for core-components.md.
- Files: `SKILL.md` (~+20 lines)
- Validation: grep `(grown)` + `core-components.md` present; scenario report template updated.

### Step 4: README — one pass, folds v1.1.0 catch-up
- What: What's-inside table (+shadcn-baseline.md, +oklch-to-hex.py, +core-components.md rows, 401→current SKILL.md count), core tier section (1 para + 13 list), shadcn FAQ entry, validation-link fix (soften claim — no validation report exists), "non-Hermus"→"non-Hermes".
- Files: `README.md`
- Validation: grep shadcn ≥2 hits; grep 401 → 0; grep Hermus → 0.

### Step 5: Commit, push, re-sync both clones
- What: `feat: core component default — 4 missing contracts, benchmark-backed tier system (v1.2.0)`; push GitHub; `git pull --ff-only` in installed-skill clone. Master-library frontmatter version: 1.
- Validation: 3-way 1:1 check (ls-remote + diff), matrix↔library parity grep re-run.

## Tests / Validation
- Parity: matrix components (13) == master library contracts (13) — grep, not eyeball.
- YAML frontmatter parses (python yaml.safe_load on frontmatter block).
- init simulation on a scratch dir: copy master-library.md → confirm all dashboard matrix components resolve.
- User skim: benchmark table + core list + Option B decision (5 min).

## Risks & Open Questions
- **Option B (needs your call):** add Checkbox, Switch/Toggle, Alert/Toast, Tooltip/Popover to core (→16-17 components)? Benchmarks all support them (3/3 sources), but each needs a contract + matrix row + shadcn-mapping row (~4× work of one contract). Default if you don't care: **ship 13 now, Option B lands via the merge loop naturally** — the tier system means grown components can promote later. That's the whole point of "grow from default."
- Modal contract vs Card elevation overlap: Modal uses `shadow.elevated` + overlay backdrop — must state "no border on modal, shadow only" to not contradict the border/shadow rule. Handled in Step 1.
- Table density choice: no row for compact/dense variants in v1 — one density only (12px row padding, `md`). Extensions via merge.
- Existing installed libraries (`hermesfordesigners` project etc.) unaffected — their `.ds4a/library.md` is a copy made at their init; baseline changes only affect new inits.
- README line counts will drift again; acceptable (P2 noted in catch-up plan).

## Changelog
- 2026-09-03: Initial draft. Benchmark run live (UXPin, shadcn registry, Base UI). Folds in pending README v1.1.0 catch-up plan.
- 2026-09-03: LINK — superseded-by relationship: this plan's Step 4 absorbs all edits from `2026-09-03_214800-readme-v1.1.0-catchup.md`; execute this plan instead.
- 2026-09-03: EXECUTED. Option B rejected by user (ship 13). Commit `ad1601a` pushed; Documents clone + installed skill byte-identical; matrix↔library parity 13==13 validated; YAML parses; frontmatter version 1; SKILL.md v1.2.0. All steps 1-5 done.
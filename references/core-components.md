# Core Component Default

What "basic components" means in ds4a — benchmarked, not guessed. Every library
installed by `ds4a init` starts from this floor, then grows via the merge loop.

## Benchmark

Live-verified 2026-09-03. A component is **core** if it appears in the ds4a
project-type matrix AND in ≥2 of the 3 external benchmarks.

Sources:
- **UXPin** — "10 Essential Design System Components" (uxpin.com/studio/blog/design-system-components/): Button, Text Input, Checkbox/Radio, Toggle, Select, Card, Modal, Navigation, Alerts, Data Table.
- **shadcn/ui registry** (ui.shadcn.com/r/index.json): 63 components.
- **Base UI v1.6.0** exports (base-ui-components/react): 38 components.
- Rejected: Adele/UXPin repository (103 systems) — tracks yes/no flags, no component inventories.

| Component | UXPin | shadcn | Base UI | Matrix | Core |
|---|---|---|---|---|---|
| Button | ✅ | ✅ | ✅ | ✅ | **core** |
| Input | ✅ | ✅ | ✅ | ✅ | **core** |
| Field / Form / Fieldset | ✅ | ✅ | ✅ | ✅ | **core** |
| Select | ✅ | ✅ | ✅ | ✅ | **core** |
| RadioGroup | ✅ | ✅ | ✅ | ✅ | **core** |
| Card | ✅ | ✅ | — | ✅ | **core** |
| Badge | ✅ | ✅ | — | ✅ | **core** |
| Modal | ✅ | ✅ | ✅ | ✅ | **core** |
| Tabs | ✅ | ✅ | ✅ | ✅ | **core** |
| Table | ✅ | ✅ | — | ✅ | **core** |
| Sidebar | ✅ | ✅ | — | ✅ | **core** |
| Checkbox | ✅ | ✅ | ✅ | — | grown-candidate |
| Switch / Toggle | ✅ | ✅ | ✅ | — | grown-candidate |
| Alert / Toast | ✅ | ✅ | ✅ | — | grown-candidate |
| Tooltip / Popover | — | ✅ | ✅ | — | grown-candidate |

12 named contracts (Field/Form/Fieldset counted as one family) = 13 matrix
components. All 13 have contracts in `master-library.md` — matrix parity is a
validated invariant, not an assumption.

## Tiers

1. **Core** — the 13 contracts above. Shipped in the baseline. Every
   `.ds4a/library.md` installed by Scenario A contains all 13. Every project
   DESIGN.md includes only the ones its project-type matrix allows.
2. **Grown** — any contract added via `ds4a merge`. Its `###` header gets an
   `(grown)` marker: `### Checkbox (grown)`. Same format rules as core
   contracts. Version bumps per merge rules.
3. **Promoted** — a grown contract that keeps proving itself. When a grown
   contract has been included in 3+ separate project DESIGN.md generations,
   `ds4a review` outputs a promotion suggestion:
   `Promote [X] to core? [y/n]`. On yes: remove the `(grown)` marker and add
   it to the Core list here and in the project-type matrix.

## Rules

- **Core never demotes.** The merge loop is add-only; nothing is removed.
- **Matrix parity is checked at init.** Every matrix component must resolve to
  a contract in the library. If a matrix row has no contract, that's a bug —
  report it, don't paper over it.
- **Grown-candidates are not promises.** Checkbox/Switch/Alert/Tooltip are
  benchmark-backed but intentionally absent from the default. They enter a
  library the honest way: the project needed one → review detected the pattern
  → user approved → merge added the contract → reuse promotes it.
- **The floor grows, not shifts.** A new ds4a baseline version may ADD core
  contracts; it never replaces or restyles existing ones. Installed libraries
  only see additions when the user re-runs the conversion explicitly.

## Why a floor at all

AI agents without a component floor invent anatomy per project — three
different modals in one codebase, a fourth in the next. The benchmark floor
says: these 13 exist, with this anatomy, these states, these a11y rules.
Everything beyond the floor is the user's taste compounding through the loop.
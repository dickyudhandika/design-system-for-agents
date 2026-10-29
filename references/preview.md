# Preview

`/ds4a preview` runs:

```bash
python3 <skill>/scripts/build-preview.py --project .   # writes .ds4a/preview.html
open .ds4a/preview.html                                 # macOS; xdg-open on Linux
```

Flags: `--tone NAME` and `--type TYPE` override the overlay's `tone:` / `type:`;
`--out FILE` writes elsewhere; `--library DIR` points at another library.

One self-contained HTML file, generated from the **resolved tokens** (core + tone +
overlay), so it always reflects the active tone. Inline CSS and JS; the only
network requests are Google Fonts for non-system families, with system-font
fallback offline.

Sections, in order:
1. **Overview**: tone name, version, project type, the layers it resolved from
   (`core v1 + tone <name> v1 + project overlay`), and a contrast pill (pass, or
   N warnings from the same check as `resolve.py`).
2. **Principles**: the lead line and bullets of the Overview (the overlay's
   Overview when it has one), plus core's principles line.
3. **Color**: swatches grouped by token name: Surfaces, Text, Brand, States,
   then **Palette** (extra tone colors) and **Project** (colors the overlay
   adds). Text and action colors carry a WCAG contrast badge.
4. **Typography**: one specimen per font family, then all 16 scale steps
   rendered at real size.
5. **Spacing**, **Radius**, **Elevation** (shadow tokens and motion tokens from
   the tone's prose tables; hover a motion row to play it).
6. **Components**: all 13 core contracts with their states (Button variants x
   default/hover/focus/disabled, Input, Field, Fieldset, Form, Select open and
   closed, RadioGroup, Card, Badge, Modal, Tabs, Table, Sidebar). Each card
   shows the anatomy line from `library/core.md`. With a project type, cards
   are filtered by `component-matrix.md`; a "Show all" chip reveals the rest.
7. **Tokens**: the resolved frontmatter, collapsible.

Features:
- **Sidebar** with grouped navigation (Overview, Foundations, Components with
  each contract and a shown/total count, Reference) that highlights the section
  and component in view. Under 900px it becomes a scrolling section bar.
- **Top bar** with a breadcrumb that follows the scroll, the tone picker and
  search (`/` focuses it, `Esc` clears it). Search filters swatches, type rows,
  scale items and component cards by visible text and by token names/values.
- **Tone switcher**: every tone in `library/tones/` is resolved at build time
  and emitted as CSS variables under `[data-tone]`. "this project" is the
  project's result (tone + overlay); the other options are the raw library
  tones without the overlay, for comparison. The page chrome uses the same
  variables, so the whole page re-skins. Components are styled only through
  `--c-<component>-<key>` variables, so switching tone changes their shape,
  not just their colors. A tone that fails to resolve is skipped with a warning.
- **Motion** comes from the tone's motion tokens: hover feedback uses
  `duration.fast` + `ease.out`, glides and scrolling use `duration.smooth` +
  `ease.out`, open/close (select popup, sidebar collapse) uses `ease.in-out`.
  Only transform and opacity animate, except the sidebar collapse, whose
  contract specifies a width transition. `prefers-reduced-motion` turns all of
  it off.

Rules:
- Writes only `.ds4a/preview.html`. Never `src/`, never `scripts/` in the project.
- Open it for the user at the end of `/ds4a init`.
- If a dev server already serves an in-framework `/design-system` route, prefer
  that URL.

Other pieces in the repo: `templates/` (`DesignSystemExplorer.tsx`,
`design-system-page.astro`, `build-tokens.ts`) and `scripts/build-preview-html.ts`
are reference implementations for projects that want an in-framework
`/design-system` route. Never copied into a project by `init`.

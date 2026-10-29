# Preview

`/ds4a preview` runs:

```bash
python3 <skill>/scripts/build-preview.py --project .   # writes .ds4a/preview.html
open .ds4a/preview.html                                 # macOS; xdg-open on Linux
```

The page is generated from the **resolved tokens** (core + tone + overlay), so
it always reflects the active tone: color swatches with live contrast ratios
(text colors vs. `background`, `primary-foreground` vs. `primary`), the full type
scale, spacing bars, radius steps, shadows, and a sandbox of buttons, inputs,
badges, card, tabs and table styled only from tokens. One self-contained HTML
file; fonts load from Google Fonts when online and fall back to system fonts
offline.

Rules:
- Writes only `.ds4a/preview.html`. Never `src/`, never `scripts/` in the project.
- Open it for the user at the end of `/ds4a init`.
- If a dev server already serves an in-framework `/design-system` route, prefer
  that URL.

Other pieces in the repo:
- `preview/index.html` — legacy static showcase of the 13 contracts for the
  original warm-sharp look. Not tone-aware.
- `templates/` (`DesignSystemExplorer.tsx`, `design-system-page.astro`,
  `build-tokens.ts`) and `scripts/build-preview-html.ts` — reference
  implementations for projects that want an in-framework `/design-system` route.
  Never copied into a project by `init`.

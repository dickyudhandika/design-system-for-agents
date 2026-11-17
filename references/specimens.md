# Specimens — the project's real components in the preview

The core contracts say what the library promises. A specimen is a static copy of
what *this project* actually built:

```
.ds4a/specimens/pill.html
.ds4a/specimens/bookmark-card.html
```

`build-preview.py` renders them in the **Project specimens** section, above the
core contracts. They use the same CSS custom properties as the rest of the page
(`var(--color-primary)`, `var(--space-lg)`, `var(--radius-md)`,
`var(--shadow-elevated)`, `var(--t-title-h6)`), so the tone switcher re-skins
them.

## File format

```html
<!-- ds4a:specimen
title: Pill
source: src/components/Pill.tsx
captured: 2026-11-17
contract: Badge
-->
<span class="pill">
  <span class="pill-dot" aria-hidden="true"></span>
  Live
</span>
<style>
  .pill { display:inline-flex; gap:var(--space-xs); align-items:center;
          padding:var(--space-xs) var(--space-sm); border-radius:var(--radius-full);
          background:var(--color-muted); color:var(--color-foreground); }
</style>
```

- `title` defaults to a prettified file name.
- `source` is the component file this copy came from, relative to the project.
- `captured` is the date the copy was taken. If the source file's mtime is newer,
  `specimens list` and the preview show a drift warning.
- `contract` is optional. Name a core contract when this specimen is the
  project's version of it; the Contracts matrix then reports `Specimen` instead
  of `Enforced` (and `specimens` can replace an excluded contract).

Scope specimen CSS with a unique class. The page injects the markup directly so
custom properties cascade and tone switching works; a global selector in a
specimen would leak into the rest of the preview.

## Commands

```bash
python3 <skill>/scripts/specimens.py --project . scan
python3 <skill>/scripts/specimens.py --project . add pill --from src/components/Pill.tsx
python3 <skill>/scripts/specimens.py --project . add pill --html /tmp/pill.html --contract Badge
python3 <skill>/scripts/specimens.py --project . remove pill
python3 <skill>/scripts/specimens.py --project . list
```

- `scan` looks under `src/components`, `components`, `app/components`, `src/ui`,
  `src/sections`, `src/blocks` for `.tsx/.jsx/.astro/.svelte/.vue/.html` files
  with no specimen and no core contract. It writes nothing.
- `add` extracts the markup (best effort), writes the provenance header,
  registers the slug in the overlay's `specimens:` list, and rebuilds the
  preview. If extraction fails it writes a placeholder with the source path, so
  the agent or human can paste the real markup. `--no-build` skips the rebuild.
- `remove` deletes the file, unregisters it, and rebuilds.
- `list` prints metadata and drift/missing warnings.

## Registration

The overlay can order and filter specimens:

```yaml
specimens: [pill, bookmark-card]
```

When `specimens:` is absent, every `.html` file in the folder renders
(alphabetical). When it is present, only listed files render — a file not listed
is hidden without deleting it. `add` appends; `remove` deletes the entry.

## Drift

A specimen is a copy, so it can go stale. `source_status` compares the captured
date with the source file's mtime:

- `changed` — source newer than capture; preview shows "source changed since capture".
- `missing` — source path no longer exists; preview shows "source file missing".
- `ok` — no source, or source not newer.

`/ds4a diff` should list a changed specimen as a low-severity finding: recapture
with `specimens.py add <slug> --from <source> --force`, or update the copy by
hand and refresh `captured`.

## Non-goals

- No prop knobs, controls panel, or per-variant story files. Specimens are static
  renderings; hover/focus demonstrations are CSS.
- No iframe of the dev server. The preview stays one file with zero build
  integration.
- No rewriting of component source. Specimens are copies, not codegen.
- No script execution: `<script>` tags and inline event handlers are stripped.

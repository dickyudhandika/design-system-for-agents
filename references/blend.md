# Blend — migrate a hand-written DESIGN.md

A project can arrive with a design doc it already trusts. `/ds4a blend` treats
that doc as a **source**, not a target:

```
read DESIGN.md (frontmatter + tables) + read code tokens
        │
        ▼
report every conflict with both values and sources
        │
        ▼
write .ds4a/project.md (tokens + unique prose)
        │
        ├── keep both: DESIGN.generated.md beside the old doc
        └── adopt:   back up the old doc → regenerate DESIGN.md in place
```

The layers stay the source of truth. The old doc never becomes a second live
source: after adoption it is a backup, and `DESIGN.md` is generated.

## Commands

```bash
python3 <skill>/scripts/blend.py --project .                    # report only
python3 <skill>/scripts/blend.py --project . --write-overlay     # write the overlay
python3 <skill>/scripts/blend.py --project . --adopt             # overlay + regenerate DESIGN.md
python3 <skill>/scripts/blend.py --project . --prefer doc        # keep doc values on conflict
```

- Default is a dry run: nothing is written.
- `--write-overlay` writes `.ds4a/project.md` (existing overlay is backed up as
  `project.md.<timestamp>.bak`). If `DESIGN.md` is hand-written, resolve writes
  `DESIGN.generated.md` beside it — the "keep both" mode.
- `--adopt` is the single-file end state: it backs up the old doc to
  `.ds4a/DESIGN.md.pre-ds4a.md`, writes the overlay, regenerates `DESIGN.md`,
  and removes a stale `DESIGN.generated.md`. Only run it after the user
  confirms adoption.

## What it reads

Doc frontmatter under `colors`, `typography`, `rounded`, `spacing`,
`components`; plus the token tables under `## Colors` (Token/Value/Role),
`## Typography` → `### Size scale`, `## Layout` → `### Spacing system`, and
`## Shapes` → `### Radius scale`.

Code: CSS custom properties (`--color-*`, `--spacing-*`, `--radius-*`,
`--font-size-*`) in `globals.css`, `tokens.css`, `@theme`, and other CSS files;
DTCG/JSON token files (`color.*`, `spacing.*`, `radius.*`, `typography.*`); and
`colors` / `spacing` / `borderRadius` / `fontSize` object literals in typed token
files and `tailwind.config.*`.

## Conflicts

A conflict is the same token with different values in the doc and in code. The
report prints both, with the source:

```
colors.primary: DESIGN.md #2563EB / code #1A5EFF
```

`--prefer code` (default) takes the code value; `--prefer doc` takes the doc's.
Either way both are printed — never silently resolved. A value that exists in
only one source is imported from there.

Existing overlay values win over both: the overlay is the latest decision. The
report still shows the conflict, so the user can choose to remove the override.

## Prose

Bullets from the doc's rule sections (`Colors`, `Typography`, `Layout`,
`Elevation & Depth`, `Shapes`, `Components`, `Do's and Don'ts`, `Pre-flight
Checklist`) are kept only when they are not already in core+tone. They land in
the overlay as `### Project notes`. Tables and code fences are not copied; they
are token sources.

This is deliberately conservative: prose that is already covered by a contract
is dropped, and rules that contradict the library stay visible in the overlay
instead of being silently deleted.

## Limits

- The doc parser understands the tables ds4a itself generates and the common
  hand-written equivalents. Irregular prose-only token lists are reported as
  missing, not guessed.
- `components` prose is not promoted to contracts by `blend`; that is `diff` →
  `merge` territory. Only tokens move automatically.
- A doc written in a different schema may need `--prefer doc` and a manual pass
  over the overlay.
- `--adopt` deletes a stale `DESIGN.generated.md` but keeps the pre-adopt backup
  permanently.

# Detection — find the project's existing design system

`/ds4a init` and `init --check` run this flow. It reads, never writes, project
files. The only output is `.ds4a/project.md` (the overlay), and `--check` doesn't
even write that.

```
find sources → extract tokens → normalize to the tone schema → write overlay
→ fill the gaps from the neutral tone → resolve → report
```

## 1. Find sources (check all; combine what's found)

| Source | Contains | Parser |
|---|---|---|
| `.ds4a/project.md` | Already initialized | Skip detection; re-resolve |
| `AGENTS.md` | Rules + guardrails in prose | Rules → overlay prose; values → discrepancy check |
| `tokens.json`, `src/tokens/tokens.json` | Token values (JSON/DTCG) | Map keys below |
| `tokens.css`, `src/tokens/tokens.css`, `tokens.generated.css` | CSS custom properties | `--color-*` etc. |
| `globals.css` with `--background` + `--primary` | shadcn theme (oklch) | `references/shadcn-baseline.md` |
| `components.json`, `@radix-ui/*`, `@base-ui/*` in package.json | shadcn / Base UI project | Hint only |
| `design-tokens.ts`, `tokens.ts` | Typed token registry | Source of truth (see §5) |
| `global.css` / `style.css` with `@theme { }` | Tailwind v4 theme | `--color-*`, `--font-*`, `--radius-*` |
| `tailwind.config.js/ts` | Colors, fonts, spacing in JS | `theme.extend` / `theme` |
| `DESIGN.md` | A hand-written design doc | **Never overwrite.** Read it as a source; write elsewhere (`--out`). |

No source found → `tone: neutral`, empty overlay. That is the "no design
system" path: structure from core, neutral tokens, grown later.

## 2. Extract

```css
:root { --color-primary:#1A5EFF; --spacing-xl:24px; --font-size-label-md:16px; --radius-md:8px }
```
Map `--color-*` → `colors.*`, `--spacing-*` → `spacing.*`,
`--font-size-*` → `typography.*.fontSize`, `--radius-*` → `rounded.*`,
`--shadow-*` → Elevation prose, `--font-family*` → `typography.*.fontFamily`.

```js
// tailwind.config
colors: { primary: '#1A5EFF' }   → colors.primary
spacing: { xl: '24px' }          → spacing.xl
borderRadius: { sm: '0px' }      → rounded.sm
fontFamily: { sans: ['Inter'] }  → typography.*.fontFamily
```

```css
/* Tailwind v4 */
@theme { --color-brand: #6366f1; --font-display: 'Geist'; --radius-card: 0.5rem; }
```

oklch values (shadcn, Tailwind v4 defaults) → hex via
`cat globals.css | python3 scripts/oklch-to-hex.py`.

## 3. Normalize → overlay

Write **only keys that were found** into the overlay frontmatter, using the
tone schema (`colors`, `typography`, `rounded`, `spacing`, `components`). Keep
the source in an end-of-line comment (`# imported --primary`).

- Color names that don't exist in core's required set (`chart-1`, `accent`,
  `sidebar-*`) are kept — resolve lists them under "Token roles".
- shadcn `--radius` → the 5-step `rounded` scale (table in `shadcn-baseline.md`).
  Component radii follow `rounded.*` automatically.
- Light mode only unless the user asks for dark.

## 4. Derive guardrails (overlay prose, `## Do's and Don'ts`)

Only from what was found:

- `primary` saturated → "primary for CTAs and active states only" (already in core; skip)
- all radius 0 → "Do use 0px for all elements"; any radius > 0 → "Don't mix radius values; take them from the scale"
- spacing scale found → "Don't invent spacing outside the scale"
- A rule in AGENTS.md → copy it verbatim into the matching section

Never invent a token that isn't in the source.

## 5. Typed pipelines (source of truth)

If `src/lib/design-tokens.ts` (or DTCG JSON) exists it is the single source of
truth; CSS (`tokens.generated.css`, `@theme`) is a build artifact compiled from
it (see `templates/build-tokens.ts`). Record that in the overlay:

```yaml
source-of-truth: src/lib/design-tokens.ts
```

and tell the user token edits happen there, never in generated CSS.

## 6. Discrepancy check (AGENTS.md projects)

Before trusting prose, grep AGENTS.md for stale values: color names ("mint" vs
"blue"), radius (4/8/16px vs 0px), legacy token names. Token files win over
prose. Fix the *overlay copy*, never the user's AGENTS.md.

## 7. Report

```
Found: <sources>. Imported N tokens (colors a, type b, radius c, spacing d).
Gaps filled from neutral: <groups>.
Contrast: <pass | warnings from resolve.py>.
```

## 8. Existing `DESIGN.md` — drift check and the adopt decision

If the project has a hand-written `DESIGN.md`, it is stale the moment code moves on.
Before writing anything, diff the doc against the extracted tokens and report
conflicts **with both values and their sources** — never silently pick one:

- frontmatter `colors.*`, `typography.*`, `rounded.*`, `spacing.*` vs the values
  found in CSS/Tailwind/DTCG (code usually wins; prose is what went stale)
- any value quoted in prose (sizes, breakpoints, radii) vs the token files
- doc-only components/sections vs what the matrix admits for this type

Token files win for the overlay itself, but the conflict goes in the report and
the user decides. Then ask, before writing any file:

1. **keep both** — overlay + generated doc beside `DESIGN.md` (both docs exist;
   the user maintains the boundary). Default if the user says nothing.
   `blend.py --write-overlay` writes `DESIGN.generated.md` beside the old doc.
2. **adopt** — the generated doc becomes the visual source of truth; record the
   drift fixes in the overlay, and mark `DESIGN.md` as superseded (header note,
   or delete if the user asks). `blend.py --adopt` is the one command: it backs
   up the old doc to `.ds4a/DESIGN.md.pre-ds4a.md`, writes the overlay, resolves,
   and replaces `DESIGN.md`. `resolve.py --adopt` is the direct flag when the
   overlay is already correct.
3. **abort** — write nothing.

Never present the generated doc as "the" design system while `DESIGN.md` also
claims that role. Two unlabelled sources of truth is the failure mode this
check exists to prevent.

`blend.py` automates the mechanical part of this: it extracts doc tokens and
unique bullets, compares them with code token files, prints every conflict with
both values and sources, and writes the overlay. It never chooses silently:
`--prefer code` (default) or `--prefer doc` decides, and the report says so.

Overlay frontmatter is metadata plus tokens. `tone`, `type`,
`exclude_components`, `specimens`, `source-of-truth`, `adopted` and `blended`
are consumed by ds4a and never appear in `DESIGN.md`; only the token groups
(`colors`, `typography`, `rounded`, `spacing`, `components`) are merged.

Where the project contradicts the library outright (no tabs, no shadows, chips
instead of tabs), encode it structurally, not as advice:

- `exclude_components: [Tabs, Card]` in the overlay frontmatter drops those
  contracts from the output entirely.
- A `<!-- replace -->` first line in an overlay `## Section` drops core+tone
  content for that section instead of appending below it.

Prose like "we don't use shadows" appended below a core section that mandates
`shadow.subtle` is not enough — the reader gets two contradictory rules.

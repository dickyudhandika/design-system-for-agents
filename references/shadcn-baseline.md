# shadcn/ui Baseline Import (ds4a detection source)

When a project uses shadcn/ui (or the user customized a theme at
https://ui.shadcn.com/create), ds4a imports the theme from `globals.css`
instead of installing the curated default. The user's theme is the
**foundation** (behavior + anatomy + tokens from the market), ds4a is the
**taste overlay** (guardrails, contracts, rules).

## Detection

shadcn is detected (see `references/detection.md`) when the project has shadcn-style CSS variables:

```css
:root {
  --background: oklch(...);
  --primary: oklch(...);
  --radius: 0.625rem;
}
```

Detect by: `globals.css` (or equivalent) contains `--background` and
`--primary` CSS variables. Also detect `components.json` (shadcn config)
or `@radix-ui` / `@base-ui` in package.json.

## Flow

```
1. Read globals.css → extract :root (light) + .dark blocks
2. Convert oklch → hex      → scripts/oklch-to-hex.py
3. Map shadcn vars → ds4a YAML frontmatter tokens
4. Derive guardrails from theme patterns (see `references/detection.md` §4)
5. Generate DESIGN.md — hex values, oklch source noted in frontmatter comment
6. Report: "Found shadcn theme. Imported [N] tokens from globals.css.
   DESIGN.md generated."
```

## Variable Mapping (shadcn → ds4a)

| shadcn var | ds4a token | Notes |
|---|---|---|
| `--background` | colors.background | Main canvas |
| `--foreground` | colors.foreground | Primary text |
| `--card` / `--card-foreground` | colors.card / card-foreground | Surface; often same as bg |
| `--popover` / `--popover-foreground` | colors.popover / popover-foreground | Overlay surface |
| `--primary` / `--primary-foreground` | colors.primary / primary-foreground | Action color |
| `--secondary` / `--secondary-foreground` | colors.secondary / secondary-foreground | Secondary action |
| `--muted` / `--muted-foreground` | colors.muted / muted-foreground | Subtle bg + secondary text |
| `--accent` / `--accent-foreground` | colors.accent / accent-foreground | Hover/selected bg |
| `--destructive` | colors.destructive | Errors, destructive actions |
| `--border` | colors.border | Separating content |
| `--input` | colors.border | Input borders (often same) |
| `--ring` | colors.focus-ring | Focus ring; fallback primary |
| `--radius` | rounded.* | Map to scale (see below) |
| `--chart-1..5` | colors.chart-1..5 | Data viz palette |
| `--sidebar*` | colors.sidebar.* | Sidebar surface tokens |

**ds4a tokens NOT covered by shadcn:** typography, spacing, shadows,
motion. These come from the `neutral` tone (or the tone named in
`.ds4a/project.md`) — ds4a owns structure for non-color axes. If the project has Tailwind config with fonts/spacing,
merge those in too.

## Radius Conversion

shadcn uses a single `--radius` value; ds4a uses a 5-step scale. Map:

| shadcn `--radius` | ds4a rounded.* |
|---|---|
| 0rem | all 0px |
| 0.25rem | xs: 2px, sm: 4px, md: 4px, lg: 6px |
| 0.375rem | xs: 2px, sm: 4px, md: 6px, lg: 8px |
| 0.5rem | xs: 4px, sm: 6px, md: 8px, lg: 10px |
| 0.625rem (default) | xs: 4px, sm: 6px, md: 10px, lg: 12px |
| 0.75rem | xs: 4px, sm: 8px, md: 12px, lg: 16px |
| 1rem | xs: 4px, sm: 8px, md: 16px, lg: 20px |

## Dark Mode

shadcn ships `.dark` block. Two approaches:

1. **Light only (default):** Use `:root` values. Note in DESIGN.md:
   "Dark theme exists in globals.css (`.dark`). ds4a covers light mode;
   dark tokens preserved in globals.css but not in DESIGN.md."
2. **Full dark support:** Add `colors.dark` subsection to YAML frontmatter
   with the `.dark` block converted. Schema extension:
   ```yaml
   colors:
     ...
     dark:
       background: "#0A0A0A"
       foreground: "#FAFAFA"
       ...
   ```

Default to light-only unless the user asks for dark.

## Guardrail Derivation

Same derivation rules as `references/detection.md` §4, applied to imported values:

- If `--primary` is saturated → "primary for CTAs and active states only"
- If `--destructive` exists → "destructive for errors only"
- If `--radius` is 0rem → "sharp edges, deliberate aesthetic choice"
- If `--radius` > 0 → "consistent radius from scale; don't mix values"
- If `--muted-foreground` contrast passes AA → "use for secondary text"
- Contrast check: verify `muted-foreground` vs `background` passes 4.5:1.
  If not, flag: "muted-foreground fails AA — adjust or use foreground."

## Oklch Conversion

shadcn themes are `oklch()` colors. Convert to hex for DESIGN.md (agents
and YAML speak hex). Script: `scripts/oklch-to-hex.py`.

```bash
cat globals.css | python3 scripts/oklch-to-hex.py
```

Preserves variable names and block structure. Non-color vars (`--radius`)
pass through untouched. Alpha values emit 8-digit hex.

## Component Mapping (shadcn anatomy → ds4a contracts)

shadcn components are already styled + accessible (Radix/Base UI + Tailwind).
ds4a contracts add taste rules on top:

| ds4a contract | shadcn component | ds4a adds |
|---|---|---|
| Button | `<Button variant="default">` | variant→role mapping, size scale |
| Input | `<Input>` | error state, label pairing |
| Card | `<Card>` | padding, border vs shadow choice |
| Badge | `<Badge>` | semantic variant mapping |
| Select | `<Select>` | trigger styling, popup elevation |
| Field/Form | `<Form>` + `<Label>` | validation UX, gap scale |
| RadioGroup | `<RadioGroup>` | layout, indicator styling |
| Modal | `<Dialog>` | backdrop, focus trap notes |
| Tabs | `<Tabs>` | underline vs pill convention |
| Table | `<Table>` | density, row hover, sort states |
| Sidebar | `<Sidebar>` | width, nav item states |
| Tooltip | `<Tooltip>` | delay, placement, arrow |
| Popover | `<Popover>` | trigger types, dismiss rules |

**Rule:** For shadcn projects, contracts reference the shadcn component by
name instead of inventing a new anatomy. ds4a owns the *taste decisions*
(variants, sizes, states, rules); shadcn owns the *implementation*
(structure, accessibility, behavior).

## Do's and Don'ts

- ✅ Do import the user's customized theme — it's the source of truth.
- ✅ Do convert oklch → hex; keep the source noted in frontmatter comment.
- ✅ Do map `--ring` to focus-ring; fall back to primary if absent.
- ✅ Do keep typography/spacing/shadows from the project's tone (`neutral` by default).
- ❌ Don't overwrite the user's globals.css. DESIGN.md is additive.
- ❌ Don't invent tokens that don't exist in the theme.
- ❌ Don't skip the AA contrast check on muted-foreground.

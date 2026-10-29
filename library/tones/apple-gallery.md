---
version: 2
name: apple-gallery
description: >-
  The product page as a white gallery. Pure white canvas, Studio Mist feature bands,
  near-black SF-style type with tight negative tracking, 28px media frames, and one
  saturated blue reserved for compact conversion pills and inline links. Flat,
  shadowless, photography-led. Transcribed 1:1 from the Apple store style reference.
colors:
  # ── Reference palette, verbatim (every --color-* in the source) ──
  gallery-white: "#FFFFFF"         # --color-gallery-white. Page canvas, hero, product story, feature-card surface.
  studio-mist: "#F5F5F7"           # --color-studio-mist. Alternate section band, carousel backdrop, footer.
  paper-frost: "#FAFAFC"           # --color-paper-frost. Opened global-navigation surface, secondary pale fill.
  hairline-silver: "#D6D6D6"       # --color-hairline-silver. 1px dividers and restrained control outlines.
  control-gray: "#E6E6E8"          # --color-control-gray. Disabled fills, subdued utility surfaces, nav edge.
  ink: "#1D1D1F"                   # --color-ink. Headlines, body copy, nav labels, dark utility icons.
  slate: "#707070"                 # --color-slate. Secondary copy, legal text, low-emphasis glyphs.
  steel: "#86868B"                 # --color-steel. Input outlines, inactive indicators, outlined-control edges.
  apple-blue: "#0066CC"            # --color-apple-blue. Inline links and blue text controls. Never a fill.
  pricing-blue: "#0071E3"          # --color-pricing-blue. Filled pricing and learn-more controls.
  launch-orange: "#B64400"         # --color-launch-orange. Launch-status labels. Bare text only.
  # ── Semantic roles (aliases into the palette; core contracts read these) ──
  background: "#FFFFFF"            # = gallery-white.
  foreground: "#1D1D1F"            # = ink.
  secondary: "#707070"             # = slate.
  muted: "#F5F5F7"                 # = studio-mist.
  border: "#D6D6D6"                # = hairline-silver.
  muted-foreground: "#707070"      # = slate.
  primary: "#0071E3"               # = pricing-blue.
  primary-foreground: "#FFFFFF"    # #ffffff on #0071e3 = 4.70:1.
  destructive: "#B64400"           # Not in the source. Core requires the role; launch-orange fills it (5.50:1).
typography:
  # ── Display: SF Pro Display 400/500/600, sizes 19/21/24/28/40/48/80, tracking -0.015em→0.012em ──
  title-h1:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 80px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -1.2px
  title-h2:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: -0.72px
  title-h3:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.0
    letterSpacing: 0px
  title-h4:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: -0.42px
  title-h5:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.17
    letterSpacing: -0.36px
  title-h6:
    fontFamily: "'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 21px
    fontWeight: 600
    lineHeight: 1.0
    letterSpacing: 0.231px
  # ── Labels: SF Pro Text 400/500/600 ──
  label-xl:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: -0.3px
  label-lg:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 17px
    fontWeight: 500
    lineHeight: 1.47
    letterSpacing: -0.374px
  label-md:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: -0.224px
  label-sm:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: -0.12px
  label-xs:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: -0.12px
  # ── Paragraphs: SF Pro Text 400 ──
  paragraph-xl:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 26px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: -0.39px
  paragraph-lg:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: -0.3px
  paragraph-md:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.47
    letterSpacing: -0.374px
  paragraph-sm:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.29
    letterSpacing: -0.224px
  paragraph-xs:
    fontFamily: "'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: -0.12px
rounded:
  # ── Core's 5 contract slots, filled from the named radii ──
  xs: 0px       # = badges 0px
  sm: 10px      # = links 10px
  md: 20px      # = navigation 20px
  lg: 28px      # = cards / images 28px
  full: 9999px  # = buttons; pills 36px and inputs 980px are separate named values
  # ── Every other named radius in the source ──
  link: 10px
  nav: 20px
  card: 28px
  image: 28px
  pill: 36px
  badge: 0px
  input: 980px
  button: 9999px
  raw-md: 4px
  raw-2xl: 20px
  raw-3xl: 32px
  raw-3xl-2: 36px
  raw-full: 120px
  raw-full-2: 170px
  raw-full-3: 980px
  raw-full-4: 999px
  raw-full-5: 9999px
spacing:
  # ── Core's 8 contract slots, filled with real scale steps ──
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
  # ── Remaining scale steps (--spacing-*); section gap 90 / card padding 28 / element gap 20 live in Layout ──
  20: 20px
  28: 28px
  40: 40px
  52: 52px
  76: 76px
  80: 80px
  128: 128px
  144: 144px
components:
  button:
    radius: 9999px
    padding-sm: "6px 14px"
    padding-md: "8px 16px"
    padding-lg: "12px 24px"
    font-size-sm: 12px
    font-size-md: 12px
    font-size-lg: 17px
    font-weight: 400
    gap: 8px
    variants: [primary, secondary, ghost]
  input:
    radius: 980px
    padding-sm: "10px 32px 10px 20px"
    padding-md: "12px 45px 12px 24px"
    padding-lg: "14px 52px 14px 28px"
    font-size-sm: 13px
    font-size-md: 13px
    font-size-lg: 13px
    font-weight: 400
    border: "1px solid #86868B"
    variants: [default, error]
  card:
    radius: 28px
    padding: 28px
    border: "none"
    variants: [default, flush]
  badge:
    radius: 0px
    padding: "0px"
    font-size: 12px
    font-weight: 600
    gap: 4px
    variants: [default]
  field:
    label-font-size: 14px
    label-font-weight: 500
    description-font-size: 14px
    description-color: muted-foreground
    error-font-size: 14px
    error-color: destructive
    gap: 8px
  fieldset:
    legend-font-size: 17px
    legend-font-weight: 500
    gap: 12px
  form:
    gap: 20px
  select:
    radius: 980px
    padding: "12px 45px 12px 24px"
    font-size: 13px
    font-weight: 400
    popup-radius: 20px
    popup-padding: 4px
    popup-max-height: 320px
    icon-rotation: 180deg
  radio-group:
    gap: 8px
    radio-card-padding: 20px
    radio-card-gap: 16px
    radio-card-padding-mobile: 16px
    checked-background: "rgba(0,113,227,0.06)"
  modal:
    radius: 28px
    padding: 28px
    width-sm: 360px
    width-md: 540px
    width-lg: 720px
    backdrop: "rgba(0, 0, 0, 0.32)"
    shadow: subtle
    header-gap: 12px
    footer-gap: 20px
    variants: [sm, md, lg]
  tabs:
    radius: 0px
    trigger-padding: "12px 0px"
    trigger-font-size: 14px
    trigger-font-weight: 500
    indicator-height: 1px
    indicator-color: primary
    list-border: "1px solid var(--color-hairline-silver)"
    variants: [underline]
  table:
    radius: 0px
    row-padding: "14px 20px"
    header-font-size: 12px
    header-font-weight: 500
    header-color: muted-foreground
    cell-font-size: 14px
    cell-font-weight: 400
    row-border: "1px solid var(--color-hairline-silver)"
    hover-background: studio-mist
    selected-background: "rgba(0,113,227,0.05)"
    variants: [default]
  sidebar:
    radius: 20px
    width: 280px
    item-padding: 12px
    item-font-size: 14px
    item-font-weight: 500
    item-gap: 4px
    section-header-padding: "8px 12px"
    section-header-font-size: 12px
    active-indicator: "2px solid #0071E3"
    container-border: "1px solid var(--color-hairline-silver)"
    variants: [default]
---

<!--
Tone pack: apple-gallery — the product page as a white gallery.
Tokens live in the frontmatter above. Prose below is tone-only: personality and
the rules that exist because of this tone. Structure, component contracts, and
universal guardrails come from library/core.md.

Transcription policy: every value in the source appears verbatim, under its own
name, in the reference tables below. The frontmatter is the mechanical layer —
core.md's contracts can only point at `colors.<role>`, `rounded.<5 slots>`,
`spacing.<8 slots>`, and `typography.<16 roles>`, so the palette is also mirrored
into those fixed slots. Where a source value has no slot (pill 36px, input 980px,
spacing-52, hero tracking -1.2px) it is carried under its own key rather than
rounded to a neighbor.
-->

## Overview

The product page as a white gallery. Enormous product photography occupies the
centre while compact black typography gives each claim a controlled, almost
editorial weight.

- **The product is the visual event.** Hardware renders sit directly on
  `{{colors.gallery-white}}` with no containing card, or inside a shadowless
  `{{rounded.lg}}` frame on `{{colors.studio-mist}}`.
- **White, then one mist band.** `{{colors.gallery-white}}` for hero and
  editorial chapters; `{{colors.studio-mist}}` for full-width feature bands and
  the footer. No third surface, no tinted canvas.
- **Type is compact, not promotional.** `{{typography.title-h1.fontSize}}` at
  weight `{{typography.title-h1.fontWeight}}` tightens to
  `{{typography.title-h1.letterSpacing}}` — the largest type feels smaller than
  it is.
- **One saturated blue in two jobs.** `{{colors.pricing-blue}}` fills compact
  conversion controls; `{{colors.apple-blue}}` colors inline links. Both are
  small punctuation marks against a monochrome page.
- **Elevation is a hairline.** Separation comes from white against
  `{{colors.studio-mist}}`, `{{rounded.card}}` corners, and 1px
  `{{colors.hairline-silver}}` edges. Nothing casts a shadow.

## Colors

### Reference palette

Every token in the source, verbatim.

| Token | Value | Role |
|---|---|---|
| `--color-gallery-white` | `#ffffff` | Primary page canvas, hero background, product story sections, feature-card surfaces |
| `--color-studio-mist` | `#f5f5f7` | Alternate full-width section background, feature-stage backdrop, footer surface, muted content blocks |
| `--color-paper-frost` | `#fafafc` | Opened global-navigation surface, secondary pale fill |
| `--color-hairline-silver` | `#d6d6d6` | 1px dividers, restrained control outlines, subtle separators |
| `--color-control-gray` | `#e6e6e8` | Disabled control fills, subdued utility surfaces, single-pixel navigation edge |
| `--color-ink` | `#1d1d1f` | Headlines, primary body copy, navigation labels, dark utility icons |
| `--color-slate` | `#707070` | Secondary copy, legal text, subdued navigation content, low-emphasis glyphs |
| `--color-steel` | `#86868b` | Input outlines, inactive indicators, fine outlined-control edges |
| `--color-apple-blue` | `#0066cc` | Inline links, section links, blue text controls |
| `--color-pricing-blue` | `#0071e3` | Filled pricing and learn-more controls |
| `--color-launch-orange` | `#b64400` | Small launch-status labels such as new-product markers |

### Tone rules

- **`background` is pure white here.** `{{colors.gallery-white}}` is the gallery
  wall. Do not tint it toward cream or gray.
- **`muted` is a full band, not a chip.** `{{colors.studio-mist}}` spans a section
  width; never a small pill fill.
- **Two blues, two jobs, no interchange.** `{{colors.pricing-blue}}` for filled
  controls, `{{colors.apple-blue}}` for text links. Never the reverse.
- **`launch-orange` is bare text.** 12px, weight 600, no background, border, or
  pill.
- **`border` is a hairline.** `{{colors.hairline-silver}}` draws 1px separators
  only — never a card outline, never doubled to 2px.

## Typography

### Reference families

| Token | Stack | Weights | OpenType |
|---|---|---|---|
| `--font-sf-pro-display` | `'SF Pro Display', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | 400, 500, 600 | `"numr"` |
| `--font-sf-pro-text` | `'SF Pro Text', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | 400, 500, 600 | `"numr"` |
| `--font-arial` | `'Arial', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | 400 | — |

- **SF Pro Display** sizes 19, 21, 24, 28, 40, 48, 80px · line heights 1.00, 1.05,
  1.08, 1.14, 1.17, 1.21, 1.33, 1.38 · tracking -1.2px at 80px, normal at 40px,
  +0.23px at 19–21px, profile -0.015em to 0.012em.
- **SF Pro Text** sizes 10, 12, 14, 17, 20, 26, 44px · line heights 1.00, 1.18,
  1.24, 1.29, 1.33, 1.43, 1.47 · tracking -0.37px at 10px, -0.12px at 12px,
  -0.22px at 14px, -0.37px at 17px, profile -0.037em to -0.003em.
- **Arial** 13px/1.20, weight 400 — search/input fallback only.

### Reference type scale

| Role | Family | Weight | Size | Line height | Tracking | Token |
|---|---|---|---|---|---|---|
| global-nav | SF Pro Text | 400 | 12px | 1 | -0.12px | `--text-global-nav` |
| compact-control | SF Pro Text | 400 | 12px | 1.33 | -0.12px | `--text-compact-control` |
| body-small | SF Pro Text | 400 | 14px | 1.29 | -0.224px | `--text-body-small` |
| body | SF Pro Text | 400 | 17px | 1.47 | -0.374px | `--text-body` |
| feature-copy | SF Pro Text | 400 | 17px | 1.24 | -0.374px | `--text-feature-copy` |
| product-nav-title | SF Pro Display | 600 | 19px | 1.21 | 0.228px | `--text-product-nav-title` |
| product-kicker | SF Pro Display | 600 | 21px | 1 | 0.231px | `--text-product-kicker` |
| feature-heading | SF Pro Display | 600 | 40px | 1 | 0px | `--text-feature-heading` |
| hero-display | SF Pro Display | 600 | 80px | 1.05 | -1.2px | `--text-hero-display` |

### Tone rules

- **Two families, split by role.** Display for H1–H6; Text for navigation, body,
  links, buttons, pricing, footnotes. Arial is reserved for the search field.
- **Negative tracking scales with size.** Display tightens to
  `{{typography.title-h1.letterSpacing}}`; body sits at
  `{{typography.paragraph-md.letterSpacing}}`; interface labels at
  `{{typography.label-sm.letterSpacing}}`.
- **Body is 17px, not 16px.** `{{typography.paragraph-md.fontSize}}` at
  `{{typography.paragraph-md.lineHeight}}`. Feature statements may tighten to the
  source's 1.24 line height (`--text-feature-copy`).
- **Weight 600 tops out.** Nothing is set at 700, and nothing is set wide.
- **The kicker opens up.** 21px at `{{typography.title-h6.letterSpacing}}` —
  the one positive-tracked role.
- **Small text carries `numr`.** Enable the `numr` feature wherever prices,
  counts, or specs are set.

## Layout

### Layout tokens

| Token | Value |
|---|---|
| `--section-gap` | 90px |
| `--card-padding` | 28px |
| `--element-gap` | 20px |

### Reference spacing scale

| Token | Value | | Token | Value |
|---|---|---|---|---|
| `--spacing-4` | 4px | | `--spacing-48` | 48px |
| `--spacing-8` | 8px | | `--spacing-52` | 52px |
| `--spacing-12` | 12px | | `--spacing-64` | 64px |
| `--spacing-16` | 16px | | `--spacing-76` | 76px |
| `--spacing-20` | 20px | | `--spacing-80` | 80px |
| `--spacing-24` | 24px | | `--spacing-128` | 128px |
| `--spacing-28` | 28px | | `--spacing-144` | 144px |
| `--spacing-32` | 32px | | | |
| `--spacing-40` | 40px | | | |

Base unit 4px. Density: comfortable.

### Tone rules

- **90px between storytelling sections.** `--section-gap`, not a spacing step.
- **20px between related elements.** `--element-gap`.
- **One idea per band.** A single claim plus its imagery; don't stack two
  competing messages in one white band.
- **Text beside oversized imagery.** Left-aligned statement, image entering from
  the opposite edge and allowed to crop. Keep the text column narrow.
- **No visible grid.** No column rules, no boxed panels, no dashboard chrome.

## Elevation & Depth

### Shadow tokens

The source defines elevation as a 1px ring. There are no cast shadows.

| Token | Value | Use for |
|---|---|---|
| `subtle` | `rgb(230, 230, 232) 0px 0px 0px 1px` | Navigation edges, selected controls, modal edge |
| `subtle-2` | `rgb(134, 134, 139) 0px 0px 0px 1px` | Outlined pills, input edges, focus rings |

### Surface levels

| Level | Name | Value | Purpose |
|---|---|---|---|
| 0 | Gallery White | `#ffffff` | Hero, editorial canvas, local navigation, feature-card surface |
| 1 | Studio Mist | `#f5f5f7` | Alternate section band, carousel backdrop, muted content, footer |
| 2 | Paper Frost | `#fafafc` | Opened global-navigation layer |
| 3 | Control Gray | `#e6e6e8` | Disabled utility-control fill, thin navigation edge |

### Motion tokens

| Token | Value | Use for |
|---|---|---|
| `duration.fast` | 150ms | Button press, hover feedback |
| `duration.smooth` | 300ms | Panels, modals, navigation reveal |
| `ease.out` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Default. Calm deceleration. |
| `ease.in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric transitions |

## Shapes

### Named radii (source)

| Element | Value | Token |
|---|---|---|
| cards | 28px | `--radius-cards` |
| links | 10px | `--radius-links` |
| pills | 36px | `--radius-pills` |
| badges | 0px | `--radius-badges` |
| images | 28px | `--radius-images` |
| inputs | 980px | `--radius-inputs` |
| buttons | 9999px | `--radius-buttons` |
| navigation | 20px | `--radius-navigation` |

### Radius tokens (source)

`--radius-md: 4px` · `--radius-lg: 10px` · `--radius-2xl: 20px` ·
`--radius-3xl: 28px` · `--radius-3xl-2: 32px` · `--radius-3xl-3: 36px` ·
`--radius-full: 120px` · `--radius-full-2: 170px` · `--radius-full-3: 980px` ·
`--radius-full-4: 999px` · `--radius-full-5: 9999px`

### Why 28px?

**Media frames are the only large rounding.** Cards, images, and media frames sit
at `{{rounded.card}}` so hardware softens without the page reading as a card
dashboard. Controls go fully round — buttons `{{rounded.button}}`, inputs
`{{rounded.input}}`. Navigation floats at `{{rounded.nav}}`. Badges stay square.

- **Don't swap 28px for 8px, 12px, or square corners.**
- **Pills at 36px are the carousel control**, not the CTA. 9999px is for buttons.
- **Tables and tabs are unrounded.** Rules, not frames.

## Do's and Don'ts

### Tone: apple-gallery

- ✅ **Do** use `{{colors.gallery-white}}` as the product-story canvas and reserve
  `{{colors.studio-mist}}` for full-width bands and the footer.
- ✅ **Do** set hero statements at `{{typography.title-h1.fontSize}}` /
  `{{typography.title-h1.fontWeight}}` with
  `{{typography.title-h1.letterSpacing}}` tracking.
- ✅ **Do** use `{{typography.paragraph-md.fontSize}}` / 400 with
  `{{typography.paragraph-md.letterSpacing}}` for feature paragraphs.
- ✅ **Do** use `{{rounded.card}}` for feature cards and contained media, with no
  shadow.
- ✅ **Do** use `{{colors.pricing-blue}}` only for compact filled controls with
  white `{{typography.label-sm.fontSize}}` text.
- ✅ **Do** use `{{colors.apple-blue}}` for inline links and textual section links.
- ✅ **Do** space major sections by `--section-gap` (90px) and keep related
  elements at `--element-gap` (20px).
- ❌ **Don't** add gradients. Product imagery supplies color and depth.
- ❌ **Don't** put shadows on feature cards, editorial blocks, or floating pricing
  capsules.
- ❌ **Don't** replace the `{{rounded.card}}` feature radius with 8px, 12px, or
  square corners.
- ❌ **Don't** use `{{colors.pricing-blue}}` as a large hero background or a
  universal filled button color.
- ❌ **Don't** set display headlines at weight 700 or tracking wider than
  `{{typography.title-h1.letterSpacing}}`.
- ❌ **Don't** put launch labels in colored pills — bare
  `{{colors.launch-orange}}` 12px/600 text.
- ❌ **Don't** place dense boxed UI panels over product renders. Keep white space
  around the hardware.

## Pre-flight Checklist

- [ ] **Two blues, correct jobs?** Filled controls `pricing-blue`, links
      `apple-blue`. Never reversed.
- [ ] **Shadowless surfaces?** Only 1px rings. Feature cards, editorial blocks,
      callouts: no box-shadow.
- [ ] **Radius from the named set?** Media `{{rounded.card}}`, buttons
      `{{rounded.button}}`, inputs `{{rounded.input}}`, nav `{{rounded.nav}}`,
      badges `{{rounded.badge}}`.
- [ ] **Tracking negative on display?** H1 at
      `{{typography.title-h1.letterSpacing}}`, body at
      `{{typography.paragraph-md.letterSpacing}}`.
- [ ] **Product imagery unobstructed?** No boxed panels over hardware renders.

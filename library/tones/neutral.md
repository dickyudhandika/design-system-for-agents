---
version: 1
name: neutral
description: >-
  Neutral starting point. System fonts, light gray surfaces, one blue action color,
  small radii. No personality yet — the default when a project has no design system.
  Grow it into a tone with `ds4a tone new <name>`.
colors:
  background: "#FFFFFF"            # Canvas.
  foreground: "#171717"            # Primary text.
  secondary: "#737373"             # Secondary gray. Mid-tone for subtle elements.
  muted: "#F5F5F5"                 # Subtle background. Sections, cards, hover states.
  border: "#E5E5E5"                # Separating content only. Never decorative.
  muted-foreground: "#737373"      # Secondary text, placeholders. 4.7:1 on background.
  primary: "#2563EB"               # Action color. CTAs and active states only.
  primary-foreground: "#FFFFFF"    # Text on primary. 5.2:1 on primary.
  destructive: "#DC2626"           # Errors and destructive actions only. 4.8:1 with white.
typography:
  # ── Titles (600) ──
  title-h1:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  title-h2:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.02em
  title-h3:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  title-h4:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: -0.01em
  title-h5:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  title-h6:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  # ── Labels (500) ──
  label-xl:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: -0.01em
  label-lg:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: -0.005em
  label-md:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0
  label-sm:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: 0
  label-xs:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0
  # ── Paragraphs (400) ──
  paragraph-xl:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.01em
  paragraph-lg:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: -0.005em
  paragraph-md:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  paragraph-sm:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: 0
  paragraph-xs:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: 0
rounded:
  xs: 2px     # Badges, small inline elements
  sm: 4px     # Inputs, small controls
  md: 6px     # Cards, buttons
  lg: 8px     # Modals, large surfaces
  full: 9999px  # Pills, avatars
spacing:
  xs: 4px     # Tight gaps, badge padding
  sm: 8px     # Button gap, field gap, radio gap
  md: 12px    # Input padding, fieldset gap
  lg: 16px    # Input padding, card gap, radio-card padding
  xl: 24px    # Card padding, form gap, minimum section gap
  2xl: 32px   # Section spacing
  3xl: 48px   # Page-level spacing
  4xl: 64px   # Hero spacing, major page divisions
components:
  button:
    radius: "{{rounded.md}}"
    padding-sm: "8px 12px"
    padding-md: "10px 16px"
    padding-lg: "12px 24px"
    font-size-sm: 14px
    font-size-md: 16px
    font-size-lg: 24px
    font-weight: 500
    gap: 8px
    variants: [primary, secondary, ghost]
  input:
    radius: "{{rounded.sm}}"
    padding-sm: "8px 12px"
    padding-md: "12px 16px"
    padding-lg: "16px 24px"
    font-size-sm: 14px
    font-size-md: 16px
    font-size-lg: 24px
    font-weight: 400
    border: "1px solid var(--color-border)"
    variants: [default, error]
  card:
    radius: "{{rounded.md}}"
    padding: 24px
    border: "1px solid var(--color-border)"
    variants: [default, elevated, flush]
  badge:
    radius: "{{rounded.xs}}"
    padding: "4px 8px"
    font-size: 12px
    font-weight: 500
    gap: 4px
    variants: [default, primary, destructive]
  field:
    label-font-size: 14px
    label-font-weight: 500
    description-font-size: 14px
    description-color: muted-foreground
    error-font-size: 14px
    error-color: destructive
    gap: 8px
  fieldset:
    legend-font-size: 16px
    legend-font-weight: 500
    gap: 12px
  form:
    gap: 24px
  select:
    radius: "{{rounded.sm}}"
    padding: "12px 16px"
    font-size: 16px
    font-weight: 400
    popup-radius: "{{rounded.sm}}"
    popup-padding: 4px
    popup-max-height: 280px
    icon-rotation: 180deg
  radio-group:
    gap: 8px
    radio-card-padding: 16px
    radio-card-gap: 16px
    radio-card-padding-mobile: 14px
    checked-background: "rgba(37,99,235,0.06)"
  modal:
    radius: "{{rounded.lg}}"
    padding: 24px
    width-sm: 320px
    width-md: 480px
    width-lg: 640px
    backdrop: "rgba(0, 0, 0, 0.4)"
    shadow: elevated
    header-gap: 8px
    footer-gap: 16px
    variants: [sm, md, lg]
  tabs:
    radius: "{{rounded.sm}}"
    trigger-padding: "8px 12px"
    trigger-font-size: 16px
    trigger-font-weight: 500
    indicator-height: 2px
    indicator-color: primary
    list-border: "1px solid var(--color-border)"
    variants: [underline]
  table:
    radius: "{{rounded.sm}}"
    row-padding: "12px 16px"
    header-font-size: 14px
    header-font-weight: 500
    header-color: muted-foreground
    cell-font-size: 14px
    cell-font-weight: 400
    row-border: "1px solid var(--color-border)"
    hover-background: muted
    selected-background: "rgba(37,99,235,0.06)"
    variants: [default]
  sidebar:
    radius: "{{rounded.sm}}"
    width: 240px
    item-padding: "12px"
    item-font-size: 14px
    item-font-weight: 500
    item-gap: 8px
    section-header-padding: "8px 12px"
    section-header-font-size: 12px
    active-indicator: "2px solid var(--color-primary)"
    container-border: "1px solid var(--color-border)"
    variants: [default]
---

<!--
Tone pack: neutral — the default when `ds4a init` finds no design system.
Deliberately unopinionated: system fonts, gray surfaces, one blue action color,
small radii, 4px grid. It is the structural baseline (Base UI-style anatomy comes
from library/core.md); personality is added later by forking it into a new tone.
-->

## Overview

Neutral baseline. System fonts, light gray surfaces, one blue action color, small radii.

**This tone has no personality on purpose.** It exists so a project without a design system starts from sound structure (anatomy, states, accessibility, spacing rhythm) instead of from someone else's taste.

- **One action color.** `{{colors.primary}}` is the only chromatic color besides `destructive`. It marks the main action and active states.
- **System fonts.** No web font to load. Titles are weight 600, labels 500, paragraphs 400.
- **Small radii.** `{{rounded.sm}}`–`{{rounded.lg}}` from the scale. Nothing pill-shaped except where `rounded.full` is chosen deliberately.
- **Light elevation.** Borders do most of the separating; shadows appear on overlays.

**Growing it:** change values in `.ds4a/project.md` for this project only, or run `/ds4a tone new <name>` to turn the current look into a reusable tone.

## Elevation & Depth

### Shadow tokens

| Token | Value | Use for |
|---|---|---|
| `subtle` | `0 1px 2px rgba(0,0,0,0.06)` | Cards, default elevation. |
| `elevated` | `0 4px 12px rgba(0,0,0,0.12)` | Popovers, dropdowns, modals. |

### Motion tokens

| Token | Value | Use for |
|---|---|---|
| `duration.fast` | 150ms | Button press, toggle, hover feedback |
| `duration.smooth` | 250ms | Page transitions, modals, dropdowns |
| `ease.out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Default. Feels natural, decelerating. |
| `ease.in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric transitions. |

## Shapes

### Radius approach

Small, consistent radii. `xs` for badges, `sm` for inputs, `md` for cards and buttons, `lg` for modals. Pick a step from the scale; don't invent in-between values.

---
version: 1
name: warm-sharp
description: >-
  Warm white, sharp edges, blue accent. Inter + Fauna One. Calm professional.
  Curated taste layer for AI coding agents. Living library that compounds with every project.
colors:
  # Semantic color tokens — use by intent, not by value
  background: "#FDFCF8"            # Warm white. Main canvas. Never pure white.
  foreground: "#1A1A1A"            # Primary text. Near-black, not pure black.
  secondary: "#A1A1A1"             # Secondary gray. Mid-tone for subtle elements.
  muted: "#F3F1EB"                 # Subtle background. Sections, cards, hover states.
  border: "#E5E2D9"                # Separating content only. Never decorative.
  muted-foreground: "#A1A1A1"      # Secondary text, placeholders. Must pass AA.
  primary: "#1A5EFF"               # Blue. CTAs and active states only. Not decoration.
  primary-foreground: "#FFFFFF"    # Text on primary. White for AA contrast on blue.
  destructive: "#C73E3E"           # Errors and destructive actions only. AA with white.
typography:
  # ── Titles (Fauna One, Medium 500) ──
  title-h1:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 56px
    fontWeight: 500
    lineHeight: 0.96
    letterSpacing: -0.01em
  title-h2:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 48px
    fontWeight: 500
    lineHeight: 1.17
    letterSpacing: -0.01em
  title-h3:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 40px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.01em
  title-h4:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 32px
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: -0.005em
  title-h5:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0
  title-h6:
    fontFamily: "\"Fauna One\", serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  # ── Labels (Inter, Medium 500) ──
  label-xl:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: -0.015em
  label-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: -0.015em
  label-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: -0.011em
  label-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: -0.006em
  label-xs:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0
  # ── Paragraphs (Inter, Regular 400) ──
  paragraph-xl:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: -0.015em
  paragraph-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: -0.015em
  paragraph-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.011em
  paragraph-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: -0.006em
  paragraph-xs:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: 0
rounded:
  xs: 0px     # Badges, small inline elements
  sm: 0px     # Inputs, badges
  md: 0px     # Cards, buttons
  lg: 0px     # Modals, large surfaces
  full: 0px   # Not used — sharp aesthetic only
spacing:
  xs: 4px     # Tight gaps, badge padding
  sm: 8px     # Button gap, field gap, radio gap
  md: 12px    # Input padding, fieldset gap, small button padding
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
    checked-background: "rgba(26,94,255,0.04)"
  modal:
    radius: "{{rounded.lg}}"
    padding: 24px
    width-sm: 320px
    width-md: 480px
    width-lg: 640px
    backdrop: "rgba(26, 26, 26, 0.4)"
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
    selected-background: "rgba(26,94,255,0.04)"
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
Tone pack: warm-sharp (the original ds4a baseline).
Tokens live in the frontmatter above. Prose below is tone-only: personality
and the rules that exist because of this tone. Structure, component contracts,
and universal guardrails come from library/core.md.
-->

## Overview

Warm white canvas. Sharp edges. Blue accent. Calm, professional, precise.

**Design personality:**
- **Warm white, not clinical.** Background is `{{colors.background}}` — a paper-like warmth that feels natural, not sterile. Never override with pure white.
- **Sharp edges, not rounded.** All radius values are `{{rounded.md}}`. Sharp corners convey precision and confidence. Rounded corners soften and casualize. This system chooses precision.
- **Blue accent, restrained.** `{{colors.primary}}` is the single accent color. It appears only on primary actions and active states. Never decorative. Never on large surfaces. One primary action per screen.
- **Two typefaces, clear roles.** Fauna One (serif) for titles — gives weight and character. Inter (sans-serif) for everything else — clean, neutral, readable. The pairing creates natural hierarchy without effort.
- **Subtle elevation.** Shadows are functional, not decorative. Max opacity 8%. A card lifts barely enough to separate from background. Popovers lift slightly more. If a shadow is visible, it's too heavy.

## Colors

### Tone rules

- **`background` is warm white, not pure white.** Never override with `#FFFFFF`. The warmth (`{{colors.background}}`) is intentional — it reduces eye strain and feels like paper.

## Typography

### Tone rules

- **One font family for everything except titles.** Inter (web) / SF Pro (iOS). Don't introduce other fonts.
- **Fauna One for titles only.** H1 through H6. Never for body, labels, or UI text. The serif character is the differentiator — use it where hierarchy matters.
- **Bold weight is sparing.** Default to `medium` (500) for emphasis. Use `bold` (700) only for critical emphasis — warnings, strong warnings. Regular (400) is the default for all body text.
- **Letter spacing is negative for large text, zero for small.** Large headings tighten (`-0.01em` to `-0.015em`); 12px text has `0` tracking.

## Elevation & Depth

### Shadow tokens

| Token | Value | Use for |
|---|---|---|
| `subtle` | `0 1px 2px rgba(0,0,0,0.04)` | Cards, default elevation. Barely visible. |
| `elevated` | `0 4px 8px rgba(0,0,0,0.08)` | Popovers, dropdowns, modals. Clearly elevated. |

**Max opacity: 8%.** `subtle` is 4%, `elevated` is 8%. If a shadow looks heavy, reduce opacity — don't remove it.

### Motion tokens

Motion tokens (not in DESIGN.md frontmatter schema — documented here):

| Token | Value | Use for |
|---|---|---|
| `duration.fast` | 150ms | Button press, toggle, hover feedback |
| `duration.smooth` | 300ms | Page transitions, modals, dropdowns |
| `ease.out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Default. Feels natural, decelerating. |
| `ease.in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric transitions. |

## Shapes

### Why 0px?

**Sharp edges convey precision and confidence.** Rounded corners soften and casualize. This system chooses precision.

The sharp aesthetic is deliberate, not accidental. It creates a clinical, professional feel — think architectural drawings, technical documents, precision instruments. Every corner is a decision: we chose sharp.

- **Don't mix radius values.** All elements are 0px. Don't introduce 4px or 8px "for variety." The consistency is the point.
- **`border-radius: 50%` is for radio indicators only.** Not for avatars, not for badges, not for buttons.
- **If a framework provides default rounded corners, override them.** Set everything to `0px` explicitly.

## Do's and Don'ts

### Tone: warm-sharp

- ✅ **Do** use Fauna One for titles (H1–H6) only.
- ✅ **Do** default to Medium (500) for emphasis. Use Bold (700) sparingly.
- ✅ **Do** use 0px for all elements. The sharp aesthetic is deliberate.
- ✅ **Do** keep shadow opacity at or below 8%.
- ❌ **Don't** override `background` with pure white (`#FFFFFF`).
- ❌ **Don't** use Fauna One for body text, labels, or UI elements.
- ❌ **Don't** use Bold (700) for general emphasis — use Medium (500).
- ❌ **Don't** mix radius values. Don't introduce 4px or 8px "for variety."
- ❌ **Don't** exceed 8% opacity on shadows.
- ❌ **Don't** add pill or boxed Tabs variants — underline is the convention; pills are decorative variety.

## Pre-flight Checklist

- [ ] **Radius values from scale?** All elements use 0px. No invented radius.
- [ ] **Shadows for elevation only?** Max 8% opacity.
- [ ] **Typography categories respected?** Titles in Fauna One. Labels and paragraphs in Inter. No mixing.

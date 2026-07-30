---
version: alpha
name: ds4a-baseline
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
    radius: 0px
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
    radius: 0px
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
    radius: 0px
    padding: 24px
    border: "1px solid var(--color-border)"
    variants: [default, elevated, flush]
  badge:
    radius: 0px
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
    radius: 0px
    padding: "12px 16px"
    font-size: 16px
    font-weight: 400
    popup-radius: 0px
    popup-padding: 4px
    popup-max-height: 280px
    icon-rotation: 180deg
  radio-group:
    gap: 8px
    radio-card-padding: 16px
    radio-card-gap: 16px
    radio-card-padding-mobile: 14px
---

## Overview

Warm white canvas. Sharp edges. Blue accent. Calm, professional, precise.

This system chooses **clarity over decoration**, **hierarchy over noise**, and **rhythm over randomness**. Every value exists for a reason. Every rule prevents a category of mistakes.

**Design personality:**
- **Warm white, not clinical.** Background is `#FDFCF8` — a paper-like warmth that feels natural, not sterile. Never override with pure white.
- **Sharp edges, not rounded.** All radius values are `0px`. Sharp corners convey precision and confidence. Rounded corners soften and casualize. This system chooses precision.
- **Blue accent, restrained.** `#1A5EFF` is the single accent color. It appears only on primary actions and active states. Never decorative. Never on large surfaces. One primary action per screen.
- **Two typefaces, clear roles.** Fauna One (serif) for titles — gives weight and character. Inter (sans-serif) for everything else — clean, neutral, readable. The pairing creates natural hierarchy without effort.
- **Subtle elevation.** Shadows are functional, not decorative. Max opacity 8%. A card lifts barely enough to separate from background. Popovers lift slightly more. If a shadow is visible, it's too heavy.

**Philosophy:** The system is opinionated so the output doesn't need to be. Follow the rules and the result is consistent, professional, and accessible. Break the rules and the output degrades visibly.

## Colors

### Token roles

| Token | Value | Role |
|---|---|---|
| `background` | `#FDFCF8` | Main canvas. Warm white. Never pure white. |
| `foreground` | `#1A1A1A` | Primary text. Near-black. |
| `secondary` | `#A1A1A1` | Secondary gray. Mid-tone for subtle elements. |
| `muted` | `#F3F1EB` | Subtle background. Sections, cards, hover states. |
| `border` | `#E5E2D9` | Separating content only. Never decorative. |
| `muted-foreground` | `#A1A1A1` | Secondary text, placeholders. Must pass AA. |
| `primary` | `#1A5EFF` | Blue. CTAs and active states only. |
| `primary-foreground` | `#FFFFFF` | Text on primary. White for AA contrast. |
| `destructive` | `#C73E3E` | Errors and destructive actions only. |

### Rules

- **`primary` is for CTAs and active states only.** Not for decoration. Not for large surfaces. Not for borders. If it's not the single most important action on the screen, it's not primary.
- **`destructive` is for errors and destructive actions only.** Delete, remove, error messages, validation errors. Never for emphasis. Never for general styling.
- **`background` is warm white, not pure white.** Never override with `#FFFFFF`. The warmth (`#FDFCF8`) is intentional — it reduces eye strain and feels like paper.
- **`border` is for separating content, not decoration.** If a border doesn't separate two distinct content areas, it doesn't exist. Don't add borders for visual interest.
- **`muted` is for subtle backgrounds.** Sections that need to feel slightly different from the canvas. Card hover states. Selected item backgrounds. Not for text.
- **`muted-foreground` is for secondary text and placeholders.** Must pass WCAG AA contrast (4.5:1). Current value `#A1A1A1` passes on `#FDFCF8` background.
- **Semantic naming over appearance.** Use `color.primary`, not `color.blue`. The name encodes intent. An AI agent reading `color.primary` knows this is the action color. Reading `color.blue` it has to guess.

## Typography

### Three categories, clear jobs

| Category | Font | Weight | Sizes | Job |
|---|---|---|---|---|
| **Title** | Fauna One, serif | Medium 500 | 56→20px (H1→H6) | Page titles, section headers, card titles. One H1 per page. |
| **Label** | Inter, sans-serif | Medium 500 | 24→12px (XL→XS) | Button text, field labels, badges, metadata. Concise, scannable. |
| **Paragraph** | Inter, sans-serif | Regular 400 | 24→12px (XL→XS) | Body text, descriptions, helper text. Readable, neutral. |

### Rules

- **One font family for everything except titles.** Inter (web) / SF Pro (iOS). Don't introduce other fonts.
- **Fauna One for titles only.** H1 through H6. Never for body, labels, or UI text. The serif character is the differentiator — use it where hierarchy matters.
- **`H1` appears once per page.** No exceptions. If you need a second large heading, use H2.
- **Labels are not content.** Label tokens are for button text, field labels, badges, metadata — short scannable text. Never use label tokens for paragraphs or body content.
- **Paragraphs are not labels.** Paragraph tokens are for body text, descriptions, and helper text. Never use paragraph tokens for button text or badges.
- **Bold weight is sparing.** Default to `medium` (500) for emphasis. Use `bold` (700) only for critical emphasis — warnings, strong warnings. Regular (400) is the default for all body text.
- **Letter spacing is negative for large text, zero for small.** Large headings tighten (`-0.01em` to `-0.015em`). Small text (12px) has `0` tracking. Don't override — the values are calibrated per size.
- **Line height tightens for titles, relaxes for paragraphs.** Titles: `0.96`–`1.4` (tight, controlled). Paragraphs: `1.33`–`1.5` (readable, breathing room). Don't mix.

### Size scale

| Token | Size | Line height | Tracking | Use for |
|---|---|---|---|---|
| `title-h1` | 56px | 0.96 | -0.01em | Page title. Once per page. |
| `title-h2` | 48px | 1.17 | -0.01em | Section title. |
| `title-h3` | 40px | 1.2 | -0.01em | Card title, subsection header. |
| `title-h4` | 32px | 1.25 | -0.005em | Subsection header. |
| `title-h5` | 24px | 1.33 | 0 | Small heading. |
| `title-h6` | 20px | 1.4 | 0 | Minor heading. |
| `label-xl` | 24px | 1.33 | -0.015em | Large labels, XL button text. |
| `label-lg` | 18px | 1.33 | -0.015em | Large labels. |
| `label-md` | 16px | 1.5 | -0.011em | Default labels, button text, field labels. |
| `label-sm` | 14px | 1.43 | -0.006em | Small labels, field labels. |
| `label-xs` | 12px | 1.33 | 0 | Metadata, badges. |
| `paragraph-xl` | 24px | 1.33 | -0.015em | Large body text. |
| `paragraph-lg` | 18px | 1.33 | -0.015em | Large paragraphs. |
| `paragraph-md` | 16px | 1.5 | -0.011em | Default body text. |
| `paragraph-sm` | 14px | 1.43 | -0.006em | Secondary body text, descriptions. |
| `paragraph-xs` | 12px | 1.33 | 0 | Fine print. |

## Layout

### Spacing system

4px base unit. Everything follows the scale. No invented values.

| Token | Value | Typical use |
|---|---|---|
| `xs` | 4px | Tight gaps, badge padding, icon gaps |
| `sm` | 8px | Button gap, field gap, radio gap, small button padding |
| `md` | 12px | Input padding, fieldset gap, small button padding |
| `lg` | 16px | Input padding, card gap, radio-card padding |
| `xl` | 24px | Card padding, form gap, **minimum section gap** |
| `2xl` | 32px | Section spacing |
| `3xl` | 48px | Page-level spacing |
| `4xl` | 64px | Hero spacing, major page divisions |

### Rules

- **4px base unit.** Every spacing value is a multiple of 4. Don't use 5px, 7px, 10px, 13px. Stick to the scale.
- **Minimum space between sections: 24px (`xl`).** Never less. If sections feel cramped, increase to `2xl` (32px) or `3xl` (48px).
- **Don't invent values.** Use the scale. If a value isn't in the scale, you don't need it. The scale covers 4px to 64px — that's enough for any layout.
- **Cards use `xl` (24px) padding by default.** Flush variant uses 0 — content manages its own spacing.
- **Forms use `xl` (24px) gap between fields.** Fields use `sm` (8px) gap between label, control, and messages.
- **Use gaps, not margins.** Flexbox/grid `gap` property. Avoid margin collapse issues. Consistent spacing flow.

### Grid

- Use CSS Grid or Flexbox. No custom grid framework needed.
- Content max-width: 1200px for dashboards, 720px for text-heavy content, full-width for landing pages.
- Sidebar: 240px fixed (dashboards). Content area fills remaining.
- Card grid: `repeat(auto-fill, minmax(320px, 1fr))` for responsive card layouts.

## Elevation & Depth

### Shadow tokens

| Token | Value | Use for |
|---|---|---|
| `subtle` | `0 1px 2px rgba(0,0,0,0.04)` | Cards, default elevation. Barely visible. |
| `elevated` | `0 4px 8px rgba(0,0,0,0.08)` | Popovers, dropdowns, modals. Clearly elevated. |

### Rules

- **Shadows are for elevation only. Never for decoration.** A shadow means "this element is above the content beneath it." If the element isn't elevated, it doesn't have a shadow.
- **Max opacity: 8%.** If a shadow looks heavy, reduce opacity — don't remove the shadow entirely (the elevation signal is still needed). `subtle` is 4%, `elevated` is 8%.
- **`subtle` is the default.** Cards, static elevated surfaces. The shadow should be barely perceptible — it separates the card from the background without drawing attention.
- **`elevated` is for interactive elevation.** Popovers, dropdowns, modals, tooltips. Elements that appear above the page content. The shadow is more visible but still restrained.
- **Don't combine shadows with borders for the same element.** A card has border OR shadow, not both. Border separates content; shadow indicates elevation. Choose the signal that matches the intent.

### Motion

Motion tokens (not in DESIGN.md frontmatter schema — documented here):

| Token | Value | Use for |
|---|---|---|
| `duration.fast` | 150ms | Button press, toggle, hover feedback |
| `duration.smooth` | 300ms | Page transitions, modals, dropdowns |
| `ease.out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Default. Feels natural, decelerating. |
| `ease.in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric transitions. |

- **`ease-out` is the default.** Use `ease-in-out` only for symmetric transitions (open/close, expand/collapse).
- **Fast (150ms) for feedback.** User interacts → element responds immediately. Button press, toggle, hover.
- **Smooth (300ms) for transitions.** Content appears or disappears. Modal open, dropdown, page transition.
- **Don't animate layout properties** (width, height, padding). Animate transform and opacity only. Layout animation causes reflow and jank.

## Shapes

### Radius scale

| Token | Value | Use for |
|---|---|---|
| `xs` | 0px | Badges, small inline elements |
| `sm` | 0px | Inputs, badges |
| `md` | 0px | Cards, buttons |
| `lg` | 0px | Modals, large surfaces |
| `full` | 0px | Not used — sharp aesthetic only |

### Why 0px?

**Sharp edges convey precision and confidence.** Rounded corners soften and casualize. This system chooses precision.

The sharp aesthetic is deliberate, not accidental. It creates a clinical, professional feel — think architectural drawings, technical documents, precision instruments. Every corner is a decision: we chose sharp.

- **Don't mix radius values.** All elements are 0px. Don't introduce 4px or 8px "for variety." The consistency is the point.
- **Don't use `border-radius: 50%` for anything except radio indicators.** Circular elements are reserved for radio buttons and selection indicators. Not for avatars, not for badges, not for buttons.
- **If a framework provides default rounded corners, override them.** Tailwind defaults to `rounded-md` (6px). Set everything to `0px` explicitly.

## Components

### Button

**3 variants: `primary`, `secondary`, `ghost`.**

| Variant | Background | Text | Use for |
|---|---|---|---|
| `primary` | `color.primary` (blue) | `color.primary-foreground` (white) | Main action. One per section. |
| `secondary` | `color.muted` | `color.foreground` | Secondary actions. Alternative to primary. |
| `ghost` | transparent | `color.foreground` | Tertiary actions. Border appears on hover. |

**3 sizes: `sm`, `md`, `lg`. Default `md`.**

| Size | Padding | Font size |
|---|---|---|
| `sm` | 8px 12px | 14px (label-sm) |
| `md` | 10px 16px | 16px (label-md) |
| `lg` | 12px 24px | 24px (label-xl) |

- Button text uses `label` typography tokens (Medium 500 weight).
- Gap between icon and text: `sm` (8px).
- `primary` = solid blue background. Used for main action, **one per section**.
- `secondary` = muted background with foreground text. Hover darkens to border color.
- `ghost` = transparent, border appears on hover. For low-priority actions.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`. All variants.
- Focus: `ds-focus-visible` class — `outline: 2px solid color.primary`, `outline-offset: 2px`.
- Transitions: `ds-transition` class — `150ms ease-out` on background-color, border-color, filter.

### Input

**3 sizes: `sm`, `md`, `lg`. Default `md`.**
**2 variants: `default`, `error`.**

| Size | Padding | Font size |
|---|---|---|
| `sm` | 8px 12px | 14px (paragraph-sm) |
| `md` | 12px 16px | 16px (paragraph-md) |
| `lg` | 16px 24px | 24px (paragraph-xl) |

- Input text uses `paragraph` typography tokens (Regular 400 weight).
- Border: `1px solid color.border`. Radius: 0px (sharp).
- Placeholder uses `color.muted-foreground` (`#A1A1A1`). WCAG AA pass.
- Error variant: border + focus ring use `color.destructive`.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`.
- Width: 100% of parent. Control width via parent container.
- Focus: `ds-focus-visible` — `outline: 2px solid color.primary`, `outline-offset: 2px`.

### Card

**3 variants: `default`, `elevated`, `flush`.**

| Variant | Shadow | Padding | Use for |
|---|---|---|---|
| `default` | `shadow.subtle` | 24px (xl) | Standard content card. |
| `elevated` | `shadow.elevated` | 24px (xl) | Popovers, floating content. |
| `flush` | `shadow.subtle` | 0 | Media cards, content manages own spacing. |

- Background: `color.background` (warm white).
- Border: `1px solid color.border`. Always present — separates card from background.
- Radius: 0px (sharp edges).
- **No hover state.** Cards are surfaces, not interactive. If you need interaction, wrap with a button or add a clickable child.

### Badge

**3 variants: `default`, `primary`, `destructive`.**

| Variant | Background | Text | Border | Use for |
|---|---|---|---|---|
| `default` | `color.muted` | `color.foreground` | `1px solid color.border` | Neutral labels, status. |
| `primary` | `color.primary` (blue) | `color.primary-foreground` (white) | none | Active/positive states. |
| `destructive` | `color.destructive` (red) | `color.primary-foreground` (white) | none | Errors/critical. |

- Font: `label-xs` (12px, Medium 500).
- Padding: `xs sm` (4px 8px). Gap: `xs` (4px).
- Radius: 0px (sharp).
- **Inline-flex. Never block-level.** Badges sit inline with text or labels.
- `white-space: nowrap`. Badge content never wraps.

### Field

Form field wrapper with label, control, description, and error messaging.

| Part | Element | Purpose |
|---|---|---|
| `Field.Root` | `<div>` | Groups all parts. Accepts `name`, `validate`, `validationMode`, `disabled`. |
| `Field.Label` | `<label>` | Accessible label. Auto-associated with control. Label-sm typography. |
| `Field.Control` | `<input>` | Text input. Same styling as Input component. |
| `Field.Description` | `<p>` | Helper text below input. Paragraph-sm, muted-foreground. |
| `Field.Error` | `<div>` | Error message. Paragraph-sm, destructive color. `aria-live` for screen readers. |

- Gap between parts: `sm` (8px).
- Label: `label-sm` (14px, Medium 500), `color.foreground`.
- Description: `paragraph-sm` (14px, Regular 400), `color.muted-foreground`.
- Error: `paragraph-sm` (14px, Regular 400), `color.destructive`.
- Invalid state: `data-invalid` attribute on root. Control border → `color.destructive`.
- Validation: `validate(value, formValues) → null | string`. `validationMode`: `onSubmit` (default), `onBlur`, `onChange`.

### Fieldset

Groups related form controls with a shared legend.

- `border: none`, `padding: 0`, `margin: 0`. Clean wrapper.
- Gap between controls: `md` (12px).
- Legend: `label-md` (16px, Medium 500), `color.foreground`.
- Disabled: `opacity: 0.5`.

### Form

Form wrapper with consolidated validation.

- Gap between fields: `xl` (24px).
- `onFormSubmit(values)` — receives all field values. `preventDefault()` called automatically.
- `validationMode`: `onSubmit` (default), `onBlur`, `onChange`.

### Select

Accessible dropdown with keyboard navigation.

| Part | Element | Purpose |
|---|---|---|
| `Select.Trigger` | `<button>` | Opens popup. Styled like Input. Paragraph-md typography. |
| `Select.Value` | `<span>` | Shows selected value or placeholder. |
| `Select.Icon` | chevron SVG | Rotates 180° when open. `duration.fast` transition. |
| `Select.Popup` | `<div>` | Popup container. `shadow.elevated`, 0px radius, max-height 280px. |
| `Select.Item` | `<div>` | Individual option. Highlighted → `color.muted` background. Selected → Medium weight + blue dot indicator. |

- Trigger: same styling as Input — `1px solid color.border`, 0px radius, `paragraph-md` typography.
- Popup padding: `xs` (4px). Item gap: 2px.
- Selected item indicator: 6px blue dot (`color.primary`).
- Disabled item: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`.

### RadioGroup

Single-select radio group. Two sub-components: `Radio` (inline) and `RadioCard` (card-style).

- Group gap: `sm` (8px). Vertical layout.
- **Radio (inline):** 16px circular indicator, 2px border. Checked → blue border + 8px blue dot. Hover → blue border. Label: `paragraph-md`.
- **RadioCard:** Full-width card. Padding `lg` (16px), gap `lg` (16px). Checked → blue border + tinted background (`rgba(26,94,255,0.04)`). Hover → blue border. Mobile: padding 14px, gap `md` (12px).
- Indicator: 18px (RadioCard) / 16px (Radio), 2px border, circular. Blue when checked or hovered.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`.
- Transitions: `duration.fast` `ease-out` on border-color, opacity.

## Do's and Don'ts

### Color

- ✅ **Do** use `primary` only for the single most important action on a screen.
- ✅ **Do** use `destructive` only for errors and destructive actions.
- ✅ **Do** use `muted-foreground` for placeholder text — it passes AA.
- ✅ **Do** use `border` only to separate distinct content areas.
- ❌ **Don't** override `background` with pure white (`#FFFFFF`).
- ❌ **Don't** use `primary` for decoration, borders, or large surface fills.
- ❌ **Don't** use `destructive` for emphasis or general styling.
- ❌ **Don't** use `border` color for placeholder text — use `muted-foreground`.

### Typography

- ✅ **Do** use Fauna One for titles (H1–H6) only.
- ✅ **Do** use label tokens for button text, field labels, and badges.
- ✅ **Do** use paragraph tokens for body text, descriptions, and helper text.
- ✅ **Do** default to Medium (500) for emphasis. Use Bold (700) sparingly.
- ❌ **Don't** use more than one H1 per page. No exceptions.
- ❌ **Don't** use label tokens for body content or paragraph tokens for labels.
- ❌ **Don't** use Fauna One for body text, labels, or UI elements.
- ❌ **Don't** use Bold (700) for general emphasis — use Medium (500).

### Spacing

- ✅ **Do** use the spacing scale for every spacing decision.
- ✅ **Do** maintain minimum 24px (`xl`) between sections.
- ✅ **Do** use Flexbox/Grid `gap` property over margins.
- ❌ **Don't** invent spacing values outside the 4px scale.
- ❌ **Don't** use values like 5px, 7px, 10px, 13px — they break the rhythm.

### Radius

- ✅ **Do** use 0px for all elements. The sharp aesthetic is deliberate.
- ❌ **Don't** mix radius values. Don't introduce 4px or 8px "for variety."
- ❌ **Don't** use `border-radius: 50%` except for radio indicators.

### Shadows

- ✅ **Do** use `shadow.subtle` for cards and default elevation.
- ✅ **Do** use `shadow.elevated` for popovers, dropdowns, and modals.
- ✅ **Do** reduce opacity if a shadow looks heavy — don't remove it entirely.
- ❌ **Don't** use shadows for decoration.
- ❌ **Don't** combine border + shadow on the same element for the same purpose.
- ❌ **Don't** exceed 8% opacity on shadows.

### Accessibility

- ✅ **Do** ensure all text passes WCAG AA (4.5:1 minimum).
- ✅ **Do** use `muted-foreground` for placeholder text — it's calibrated for AA.
- ✅ **Do** use `opacity: 0.5` + `cursor: not-allowed` + `pointer-events: none` for disabled states.
- ✅ **Do** provide visible focus rings (`ds-focus-visible` — `outline: 2px solid color.primary`).
- ✅ **Do** use semantic HTML (`<label>`, `<fieldset>`, `<legend>`, `aria-live` for errors).
- ❌ **Don't** change text color for disabled states — use opacity only.
- ❌ **Don't** eyeball contrast — use a contrast calculator.
- ❌ **Don't** remove focus outlines without providing an alternative.

### Components

- ✅ **Do** limit one `primary` button per section.
- ✅ **Do** use `secondary` for alternative actions, `ghost` for tertiary.
- ✅ **Do** keep cards non-interactive — wrap with button if click is needed.
- ✅ **Do** use `inline-flex` for badges — never block-level.
- ❌ **Don't** add hover states to cards — they're surfaces, not interactive.
- ❌ **Don't** use badge `primary` variant for anything except active/positive states.

## Pre-flight Checklist

Before generating any UI, verify:

- [ ] **One primary action per screen?** Only one element uses `color.primary` as background.
- [ ] **Spacing follows 4px grid?** No invented values. All spacing from `xs` to `4xl` scale.
- [ ] **Semantic tokens used, not raw values?** No `#1A5EFF` in markup — use `color.primary` or `var(--color-primary)`.
- [ ] **WCAG AA checked?** All text passes 4.5:1 contrast. Placeholder text uses `muted-foreground`.
- [ ] **H1 appears once?** Page has exactly one `title-h1`. Additional headings use H2+.
- [ ] **Radius values from scale?** All elements use 0px. No invented radius.
- [ ] **Shadows for elevation only?** No decorative shadows. Max 8% opacity.
- [ ] **Typography categories respected?** Titles in Fauna One. Labels and paragraphs in Inter. No mixing.
- [ ] **Disabled states use opacity?** No color changes for disabled — `opacity: 0.5` only.
- [ ] **Border for separation, not decoration?** Every border separates distinct content areas.
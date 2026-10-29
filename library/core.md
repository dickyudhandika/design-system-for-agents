---
schema: ds4a-core
version: 1
---

<!--
ds4a core — the tone-free layer.

Everything here is a fundamental: component anatomy, states, accessibility,
usage rules. It contains NO tone values (no hex, no px that a tone could
change). Tone values arrive through {{placeholders}} that `scripts/resolve.py`
fills from the merged tokens: core -> tone pack -> project overlay.

Placeholder syntax:
  {{colors.primary}}                 value from the merged token tree
  {{components.button.padding-md}}   nested path
  {{extra:colors}}                   rows for project-specific color tokens
Layout lines may carry <!--layout:Name--> markers; `resolve.py --type` keeps or
drops them using references/component-matrix.md. Markers are stripped on output.
-->

## Overview

**Principles:** clarity over decoration, hierarchy over noise, rhythm over randomness. Every value exists for a reason. Every rule prevents a category of mistakes.

**Philosophy:** The system is opinionated so the output doesn't need to be. Follow the rules and the result is consistent, professional, and accessible. Break the rules and the output degrades visibly.

## Colors

### Token roles

| Token | Value | Role |
|---|---|---|
| `background` | `{{colors.background}}` | Main canvas. |
| `foreground` | `{{colors.foreground}}` | Primary text. |
| `secondary` | `{{colors.secondary}}` | Secondary gray. Mid-tone for subtle elements. |
| `muted` | `{{colors.muted}}` | Subtle background. Sections, cards, hover states. |
| `border` | `{{colors.border}}` | Separating content only. Never decorative. |
| `muted-foreground` | `{{colors.muted-foreground}}` | Secondary text, placeholders. Must pass AA. |
| `primary` | `{{colors.primary}}` | The action color. CTAs and active states only. |
| `primary-foreground` | `{{colors.primary-foreground}}` | Text on primary. Must pass AA on `primary`. |
| `destructive` | `{{colors.destructive}}` | Errors and destructive actions only. |
{{extra:colors}}

### Rules

- **`primary` is for CTAs and active states only.** Not for decoration. Not for large surfaces. Not for borders. If it's not the single most important action on the screen, it's not primary.
- **`destructive` is for errors and destructive actions only.** Delete, remove, error messages, validation errors. Never for emphasis. Never for general styling.
- **`background` is the canvas.** Don't override it per component with a raw value.
- **`border` is for separating content, not decoration.** If a border doesn't separate two distinct content areas, it doesn't exist. Don't add borders for visual interest.
- **`muted` is for subtle backgrounds.** Sections that need to feel slightly different from the canvas. Card hover states. Selected item backgrounds. Not for text.
- **`muted-foreground` is for secondary text and placeholders.** Must pass WCAG AA contrast (4.5:1) against `background`. `ds4a resolve` checks this and warns on failure.
- **Semantic naming over appearance.** Use `color.primary`, not `color.blue`. The name encodes intent. An AI agent reading `color.primary` knows this is the action color. Reading `color.blue` it has to guess.

## Typography

### Three categories, clear jobs

| Category | Font | Weight | Sizes | Job |
|---|---|---|---|---|
| **Title** | `{{typography.title-h1.fontFamily}}` | {{typography.title-h1.fontWeight}} | {{typography.title-h1.fontSize}}→{{typography.title-h6.fontSize}} (H1→H6) | Page titles, section headers, card titles. One H1 per page. |
| **Label** | `{{typography.label-md.fontFamily}}` | {{typography.label-md.fontWeight}} | {{typography.label-xl.fontSize}}→{{typography.label-xs.fontSize}} (XL→XS) | Button text, field labels, badges, metadata. Concise, scannable. |
| **Paragraph** | `{{typography.paragraph-md.fontFamily}}` | {{typography.paragraph-md.fontWeight}} | {{typography.paragraph-xl.fontSize}}→{{typography.paragraph-xs.fontSize}} (XL→XS) | Body text, descriptions, helper text. Readable, neutral. |

### Rules

- **Each category uses the font family assigned to it above.** Don't introduce other fonts.
- **`H1` appears once per page.** No exceptions. If you need a second large heading, use H2.
- **Labels are not content.** Label tokens are for button text, field labels, badges, metadata — short scannable text. Never use label tokens for paragraphs or body content.
- **Paragraphs are not labels.** Paragraph tokens are for body text, descriptions, and helper text. Never use paragraph tokens for button text or badges.
- **Weights come from the tokens.** Don't introduce weights outside the scale.
- **Letter spacing is negative or zero, never positive.** Large headings tighten; small text (12px class) has no tracking. Don't override — the values are calibrated per size.
- **Line height tightens for titles, relaxes for paragraphs.** Don't mix.

### Size scale

| Token | Size | Line height | Tracking | Use for |
|---|---|---|---|---|
| `title-h1` | {{typography.title-h1.fontSize}} | {{typography.title-h1.lineHeight}} | {{typography.title-h1.letterSpacing}} | Page title. Once per page. |
| `title-h2` | {{typography.title-h2.fontSize}} | {{typography.title-h2.lineHeight}} | {{typography.title-h2.letterSpacing}} | Section title. |
| `title-h3` | {{typography.title-h3.fontSize}} | {{typography.title-h3.lineHeight}} | {{typography.title-h3.letterSpacing}} | Card title, subsection header. |
| `title-h4` | {{typography.title-h4.fontSize}} | {{typography.title-h4.lineHeight}} | {{typography.title-h4.letterSpacing}} | Subsection header. |
| `title-h5` | {{typography.title-h5.fontSize}} | {{typography.title-h5.lineHeight}} | {{typography.title-h5.letterSpacing}} | Small heading. |
| `title-h6` | {{typography.title-h6.fontSize}} | {{typography.title-h6.lineHeight}} | {{typography.title-h6.letterSpacing}} | Minor heading. |
| `label-xl` | {{typography.label-xl.fontSize}} | {{typography.label-xl.lineHeight}} | {{typography.label-xl.letterSpacing}} | Large labels, XL button text. |
| `label-lg` | {{typography.label-lg.fontSize}} | {{typography.label-lg.lineHeight}} | {{typography.label-lg.letterSpacing}} | Large labels. |
| `label-md` | {{typography.label-md.fontSize}} | {{typography.label-md.lineHeight}} | {{typography.label-md.letterSpacing}} | Default labels, button text, field labels. |
| `label-sm` | {{typography.label-sm.fontSize}} | {{typography.label-sm.lineHeight}} | {{typography.label-sm.letterSpacing}} | Small labels, field labels. |
| `label-xs` | {{typography.label-xs.fontSize}} | {{typography.label-xs.lineHeight}} | {{typography.label-xs.letterSpacing}} | Metadata, badges. |
| `paragraph-xl` | {{typography.paragraph-xl.fontSize}} | {{typography.paragraph-xl.lineHeight}} | {{typography.paragraph-xl.letterSpacing}} | Large body text. |
| `paragraph-lg` | {{typography.paragraph-lg.fontSize}} | {{typography.paragraph-lg.lineHeight}} | {{typography.paragraph-lg.letterSpacing}} | Large paragraphs. |
| `paragraph-md` | {{typography.paragraph-md.fontSize}} | {{typography.paragraph-md.lineHeight}} | {{typography.paragraph-md.letterSpacing}} | Default body text. |
| `paragraph-sm` | {{typography.paragraph-sm.fontSize}} | {{typography.paragraph-sm.lineHeight}} | {{typography.paragraph-sm.letterSpacing}} | Secondary body text, descriptions. |
| `paragraph-xs` | {{typography.paragraph-xs.fontSize}} | {{typography.paragraph-xs.lineHeight}} | {{typography.paragraph-xs.letterSpacing}} | Fine print. |

## Layout

### Spacing system

4px base unit. Everything follows the scale. No invented values.

| Token | Value | Typical use |
|---|---|---|
| `xs` | {{spacing.xs}} | Tight gaps, badge padding, icon gaps |
| `sm` | {{spacing.sm}} | Button gap, field gap, radio gap, small button padding |
| `md` | {{spacing.md}} | Input padding, fieldset gap, small button padding |
| `lg` | {{spacing.lg}} | Input padding, card gap, radio-card padding |
| `xl` | {{spacing.xl}} | Card padding, form gap, **minimum section gap** |
| `2xl` | {{spacing.2xl}} | Section spacing |
| `3xl` | {{spacing.3xl}} | Page-level spacing |
| `4xl` | {{spacing.4xl}} | Hero spacing, major page divisions |

### Rules

- **4px base unit.** Every spacing value is a multiple of 4. Don't use 5px, 7px, 10px, 13px. Stick to the scale.
- **Minimum space between sections: `xl` ({{spacing.xl}}).** Never less. If sections feel cramped, increase to `2xl` ({{spacing.2xl}}) or `3xl` ({{spacing.3xl}}).
- **Don't invent values.** Use the scale. If a value isn't in the scale, you don't need it. The scale covers `xs` to `4xl` — that's enough for any layout.
- **Cards use `xl` padding by default.** Flush variant uses 0 — content manages its own spacing.
- **Forms use `xl` gap between fields.** Fields use `sm` gap between label, control, and messages.
- **Use gaps, not margins.** Flexbox/grid `gap` property. Avoid margin collapse issues. Consistent spacing flow.

### Grid

- Use CSS Grid or Flexbox. No custom grid framework needed.
<!--layout:Content max-width: 1200px-->- Content max-width: 1200px for dashboards and other app screens.
<!--layout:Content max-width: 720px-->- Content max-width: 720px for text-heavy content.
<!--layout:Full-width-->- Full-width for landing pages.
<!--layout:Sidebar (240px fixed)-->- Sidebar: `{{components.sidebar.width}}` fixed (dashboards). Content area fills remaining.
<!--layout:Card grid-->- Card grid: `repeat(auto-fill, minmax(320px, 1fr))` for responsive card layouts.

## Elevation & Depth

### Rules

- **Shadows are for elevation only. Never for decoration.** A shadow means "this element is above the content beneath it." If the element isn't elevated, it doesn't have a shadow.
- **If a shadow looks heavy, reduce opacity — don't remove the shadow entirely** (the elevation signal is still needed).
- **`subtle` is the default.** Cards, static elevated surfaces. The shadow should be barely perceptible — it separates the card from the background without drawing attention.
- **`elevated` is for interactive elevation.** Popovers, dropdowns, modals, tooltips. Elements that appear above the page content. The shadow is more visible but still restrained.
- **Don't combine shadows with borders for the same element.** A card has border OR shadow, not both. Border separates content; shadow indicates elevation. Choose the signal that matches the intent.

### Motion rules

- **`ease.out` is the default.** Use `ease.in-out` only for symmetric transitions (open/close, expand/collapse).
- **`duration.fast` for feedback.** User interacts → element responds immediately. Button press, toggle, hover.
- **`duration.smooth` for transitions.** Content appears or disappears. Modal open, dropdown, page transition.
- **Don't animate layout properties** (width, height, padding). Animate transform and opacity only. Layout animation causes reflow and jank.

## Shapes

### Radius scale

| Token | Value | Use for |
|---|---|---|
| `xs` | {{rounded.xs}} | Badges, small inline elements |
| `sm` | {{rounded.sm}} | Inputs, small controls |
| `md` | {{rounded.md}} | Cards, buttons |
| `lg` | {{rounded.lg}} | Modals, large surfaces |
| `full` | {{rounded.full}} | Pills, avatars — only if the tone gives it a non-zero value |

### Rules

- **Radius comes from the scale.** Don't invent values. Don't mix scale steps on the same kind of element.
- **`border-radius: 50%` is reserved for radio indicators** unless `rounded.full` is non-zero in the tone.
- **If a framework provides default rounded corners, override them** with the scale values above. Tailwind defaults to `rounded-md` (6px) — map it to the scale explicitly.

## Components

### Button

**3 variants: `primary`, `secondary`, `ghost`.**

| Variant | Background | Text | Use for |
|---|---|---|---|
| `primary` | `color.primary` | `color.primary-foreground` | Main action. One per section. |
| `secondary` | `color.muted` | `color.foreground` | Secondary actions. Alternative to primary. |
| `ghost` | transparent | `color.foreground` | Tertiary actions. Border appears on hover. |

**3 sizes: `sm`, `md`, `lg`. Default `md`.**

| Size | Padding | Font size |
|---|---|---|
| `sm` | {{components.button.padding-sm}} | {{components.button.font-size-sm}} (label-sm) |
| `md` | {{components.button.padding-md}} | {{components.button.font-size-md}} (label-md) |
| `lg` | {{components.button.padding-lg}} | {{components.button.font-size-lg}} (label-xl) |

- Button text uses `label` typography tokens (weight {{components.button.font-weight}}).
- Radius: `{{components.button.radius}}`.
- Gap between icon and text: `sm` ({{components.button.gap}}).
- `primary` = solid `color.primary` background. Used for main action, **one per section**.
- `secondary` = muted background with foreground text. Hover darkens to border color.
- `ghost` = transparent, border appears on hover. For low-priority actions.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`. All variants.
- Focus: `ds-focus-visible` class — `outline: 2px solid color.primary`, `outline-offset: 2px`.
- Transitions: `ds-transition` class — `duration.fast` `ease.out` on background-color, border-color, filter.

### Input

**3 sizes: `sm`, `md`, `lg`. Default `md`.**
**2 variants: `default`, `error`.**

| Size | Padding | Font size |
|---|---|---|
| `sm` | {{components.input.padding-sm}} | {{components.input.font-size-sm}} (paragraph-sm) |
| `md` | {{components.input.padding-md}} | {{components.input.font-size-md}} (paragraph-md) |
| `lg` | {{components.input.padding-lg}} | {{components.input.font-size-lg}} (paragraph-xl) |

- Input text uses `paragraph` typography tokens (weight {{components.input.font-weight}}).
- Border: `{{components.input.border}}`. Radius: `{{components.input.radius}}`.
- Placeholder uses `color.muted-foreground` (`{{colors.muted-foreground}}`). Must pass WCAG AA.
- Error variant: border + focus ring use `color.destructive`.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`.
- Width: 100% of parent. Control width via parent container.
- Focus: `ds-focus-visible` — `outline: 2px solid color.primary`, `outline-offset: 2px`.

### Card

**3 variants: `default`, `elevated`, `flush`.**

| Variant | Shadow | Padding | Use for |
|---|---|---|---|
| `default` | `shadow.subtle` | {{components.card.padding}} (xl) | Standard content card. |
| `elevated` | `shadow.elevated` | {{components.card.padding}} (xl) | Popovers, floating content. |
| `flush` | `shadow.subtle` | 0 | Media cards, content manages own spacing. |

- Background: `color.background`.
- Border: `{{components.card.border}}`. Always present — separates card from background.
- Radius: `{{components.card.radius}}`.
- **No hover state.** Cards are surfaces, not interactive. If you need interaction, wrap with a button or add a clickable child.

### Badge

**3 variants: `default`, `primary`, `destructive`.**

| Variant | Background | Text | Border | Use for |
|---|---|---|---|---|
| `default` | `color.muted` | `color.foreground` | `1px solid color.border` | Neutral labels, status. |
| `primary` | `color.primary` | `color.primary-foreground` | none | Active/positive states. |
| `destructive` | `color.destructive` | `color.primary-foreground` | none | Errors/critical. |

- Font: `label-xs` ({{components.badge.font-size}}, weight {{components.badge.font-weight}}).
- Padding: `{{components.badge.padding}}`. Gap: `{{components.badge.gap}}`.
- Radius: `{{components.badge.radius}}`.
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

- Gap between parts: `sm` ({{components.field.gap}}).
- Label: `label-sm` ({{components.field.label-font-size}}, weight {{components.field.label-font-weight}}), `color.foreground`.
- Description: `paragraph-sm` ({{components.field.description-font-size}}), `color.{{components.field.description-color}}`.
- Error: `paragraph-sm` ({{components.field.error-font-size}}), `color.{{components.field.error-color}}`.
- Invalid state: `data-invalid` attribute on root. Control border → `color.destructive`.
- Validation: `validate(value, formValues) → null | string`. `validationMode`: `onSubmit` (default), `onBlur`, `onChange`.

### Fieldset

Groups related form controls with a shared legend.

- `border: none`, `padding: 0`, `margin: 0`. Clean wrapper.
- Gap between controls: `md` ({{components.fieldset.gap}}).
- Legend: `label-md` ({{components.fieldset.legend-font-size}}, weight {{components.fieldset.legend-font-weight}}), `color.foreground`.
- Disabled: `opacity: 0.5`.

### Form

Form wrapper with consolidated validation.

- Gap between fields: `xl` ({{components.form.gap}}).
- `onFormSubmit(values)` — receives all field values. `preventDefault()` called automatically.
- `validationMode`: `onSubmit` (default), `onBlur`, `onChange`.

### Select

Accessible dropdown with keyboard navigation.

| Part | Element | Purpose |
|---|---|---|
| `Select.Trigger` | `<button>` | Opens popup. Styled like Input. Paragraph-md typography. |
| `Select.Value` | `<span>` | Shows selected value or placeholder. |
| `Select.Icon` | chevron SVG | Rotates {{components.select.icon-rotation}} when open. `duration.fast` transition. |
| `Select.Popup` | `<div>` | Popup container. `shadow.elevated`, radius `{{components.select.popup-radius}}`, max-height {{components.select.popup-max-height}}. |
| `Select.Item` | `<div>` | Individual option. Highlighted → `color.muted` background. Selected → Medium weight + `color.primary` dot indicator. |

- Trigger: same styling as Input — `{{components.input.border}}`, radius `{{components.select.radius}}`, `paragraph-md` typography.
- Popup padding: `xs` ({{components.select.popup-padding}}). Item gap: 2px.
- Selected item indicator: 6px dot (`color.primary`).
- Disabled item: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`.

### RadioGroup

Single-select radio group. Two sub-components: `Radio` (inline) and `RadioCard` (card-style).

- Group gap: `sm` ({{components.radio-group.gap}}). Vertical layout.
- **Radio (inline):** 16px circular indicator, 2px border. Checked → `color.primary` border + 8px dot. Hover → `color.primary` border. Label: `paragraph-md`.
- **RadioCard:** Full-width card. Padding `lg` ({{components.radio-group.radio-card-padding}}), gap `lg` ({{components.radio-group.radio-card-gap}}). Checked → `color.primary` border + tinted background (`{{components.radio-group.checked-background}}`). Hover → `color.primary` border. Mobile: padding {{components.radio-group.radio-card-padding-mobile}}, gap `md` ({{spacing.md}}).
- Indicator: 18px (RadioCard) / 16px (Radio), 2px border, circular. `color.primary` when checked or hovered.
- Disabled: `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none`.
- Transitions: `duration.fast` `ease.out` on border-color, opacity.

### Modal

**3 sizes: `sm`, `md`, `lg`. Default `md`.**

| Size | Width | Use for |
|---|---|---|
| `sm` | {{components.modal.width-sm}} | Confirmations, short alerts |
| `md` | {{components.modal.width-md}} | Forms, standard dialogs |
| `lg` | {{components.modal.width-lg}} | Settings panels, multi-step content |

| Part | Element | Purpose |
|---|---|---|
| `Modal.Backdrop` | `<div>` | Overlay. `{{components.modal.backdrop}}`. Click closes. |
| `Modal.Container` | `<div role="dialog">` | Content surface. Centered. |
| `Modal.Header` | `<div>` | Title (`title-h6`) + close button. Gap `sm` ({{components.modal.header-gap}}). |
| `Modal.Body` | `<div>` | Content. Padding: 0 — container padding covers it. |
| `Modal.Footer` | `<div>` | Actions. Gap `lg` ({{components.modal.footer-gap}}). Right-aligned. |

- Container: `color.background`, `shadow.{{components.modal.shadow}}`, **no border** (elevation IS the separation — border + shadow on one element is forbidden by the elevation rule).
- Radius: `{{components.modal.radius}}`.
- Container padding: `xl` ({{components.modal.padding}}).
- Padding between header, body, footer: `lg` ({{spacing.lg}}) each.
- **Backdrop blocks interaction with the page.** No scrolling underneath while open (`overflow: hidden` on body).
- Backdrop fade: `duration.smooth` `ease.out`. Container entrance: `duration.smooth`, transform + opacity only.
- **Focus trap.** Focus enters the modal on open, returns to trigger on close. Esc closes. Close button is a `ghost` Button with icon, top-right.
- **One modal at a time.** Never stack modals. If a modal needs to confirm a destructive action, that confirmation is a second modal replacing the first — not an overlay on an overlay.
- Title uses `title-h6` ({{typography.title-h6.fontSize}}). One title per modal.
- Footer buttons: max 2. Primary action rightmost. Destructive confirmations use `destructive` variant Button — never a `primary` button for a delete.

### Tabs

**1 variant: `underline`.**

| Part | Element | Purpose |
|---|---|---|
| `Tabs.List` | `<div role="tablist">` | Row of triggers. Bottom border `{{components.tabs.list-border}}`. |
| `Tabs.Trigger` | `<button role="tab">` | Tab label. Padding `{{components.tabs.trigger-padding}}`. `label-md` typography. |
| `Tabs.Indicator` | `<div>` | {{components.tabs.indicator-height}} bar under the active tab. `color.{{components.tabs.indicator-color}}`. |
| `Tabs.Content` | `<div role="tabpanel">` | Active panel. Padding `lg` ({{spacing.lg}}) top. |

- Trigger: `label-md` ({{components.tabs.trigger-font-size}}, weight {{components.tabs.trigger-font-weight}}), `color.foreground`. Inactive trigger: `color.muted-foreground`.
- Active trigger: `color.foreground` + {{components.tabs.indicator-height}} `color.{{components.tabs.indicator-color}}` underline indicator.
- Radius: `{{components.tabs.radius}}`.
- Hover (inactive): `color.foreground` text. No background change.
- Disabled trigger: `opacity: 0.5`, `cursor: not-allowed`.
- Indicator slides between tabs: `duration.smooth` `ease.out`. Animate `transform` only — never width/position properties.
- **Keyboard navigation.** Arrow keys move between triggers, Home/End jump to first/last. Each trigger is tabbable.
- Full-width variant: triggers share width equally (`flex: 1`). Default is content-width.

### Table

**1 variant: `default`.**

| Part | Element | Purpose |
|---|---|---|
| `Table.Root` | `<table>` | Container. Full-width of parent. |
| `Table.Header` | `<thead>` | Header row. Bottom border `{{components.table.row-border}}`. |
| `Table.Row` | `<tr>` | Data row. Bottom border `{{components.table.row-border}}`. |
| `Table.Cell` | `<td>` | Cell. Paragraph-sm typography. |
| `Table.HeaderCell` | `<th>` | Header cell. Label-sm typography. |

- Row padding: `{{components.table.row-padding}}`. One density only.
- Header cells: `label-sm` ({{components.table.header-font-size}}, weight {{components.table.header-font-weight}}), `color.{{components.table.header-color}}`. No background — the border separates.
- Body cells: `paragraph-sm` ({{components.table.cell-font-size}}, weight {{components.table.cell-font-weight}}), `color.foreground`.
- **Row hover: background `color.{{components.table.hover-background}}`.** Hover signals interactivity only — if rows are not clickable, no hover.
- Selected row: `{{components.table.selected-background}}` (primary tint, same as RadioCard checked).
- Row selection indicator: 16px checkbox placeholder, leftmost column. Selection is visual — checkable rows use the grown-checkbox contract if present, else a plain checkbox input.
- **Sort state in header cell:** sort icon (chevron) + `label-sm` weight on the active sort column. Only one sort column at a time.
- Numeric columns right-aligned. Text columns left-aligned. Never center data.
- **Empty state:** single row, `paragraph-sm` `muted-foreground`, centered, "No results" + optional action link. Never render a bare empty `<tbody>`.
- **Loading state:** first 3-5 rows as skeleton bars (`color.muted` blocks, `duration.fast` pulse). Never a spinner overlay on the table.
- Radius: `{{components.table.radius}}`. No zebra striping — borders separate rows.
- Max-width: parent container governs. Horizontal scroll (`overflow-x: auto`) if columns exceed width — never shrink cells below their padding.

### Sidebar

**1 variant: `default`.**

| Part | Element | Purpose |
|---|---|---|
| `Sidebar.Container` | `<nav>` | Fixed {{components.sidebar.width}} column. Border-right `{{components.sidebar.container-border}}`. |
| `Sidebar.Header` | `<div>` | Logo/brand block. Padding `lg` ({{spacing.lg}}). |
| `Sidebar.Section` | `<div>` | Group of items under a section header. |
| `Sidebar.SectionHeader` | `<div>` | `label-xs` ({{components.sidebar.section-header-font-size}}, Medium), `muted-foreground`, uppercase. |
| `Sidebar.Item` | `<a>` | Nav item. Padding `{{components.sidebar.item-padding}}`. Gap `sm` ({{components.sidebar.item-gap}}) between icon and label. |
| `Sidebar.Footer` | `<div>` | Bottom block. User menu, collapse trigger. |

- Width: {{components.sidebar.width}} fixed. Content area fills remaining width (grid `{{components.sidebar.width}} 1fr`).
- Item: `label-sm` ({{components.sidebar.item-font-size}}, weight {{components.sidebar.item-font-weight}}), `color.foreground`. Icon 16px.
- Hover: background `color.muted`. Text stays `color.foreground`.
- Active: background `color.muted` + `{{components.sidebar.active-indicator}}` left-edge indicator. Text `color.foreground`.
- Item radius: `{{components.sidebar.radius}}`. Indicator is an inset border — not a pill, not a background fill.
- Section header padding: `{{components.sidebar.section-header-padding}}`. Gap between sections: `lg` ({{spacing.lg}}).
- **Section headers are not links.** They label groups only.
- Container background: `color.background` — same as canvas. The border separates, not a tint.
- Disabled item: `opacity: 0.5`, `cursor: not-allowed`.
- Mobile (< 768px): sidebar collapses behind a hamburger trigger into a full-height Sheet-like overlay (uses Modal elevation + backdrop rules). Never render a squished {{components.sidebar.width}} column on mobile.
- Collapse trigger (desktop, optional): icon-only button, `ghost` variant. Collapsed state = `4xl` ({{spacing.4xl}}), icons only, no labels. Transition: `duration.smooth` on width.

## Do's and Don'ts

### Color

- ✅ **Do** use `primary` only for the single most important action on a screen.
- ✅ **Do** use `destructive` only for errors and destructive actions.
- ✅ **Do** use `muted-foreground` for placeholder text — it must pass AA.
- ✅ **Do** use `border` only to separate distinct content areas.
- ❌ **Don't** override `background` with a raw value.
- ❌ **Don't** use `primary` for decoration, borders, or large surface fills.
- ❌ **Don't** use `destructive` for emphasis or general styling.
- ❌ **Don't** use `border` color for placeholder text — use `muted-foreground`.

### Typography

- ✅ **Do** use label tokens for button text, field labels, and badges.
- ✅ **Do** use paragraph tokens for body text, descriptions, and helper text.
- ❌ **Don't** use more than one H1 per page. No exceptions.
- ❌ **Don't** use label tokens for body content or paragraph tokens for labels.

### Spacing

- ✅ **Do** use the spacing scale for every spacing decision.
- ✅ **Do** maintain minimum `xl` ({{spacing.xl}}) between sections.
- ✅ **Do** use Flexbox/Grid `gap` property over margins.
- ❌ **Don't** invent spacing values outside the 4px scale.
- ❌ **Don't** use values like 5px, 7px, 10px, 13px — they break the rhythm.

### Radius

- ✅ **Do** take every radius from the `rounded` scale.
- ❌ **Don't** invent radius values or mix scale steps on the same kind of element.
- ❌ **Don't** use `border-radius: 50%` except for radio indicators (unless `rounded.full` is non-zero).

### Shadows

- ✅ **Do** use `shadow.subtle` for cards and default elevation.
- ✅ **Do** use `shadow.elevated` for popovers, dropdowns, and modals.
- ✅ **Do** reduce opacity if a shadow looks heavy — don't remove it entirely.
- ❌ **Don't** use shadows for decoration.
- ❌ **Don't** combine border + shadow on the same element for the same purpose.

### Accessibility

- ✅ **Do** ensure all text passes WCAG AA (4.5:1 minimum).
- ✅ **Do** use `muted-foreground` for placeholder text — it's the AA-checked secondary text color.
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
- [ ] **Semantic tokens used, not raw values?** No `{{colors.primary}}` in markup — use `color.primary` or `var(--color-primary)`.
- [ ] **WCAG AA checked?** All text passes 4.5:1 contrast. Placeholder text uses `muted-foreground`.
- [ ] **H1 appears once?** Page has exactly one `title-h1`. Additional headings use H2+.
- [ ] **Radius values from scale?** No invented radius.
- [ ] **Shadows for elevation only?** No decorative shadows.
- [ ] **Typography categories respected?** Titles, labels and paragraphs each use their own assigned font. No mixing.
- [ ] **Disabled states use opacity?** No color changes for disabled — `opacity: 0.5` only.
- [ ] **Border for separation, not decoration?** Every border separates distinct content areas.

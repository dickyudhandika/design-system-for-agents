# design-system-for-agents (ds4a)

> A reusable design library for AI coding agents. One set of fundamentals, many tones. Detects the design system a project already has, or starts from a neutral baseline and grows.

## What it is

A skill (usable by any agent that reads project files) that makes AI-generated UI visibly better and gets smarter with every project.

```
library/core.md  +  library/tones/<tone>.md  +  .ds4a/project.md   →   DESIGN.md
 fundamentals         look: tokens + personality   this project's deltas   what the agent reads
```

- **Core** — component contracts (anatomy, states, accessibility) and universal guardrails. Tone-free: no hex, no pixel values a tone could change.
- **Tones** — token values plus the rules that exist because of a look. `neutral` (default, no personality) and `warm-sharp` (the original ds4a look) ship today. Add more with `/ds4a tone new <name>`.
- **Project overlay** — what's detected from the project (colors, type, radius…) plus per-project overrides. Only the differences.

## Commands

Invoke as `/ds4a <subcommand>`.

| Command | What happens |
|---|---|
| `/ds4a init [type]` | Detect existing design system → overlay → `DESIGN.md` → preview |
| `/ds4a detect` | Dry run: what would be imported. Writes nothing |
| `/ds4a tone` / `tone <name>` / `tone new <name>` | List, switch, or fork a tone |
| `/ds4a resolve` | Regenerate `DESIGN.md` from the layers |
| `/ds4a preview` | Build and open the design-system page `.ds4a/preview.html` |
| `/ds4a review` | Three-pass review of generated code, approve/reject each suggestion |
| `/ds4a merge` | Merge approved rules to the project, a tone, or core |
| `/ds4a status` | Active tone, type, versions, pending review |

**The loop:**
```
new project → /ds4a init → build with AI → /ds4a review → approve → /ds4a merge → library grows
```

## Preview

`/ds4a preview` (or `python3 scripts/build-preview.py --project .`) writes one self-contained page, `.ds4a/preview.html`, generated from the resolved tokens. It opens offline; only Google Fonts load when online.

- **Foundations:** principles from the tone's Overview, color with WCAG contrast badges, type specimens and the full scale, spacing, radius, shadows and motion.
- **Components:** all 13 core contracts with live states (hover, focus, error, disabled, open, selected). Filtered by project type, with "Show all".
- **Tone switcher:** every tone in `library/tones/` is built into the page. Compare "this project" (tone + overlay) with the raw tones; components re-shape, not just recolor.
- **Navigation:** grouped sidebar, breadcrumb, search (`/`), and a gliding nav pill on desktop and mobile.
- **Motion from tokens:** every transition uses the tone's `duration.*` and `ease.*`; `prefers-reduced-motion` is respected.

Rebuild after changing the tone or `.ds4a/project.md`; the page does not watch files. Nothing is written outside `.ds4a/`.

## The four cases

1. **Reuse at scale.** The library lives in this repo (`library/`). Every project resolves from the same copy; merges write back to it, so project 10 starts from everything projects 1–9 taught it.
2. **Several tones, same fundamentals.** Switch with `/ds4a tone <name>`. Change one radius step and every component follows (`rounded.md` → buttons, cards…). The contracts never change.
3. **Project already has a system.** Detection reads AGENTS.md, `tokens.*`, shadcn `globals.css` (oklch → hex), Tailwind v4 `@theme`, `design-tokens.ts`, `tailwind.config`. Found tokens go in the overlay and win; gaps fall back to `neutral`. Nothing you own is overwritten.
4. **Project has nothing.** `neutral` tone: system fonts, grays, one action color, small radii, 4px grid, on top of the 13 core contracts (anatomy modeled on Base UI's unstyled parts). Grow it per project in the overlay, or fork it into a tone.

## Core components

13 core contracts — Button, Input, Field/Form/Fieldset, Select, RadioGroup, Card, Badge, Modal, Tabs, Table, Sidebar — benchmarked against UXPin's essential-components list, the shadcn/ui registry and Base UI. Contracts added by reviews carry `(grown)`; a grown contract used by 3+ projects (`library/usage.md`) is offered for promotion to core. See [core-components.md](references/core-components.md).

## Install

```bash
cd ~/.agents/skills        # or your agent's skills directory
git clone https://github.com/dickyudhandika/design-system-for-agents.git ds4a
```

Requires `python3` (standard library only) for `scripts/resolve.py` and `scripts/build-preview.py`.

Without a skill runner: `python3 scripts/resolve.py --tone neutral --stdout > DESIGN.md` and give your agent the file.

## What's inside

| Path | What |
|---|---|
| `SKILL.md` | Command router and workflow |
| `library/core.md` | Tone-free contracts and guardrails |
| `library/tones/` | `neutral.md`, `warm-sharp.md` |
| `library/usage.md` | Which projects used which grown contracts |
| `scripts/resolve.py` | Layers → `DESIGN.md`, with contrast and matrix-parity checks |
| `scripts/build-preview.py` | Tokens → `.ds4a/preview.html` (see [Preview](#preview), [preview.md](references/preview.md)) |
| `scripts/oklch-to-hex.py` | shadcn oklch → hex |
| `references/` | detection, shadcn mapping, review prompt, matrix, core benchmark, pitfalls |
| `templates/project-overlay.md` | Starting overlay |
| `templates/*.tsx/.astro`, `scripts/build-preview-html.ts` | In-framework `/design-system` references |

## Which AI agents work

Anything that reads project files: Claude Code, Codex, Cursor, Copilot, Hermes, v0, Lovable.

## FAQ

**Do I need to know design?** No. Pick or import a tone, approve suggestions with yes/no.

**Is it framework-specific?** No. `DESIGN.md` is framework-agnostic.

**Will it overwrite my theme or my DESIGN.md?** No. Only `DESIGN.md` (if it's ds4a-generated) and `.ds4a/` are written; `resolve.py` refuses to overwrite a DESIGN.md it didn't generate.

**Why is the preview plain HTML?** It has to open anywhere with no build step and no dependencies, and it shows the tokens in a real browser. For live framework components, use the in-framework `/design-system` references in `templates/`.

**What does the contrast check do?** `resolve.py` and `build-preview.py` warn when `foreground`, `muted-foreground`, or button text fail WCAG AA against their backgrounds. `warm-sharp`'s `muted-foreground` (`#A1A1A1` on `#FDFCF8`) currently fails at 2.5:1 — it's kept as-is so the original look is preserved, but the warning is real.

## License

MIT

## Roadmap

- [x] Multiple base libraries (tones)
- [ ] More tones (soft/friendly, dark/technical)
- [ ] Dark-mode tokens per tone
- [ ] Vision check — screenshots + vision AI for issues code can't catch
- [ ] Team libraries — shared evolution across developers

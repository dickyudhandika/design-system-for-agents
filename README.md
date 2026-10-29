# design-system-for-agents (ds4a)

> A reusable design library for AI coding agents. One set of fundamentals, many looks. ds4a finds the design system your project already has (or starts from a neutral baseline), writes it into one file your agent reads, and grows every time you use it.

## What is ds4a

ds4a is a **skill** — a folder of instructions, token files, and two small Python scripts that any AI coding agent can load from your project. Claude Code, Codex, Cursor, Copilot, v0, Lovable: anything that reads project files.

It does three things:

1. **Detects.** It looks for a design system you already have — `AGENTS.md`, `tokens.json`, shadcn's `globals.css`, Tailwind v4 `@theme`, `tailwind.config`, `design-tokens.ts` — and imports what's there. If there isn't one, it starts from a neutral baseline.
2. **Resolves.** The core fundamentals, one *tone* (the look), and your project's own overrides collapse into a single file: `DESIGN.md`. That file is what your agent reads when it builds.
3. **Grows.** After you build, `/ds4a review` finds where your agent drifted from the rules and proposes fixes. You approve them; `/ds4a merge` writes them back — to the project, to the tone, or to the shared library. Project 10 starts with everything projects 1–9 taught it.

Short version: **it makes AI-generated UI consistent instead of random, and it remembers what you taught it.**

## Why it exists

Three problems, one cause.

**Agents have no memory of your design.** Every session starts cold. The agent sees your files, not your decisions. Unless the rules are written somewhere the agent reads, it re-invents the button, the card, and the gray scale — slightly differently every time. The result looks like three products wearing one logo.

**Most design docs record the wrong thing.** A style guide is usually a color table and a font list. That's the *look*. It says nothing about the *rules*: which color is allowed for a CTA, when a border may exist, what a button looks like while disabled, what happens when a field fails validation. An agent can copy `#3B82F6` but it can't copy a principle — so the output drifts anyway.

**Good decisions die in the chat.** A rule you explained three times ("no shadows on cards, use a border") lives in one conversation and nowhere else. It never reaches the next agent, the next repo, or the next teammate.

ds4a makes the rules durable and shared:

- **Fundamentals live in one versioned place.** Component anatomy, states, accessibility, guardrails — written once, used by every project, the same way every time.
- **The look is swappable.** A tone holds color, type, radius, density, and the decisions that only make sense with that look. Change the tone and every component follows. The contracts don't change.
- **Your project always wins.** Detected tokens and your explicit overrides beat the library. ds4a never overwrites a file you own.
- **The library learns.** Rules that keep showing up get promoted into core and reach every project that follows.

## How it works

### Three layers, resolved into one file

```
library/core.md  +  library/tones/<tone>.md  +  .ds4a/project.md   →   DESIGN.md
 fundamentals         look (tokens + personality)   this project's deltas   what the agent reads
```

- **Core** (`library/core.md`) — component contracts (anatomy, states, accessibility) and universal guardrails. Tone-free on purpose: no hex, no pixel value a tone could change.
- **Tone** (`library/tones/<tone>.md`) — token values plus the rules that exist *because* of a look. Three ship today: `neutral` (the default, no personality), `warm-sharp` (the original ds4a look), and `apple-gallery` (a white product-page gallery). Make your own with `/ds4a tone new <name>`.
- **Project overlay** (`.ds4a/project.md`) — only what was detected from your project, plus anything you override. Just the differences.

Resolution is deterministic and self-checking: `scripts/resolve.py` merges the layers, flags token values that fail WCAG contrast, and reports components that don't match the matrix for your project type.

### The loop

```
new project → /ds4a init → build with AI → /ds4a review → approve → /ds4a merge → library grows
```

`/ds4a init` detects (or invents) a system, writes the overlay, resolves `DESIGN.md`, and opens the preview. You build. Then `/ds4a review` reads your code against the rules in three passes — violations, repeated-but-uncodified patterns, and gaps where the agent had to guess. You approve the good ones, and `/ds4a merge` files each one to the right layer.

Nothing happens automatically. Review and merge only run when you ask.

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

## Preview

`/ds4a preview` (or `python3 scripts/build-preview.py --project .`) writes one self-contained page, `.ds4a/preview.html`, generated from the resolved tokens. It opens offline; only Google Fonts load when online.

- **Foundations:** principles from the tone's Overview, color with WCAG contrast badges, type specimens and the full scale, spacing, radius, shadows, motion.
- **Components:** all 13 core contracts with live states (hover, focus, error, disabled, open, selected). Filtered by project type, with "Show all".
- **Tone switcher:** every tone in `library/tones/` is built into the page. Compare "this project" (tone + overlay) against the raw tones; components re-shape, not just recolor.
- **Navigation:** grouped sidebar, breadcrumb, search (`/`), and a gliding nav pill on desktop and mobile.
- **Motion from tokens:** every transition uses the tone's `duration.*` and `ease.*`; `prefers-reduced-motion` is respected.

Rebuild after changing the tone or `.ds4a/project.md` — the page does not watch files. Nothing is written outside `.ds4a/`.

## Four situations you'll hit

1. **You use it at scale.** The library lives in this repo (`library/`). Every project resolves from the same copy, and merges write back to it — so project 10 starts from everything projects 1–9 taught it.
2. **You want several looks, one set of fundamentals.** Switch with `/ds4a tone <name>`. Change one radius step and every component follows (`rounded.md` → buttons, cards…). The contracts never change.
3. **Your project already has a system.** Detection reads AGENTS.md, `tokens.*`, shadcn `globals.css` (oklch → hex), Tailwind v4 `@theme`, `design-tokens.ts`, `tailwind.config`. Found tokens go in the overlay and win; gaps fall back to `neutral`. Nothing you own is overwritten.
4. **Your project has nothing.** You get the `neutral` tone: system fonts, grays, one action color, small radii, a 4px grid, sitting on top of the 13 core contracts (anatomy modeled on Base UI's unstyled parts). Grow it per project in the overlay, or fork it into a tone.

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
| `library/tones/` | `neutral.md`, `warm-sharp.md`, `apple-gallery.md` |
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

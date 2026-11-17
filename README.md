# design-system-for-agents (ds4a)

> A reusable design library for AI coding agents. One set of fundamentals, many looks. ds4a finds the design system your project already has (or starts from a neutral baseline), writes it into one file your agent reads, and grows every time you use it.

## What is ds4a

ds4a is a **skill** — a folder of instructions, token files, and small Python scripts that any AI coding agent can load from your project. Claude Code, Codex, Cursor, Copilot, v0, Lovable: anything that reads project files.

It does five things:

1. **Detects.** It looks for a design system you already have — `AGENTS.md`, `tokens.json`, shadcn's `globals.css`, Tailwind v4 `@theme`, `tailwind.config`, `design-tokens.ts` — and imports what's there. If there isn't one, it starts from a neutral baseline.
2. **Resolves.** The core fundamentals, one *tone* (the look), and your project's own overrides collapse into a single file: `DESIGN.md`. That file is what your agent reads when it builds.
3. **Shows.** `preview.html` renders that system — foundations, your project's actual components as *specimens*, the core contracts, and every contract's status — as one self-contained page.
4. **Applies.** `apply` writes the resolved tokens into exactly one generated CSS file (or one Tailwind `@theme` block) and prints the import line. `--check` reports drift and hardcoded values that could become tokens.
5. **Grows.** After you build, `/ds4a diff` finds where your agent drifted from the rules and proposes fixes. You approve them; diff writes them back — to the project, to the tone, or to the shared library. Project 10 starts with everything projects 1–9 taught it.

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
new project → /ds4a init → build with AI → /ds4a diff → approve → library grows
                                                    ↘ specimens → preview
                                                    ↘ /ds4a apply → tokens in code
```

`/ds4a init` detects (or invents) a system, writes the overlay, resolves `DESIGN.md`, and opens the preview. You build. Then `/ds4a diff` reads your code against the rules in four passes — violations, repeated-but-uncodified patterns, gaps where the agent had to guess, and components the preview doesn't show yet. You approve the good ones; diff files each approved finding to the right layer and rebuilds the preview.

Nothing happens automatically. `diff` writes only the findings you approve one by one, and `--dry-run` writes nothing.

## Commands

Invoke as `/ds4a <subcommand>`.

| Command | What happens |
|---|---|
| `/ds4a init [type]` | Detect/adopt → overlay → `DESIGN.md` → preview. Later runs re-resolve and rebuild. `--check` = dry run/status; `--adopt` = confirmed adopt; `--tone <name>` = seed tone |
| `/ds4a diff` | Four-pass review (violations, patterns, gaps, specimens); approve/reject each; approved findings merge to project/tone/core/preview; preview rebuilds. `--dry-run` reports only |
| `/ds4a tone` | No args: active tone + project status. `tone <name>` switches; `tone new <name>` forks |
| `/ds4a apply [--check]` | Write resolved tokens to one CSS file (or Tailwind `@theme`); check drift and hardcoded candidates |

The old `detect`, `resolve`, `preview`, `status`, `blend`, `specimens`, and `merge` commands are now steps inside these four — see [SKILL.md](SKILL.md#where-the-old-commands-went). The scripts remain available for direct use.

## Preview

`/ds4a init` (and `tone`, `diff`) rebuild `python3 scripts/build-preview.py --project .`, which writes one self-contained page, `.ds4a/preview.html`, generated from the resolved tokens. It opens offline; only Google Fonts load when online.

- **Foundations:** principles from the tone's Overview, color with WCAG contrast badges, type specimens and the full scale, spacing, radius, shadows, motion.
- **Project specimens:** the components this project *actually* has, captured as static markup in `.ds4a/specimens/` and rendered above the core contracts. Each carries its source file and capture date; `diff` flags drift. Switching tone re-skins them because they use the same tokens.
- **Components:** all 13 core contracts with live states (hover, focus, error, disabled, open, selected). Filtered by project type, with "Show all"; contracts the overlay excludes are hidden.
- **Contracts:** a status matrix — enforced, specimen, excluded, grown, or not used by this project type — so it is obvious what the agent is told to build and what the project replaced.
- **Copy-on-click:** every color, type shorthand, spacing step, radius, shadow and motion value has a ⧉ button.
- **Tone switcher:** every tone in `library/tones/` is built into the page. Compare "this project" (tone + overlay) against the raw tones; components re-shape, not just recolor.
- **Navigation:** grouped sidebar (Foundations, Components, Reference), breadcrumb, search (`/`), and a gliding nav pill on desktop and mobile.
- **Motion from tokens:** every transition uses the tone's `duration.*` and `ease.*`; `prefers-reduced-motion` is respected.

Rebuild after changing the tone, `.ds4a/project.md`, or a specimen — the page does not watch files. Nothing is written outside `.ds4a/`.

## Specimens

The core contracts show what the library promises. **Specimens** show what your project actually built:

Specimens are captured through `/ds4a diff`'s fourth pass, or directly with the script:

```bash
python3 scripts/specimens.py --project . scan
python3 scripts/specimens.py --project . add pill --from src/components/Pill.tsx
```

`add` extracts the markup (React/Vue/Svelte/HTML), writes `.ds4a/specimens/pill.html` with a provenance header (`source`, `captured`, optional `contract:`), registers it in the overlay, and rebuilds the preview. A specimen is a static copy — never a dev-server iframe — so the page stays one file with no build integration. It reads the same custom properties as the rest of the page, so switching tone re-skins it.

`scan` finds component files with no specimen and no matching contract; `diff` proposes the same list. Approving one runs the `add` command above.

## Apply

Stop hand-copying values out of `DESIGN.md`:

```bash
/ds4a apply            # writes src/styles/ds4a-tokens.css
/ds4a apply --tailwind # writes one @theme block to src/styles/ds4a-theme.css
/ds4a apply --check    # drift + hardcoded values that match a token
```

It writes exactly one new file, never edits components or `tailwind.config`, and prints the one `@import` line to add. The file carries a generated marker; `apply` refuses to overwrite a file without it. `--check` writes nothing and lists hardcoded hex/px in source that exactly match a token as migration candidates.

## Four situations you'll hit

1. **You use it at scale.** The library lives in this repo (`library/`). Every project resolves from the same copy, and merges write back to it — so project 10 starts from everything projects 1–9 taught it.
2. **You want several looks, one set of fundamentals.** Switch with `/ds4a tone <name>`. Change one radius step and every component follows (`rounded.md` → buttons, cards…). The contracts never change.
3. **Your project already has a system.** Detection reads AGENTS.md, `tokens.*`, shadcn `globals.css` (oklch → hex), Tailwind v4 `@theme`, `design-tokens.ts`, `tailwind.config`. Found tokens go in the overlay and win; gaps fall back to `neutral`. Nothing you own is overwritten. If a hand-written `DESIGN.md` exists, init stops and asks first — keep both, adopt the generated doc, or abort — and doc-vs-code drift is reported, not silently resolved. `/ds4a init --adopt` migrates that doc: tokens and unique rules move into the overlay, conflicts print with both values and sources, and the old file is backed up while `DESIGN.md` is regenerated in place. Where the project contradicts the library outright, the overlay can drop contracts (`exclude_components:`) or take over a whole section (`<!-- replace -->`) instead of arguing in prose.
4. **Your project has nothing.** You get the `neutral` tone: system fonts, grays, one action color, small radii, a 4px grid, sitting on top of the 13 core contracts (anatomy modeled on Base UI's unstyled parts). Grow it per project in the overlay, or fork it into a tone.

## Core components

13 core contracts — Button, Input, Field/Form/Fieldset, Select, RadioGroup, Card, Badge, Modal, Tabs, Table, Sidebar — benchmarked against UXPin's essential-components list, the shadcn/ui registry and Base UI. Contracts added by reviews carry `(grown)`; a grown contract used by 3+ projects (`library/usage.md`) is offered for promotion to core. See [core-components.md](references/core-components.md).

## Vision

[VISION.md](VISION.md) — the loop ds4a now runs: detect → preview → build → codify, with the overlay as the only hand-edited layer and `DESIGN.md` and the preview as two render targets of it. Shipped in v2.2.0; command surface simplified in v2.3.0.

## Install

```bash
cd ~/.agents/skills        # or your agent's skills directory
git clone https://github.com/dickyudhandika/design-system-for-agents.git ds4a
```

Requires `python3` (standard library only) for all scripts, including `resolve.py`, `build-preview.py`, `blend.py`, `specimens.py`, and `apply.py`.

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
| `scripts/blend.py` | Hand-written `DESIGN.md` → overlay, verified against code; `--adopt` regenerates in place |
| `scripts/specimens.py` | `scan` candidates; `add`/`remove` captured components and register them |
| `scripts/apply.py` | Resolved tokens → one generated CSS file or Tailwind `@theme`; `--check` drift |
| `scripts/oklch-to-hex.py` | shadcn oklch → hex |
| `references/` | detection, blend, specimens, apply, review prompt, matrix, core benchmark, pitfalls |
| `templates/project-overlay.md` | Starting overlay |
| `templates/*.tsx/.astro`, `scripts/build-preview-html.ts` | In-framework `/design-system` references |
| `tests/` | `python3 -m unittest discover -s tests -v` |

## Which AI agents work

Anything that reads project files: Claude Code, Codex, Cursor, Copilot, Hermes, v0, Lovable.

## FAQ

**Do I need to know design?** No. Pick or import a tone, approve suggestions with yes/no.

**Is it framework-specific?** No. `DESIGN.md` is framework-agnostic.

**Will it overwrite my theme or my DESIGN.md?** No. Only `DESIGN.md` (if it's ds4a-generated), `.ds4a/`, and the one `ds4a apply` token file are written; `resolve.py` refuses to overwrite a DESIGN.md it didn't generate, and `apply` refuses a token file without its marker. Adopting a hand-written doc is explicit (`/ds4a init --adopt`) and keeps a backup.

**Why is the preview plain HTML?** It has to open anywhere with no build step and no dependencies, and it shows the tokens in a real browser. For live framework components, use the in-framework `/design-system` references in `templates/`.

**What does the contrast check do?** `resolve.py` and `build-preview.py` warn when `foreground`, `muted-foreground`, or button text fail WCAG AA against their backgrounds. `warm-sharp`'s `muted-foreground` (`#A1A1A1` on `#FDFCF8`) currently fails at 2.5:1 — it's kept as-is so the original look is preserved, but the warning is real.

## License

MIT

## Roadmap

- [x] Multiple base libraries (tones)
- [x] Project specimens + contracts matrix in the preview
- [x] `apply` tokens into one generated CSS file; `--check` drift
- [x] Blend/adopt a hand-written `DESIGN.md`
- [ ] More tones (soft/friendly, dark/technical)
- [ ] Dark-mode tokens per tone
- [ ] Vision check — screenshots + vision AI for issues code can't catch
- [ ] Team libraries — shared evolution across developers

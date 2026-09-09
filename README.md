# design-system-for-agents

> A portable taste layer for AI coding agents. A living DESIGN.md library that starts with a designer's curated taste and compounds with every project. Developers ship world-class UI without learning design.

## What it is

A Hermes skill (also usable by any AI agent that reads project files) that makes AI-generated UI visibly better and gets smarter with every project.

**Three commands power the full loop:**

| Command | What happens |
|---|---|
| `ds4a init [type]` | Detect baseline → install/convert → generate project DESIGN.md |
| *(build normally)* | Agent reads DESIGN.md, generates UI. Skill stays out. |
| `ds4a review` | Three-pass analysis on generated code. Interactive approve/reject. |
| `ds4a merge` | Merge approved rules into `.ds4a/library.md` in-place. |

**Preview:** open `preview/index.html` — a live, browser-viewable showcase of all 13 core contracts, navigated by a sidebar that is itself the Sidebar contract. No server, no build; works offline.

**The loop:**
```
new project → ds4a init → build with AI → ds4a review → approve rules → ds4a merge → library grows → repeat
```

By project 10, the library isn't your defaults anymore — it's your design DNA.

## Core component default

The baseline ships with **13 core component contracts** — benchmarked against UXPin's essential-components list, the shadcn/ui registry (63 components), and Base UI v1.6.0 (38 components). Button, Input, Field/Form, Select, RadioGroup, Card, Badge, Modal, Tabs, Table, Sidebar — every project starts from this floor.

Contracts added by your reviews are marked `(grown)`. A grown contract used across 3+ projects earns a promotion to core. The floor grows as you build — it never shifts under you. See [core-components.md](references/core-components.md) for the benchmark and tier rules.

## Install

### As a Hermes skill

```bash
cd ~/.hermes/profiles/<your-profile>/skills/design/
git clone https://github.com/dickyudhandika/design-system-for-agents.git ds4a
```

Skill auto-registers. Use `ds4a init`, `ds4a review`, `ds4a merge` in chat.

### With other AI agents (Cursor, Claude Code, Copilot, etc.)

```bash
git clone https://github.com/dickyudhandika/design-system-for-agents.git
```

Copy `references/master-library.md` into your project as `DESIGN.md`. Your AI agent reads it as project context. Copy `references/review-prompt.md` for post-project reviews.

### shadcn/ui projects

`ds4a init` detects shadcn CSS variables in `globals.css` and **imports your customized theme — never overwrites it.** oklch values are converted to hex, your variables map onto the ds4a token schema, guardrails are generated from your theme's patterns, and an AA contrast check runs on `muted-foreground`. You keep your theme; you gain the contracts, guardrails, and review loop.

## What's inside

| File | Lines | What |
|---|---|---|
| `SKILL.md` | 439 | Operational loop definition (init, review, merge) |
| `references/master-library.md` | 734 | Curated baseline — 13 core component contracts, 44 guardrails, 10-item pre-flight checklist |
| `references/core-components.md` | 71 | Benchmark table (UXPin × shadcn × Base UI), core/grown/promoted tiers, promotion rules |
| `references/review-prompt.md` | 352 | Three-pass analysis: violation detection, pattern detection, gap detection |
| `references/project-generator-prompt.md` | 242 | Slim subset extractor — 8 project types, 13×8 component matrix |
| `references/component-matrix.md` | 52 | Component relevance + layout rules matrices |
| `references/shadcn-baseline.md` | 154 | shadcn theme import: variable mapping, radius conversion, guardrail derivation |
| `templates/project-design.md` | 66 | Blank DESIGN.md template |
| `scripts/oklch-to-hex.py` | 105 | oklch → hex converter for shadcn theme import |
| `preview/index.html` | 1515 | Live browser showcase — 13 contracts + foundations, self-dogfooding |

## Design aesthetic

The curated baseline uses:
- **Warm white** background (`#FDFCF8`) — paper-like, not clinical
- **Sharp edges** — all radius 0px. Deliberate, not missing
- **Blue accent** (`#1A5EFF`) — CTAs and active states only
- **Fauna One + Inter** — serif titles, sans-serif body
- **4px spacing grid** — consistent rhythm

Change any of these in your `.ds4a/library.md` — the system works with any aesthetic.

## Which AI agents work

Any agent that reads project files:
- ✅ Hermes (native skill)
- ✅ Cursor
- ✅ Claude Code
- ✅ Copilot
- ✅ Codex
- ✅ v0
- ✅ Lovable

## FAQ

**Do I need to know design?** No. Copy the file, your AI gets better, approve suggestions with yes/no.

**Is it framework-specific?** No. DESIGN.md is framework-agnostic. React, Vue, Svelte, Astro, plain HTML.

**I use shadcn — will it overwrite my theme?** No. `ds4a init` detects shadcn variables in `globals.css` and imports your theme into the DESIGN.md format: oklch → hex conversion, variable mapping, generated guardrails, contrast check. `globals.css` and every existing file are untouched — ds4a only writes `.ds4a/library.md` and `DESIGN.md`.

**Non-destructive?** Yes. DESIGN.md sits alongside your existing files. AGENTS.md, tokens.css, globals.css, tailwind.config.js — all untouched.

**How is this different from Cursor Rules?** Cursor Rules are manual. This system: AI suggests rules, you approve, library grows automatically. Your only interaction is yes/no.

## License

MIT

## Roadmap

- [ ] CLI tool (`ds4a` npm package) — same loop, terminal-based, for non-Hermes users
- [ ] Multiple base libraries — different aesthetics (soft/friendly, dark/technical)
- [ ] Vision check — screenshots + vision AI to catch visual issues code can't
- [ ] Team libraries — shared evolution across developers
- [ ] Marketplace — designers sell their taste as base libraries
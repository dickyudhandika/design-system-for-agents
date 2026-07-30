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

**The loop:**
```
new project → ds4a init → build with AI → ds4a review → approve rules → ds4a merge → library grows → repeat
```

By project 10, the library isn't your defaults anymore — it's your design DNA.

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

## What's inside

| File | Lines | What |
|---|---|---|
| `SKILL.md` | 401 | Operational loop definition (init, review, merge) |
| `references/master-library.md` | 591 | Curated baseline — 14 component contracts, 44 guardrails, 10-item pre-flight checklist |
| `references/review-prompt.md` | 352 | Three-pass analysis: violation detection, pattern detection, gap detection |
| `references/project-generator-prompt.md` | 242 | Slim subset extractor — 8 project types, 13×8 component matrix |
| `references/component-matrix.md` | 52 | Component relevance + layout rules matrices |
| `templates/project-design.md` | 66 | Blank DESIGN.md template |

## Design aesthetic

The curated baseline uses:
- **Warm white** background (`#FDFCF8`) — paper-like, not clinical
- **Sharp edges** — all radius 0px. Deliberate, not missing
- **Blue accent** (`#1A5EFF`) — CTAs and active states only
- **Fauna One + Inter** — serif titles, sans-serif body
- **4px spacing grid** — consistent rhythm

Change any of these in your `.ds4a/library.md` — the system works with any aesthetic.

## Validation

All 5 validation tests pass. See [validation report](https://github.com/dickyudhandika/design-system-for-agents/blob/main/references/master-library.md) for details.

| Test | Result |
|---|---|
| Format conversion | ✅ All tokens + guardrails preserved |
| Before/after | ✅ Obvious quality difference with vs without |
| Suggestion quality | ✅ Specific, evidence-backed, taste-matched |
| Evolution loop | ✅ Library grew from 9 → 14 contracts through one review cycle |
| Contract emergence | ✅ 6 card variations → pattern detected → contract suggested |

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

**Non-destructive?** Yes. DESIGN.md sits alongside your existing files. AGENTS.md, tokens.css, tailwind.config.js — all untouched.

**How is this different from Cursor Rules?** Cursor Rules are manual. This system: AI suggests rules, you approve, library grows automatically. Your only interaction is yes/no.

## License

MIT

## Roadmap

- [ ] CLI tool (`ds4a` npm package) — same loop, terminal-based, for non-Hermus users
- [ ] Multiple base libraries — different aesthetics (soft/friendly, dark/technical)
- [ ] Vision check — screenshots + vision AI to catch visual issues code can't
- [ ] Team libraries — shared evolution across developers
- [ ] Marketplace — designers sell their taste as base libraries
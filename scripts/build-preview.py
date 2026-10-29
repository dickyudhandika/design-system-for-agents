#!/usr/bin/env python3
"""ds4a preview — render the resolved tokens as one self-contained HTML page.

Reads the same layers as resolve.py (core + tone + .ds4a/project.md) and writes
<project>/.ds4a/preview.html: colors with live contrast, type scale, spacing,
radius, shadows, and a small component sandbox styled only from tokens. The page
changes with the active tone; nothing is written outside .ds4a/.

Usage:
  python3 scripts/build-preview.py --project . [--tone NAME] [--out FILE]
Standard library only.
"""
import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve as R  # noqa: E402

SYSTEM_FONTS = {"system-ui", "-apple-system", "sans-serif", "serif", "monospace", "segoe ui", "roboto",
                "helvetica", "helvetica neue", "arial", "ui-sans-serif", "ui-monospace", "georgia"}


def build(tree, tone, ptype):
    def g(path, default=""):
        try:
            return R.unquote(R.resolve_value(tree, path))
        except KeyError:
            return default

    colors = [(k, R.unquote(v.value)) for k, v in tree["colors"].items() if isinstance(v, R.Leaf)]
    bg = R._rgb(g("colors.background", "#ffffff")) or (255, 255, 255)

    # Google Fonts link for any non-system family used by the type tokens.
    families = set()
    for k, v in tree["typography"].items():
        if isinstance(v, dict):
            first = R.unquote(v["fontFamily"].value).split(",")[0].strip().strip("\"'")
            if first.lower() not in SYSTEM_FONTS:
                families.add(first)
    font_link = ""
    if families:
        q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700" for f in sorted(families))
        font_link = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{q}&display=swap">'

    css_vars = [f"--color-{k}:{v}" for k, v in colors]
    css_vars += [f"--radius-{k}:{R.unquote(v.value)}" for k, v in tree["rounded"].items() if isinstance(v, R.Leaf)]
    css_vars += [f"--space-{k}:{R.unquote(v.value)}" for k, v in tree["spacing"].items() if isinstance(v, R.Leaf)]

    def tstyle(name):
        t = tree["typography"][name]
        return (f"font-family:{R.unquote(t['fontFamily'].value)};font-size:{R.unquote(t['fontSize'].value)};"
                f"font-weight:{R.unquote(t['fontWeight'].value)};line-height:{R.unquote(t['lineHeight'].value)};"
                f"letter-spacing:{R.unquote(t['letterSpacing'].value)}")

    # Contrast is only meaningful for colors that carry text or UI affordances.
    against = {"foreground": "background", "secondary": "background", "muted-foreground": "background",
               "primary": "background", "destructive": "background", "primary-foreground": "primary"}
    swatches = []
    for k, v in colors:
        rgb = R._rgb(v)
        badge = ""
        if rgb and v.startswith("#") and k in against:
            other = R._rgb(g(f"colors.{against[k]}", "#ffffff")) or bg
            r = R.contrast(rgb, other)
            badge = f'<span class="b">{r:.1f}:1 vs {against[k]} · {"AAA" if r >= 7 else "AA" if r >= 4.5 else "AA-large" if r >= 3 else "fail"}</span>'
        swatches.append(f'<div class="sw"><div class="chip" style="background:{html.escape(v)}"></div>'
                        f'<b>{k}</b><code>{html.escape(v)}</code>{badge}</div>')

    types = "".join(
        f'<div class="trow"><code>{n}</code><div style="{html.escape(tstyle(n))}">The quick brown fox jumps over the lazy dog</div></div>'
        for n, v in tree["typography"].items() if isinstance(v, dict))
    spaces = "".join(
        f'<div class="srow"><code>{k}</code><div class="bar" style="width:{R.unquote(v.value)}"></div><i>{R.unquote(v.value)}</i></div>'
        for k, v in tree["spacing"].items() if isinstance(v, R.Leaf))
    radii = "".join(
        f'<div class="rad" style="border-radius:{R.unquote(v.value)}"><code>{k}</code><i>{R.unquote(v.value)}</i></div>'
        for k, v in tree["rounded"].items() if isinstance(v, R.Leaf))

    btn = lambda var, label: (f'<button class="btn {var}">{label}</button>')
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in
                   [("Alpha", "Active", "12"), ("Beta", "Paused", "7"), ("Gamma", "Failed", "0")])

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ds4a preview — {html.escape(tone)}</title>{font_link}
<style>
:root{{{";".join(css_vars)}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--color-background);color:var(--color-foreground);{tstyle("paragraph-md")}}}
main{{max-width:1040px;margin:0 auto;padding:var(--space-3xl) var(--space-xl)}}
header{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--color-border);padding-bottom:var(--space-lg);margin-bottom:var(--space-2xl)}}
h1{{margin:0;{tstyle("title-h2")}}} h2{{margin:var(--space-3xl) 0 var(--space-lg);{tstyle("title-h5")}}}
code{{font-family:ui-monospace,monospace;font-size:12px;color:var(--color-muted-foreground)}}
.tag{{{tstyle("label-sm")};color:var(--color-muted-foreground)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:var(--space-lg)}}
.sw{{display:flex;flex-direction:column;gap:var(--space-xs)}} .chip{{height:56px;border:1px solid var(--color-border)}}
.b{{{tstyle("label-xs")};color:var(--color-muted-foreground)}}
.trow{{display:grid;grid-template-columns:120px 1fr;gap:var(--space-lg);align-items:baseline;padding:var(--space-sm) 0;border-bottom:1px solid var(--color-border)}}
.srow{{display:grid;grid-template-columns:48px 80px 1fr;gap:var(--space-md);align-items:center;margin-bottom:var(--space-xs)}}
.bar{{height:12px;background:var(--color-primary)}} i{{font-style:normal;font-size:12px;color:var(--color-muted-foreground)}}
.rad{{width:104px;height:72px;border:1px solid var(--color-border);background:var(--color-muted);display:flex;flex-direction:column;align-items:center;justify-content:center}}
.row{{display:flex;gap:var(--space-lg);flex-wrap:wrap;align-items:center}}
.shadow{{width:160px;height:80px;background:var(--color-background);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center}}
.btn{{padding:{g("components.button.padding-md")};border-radius:{g("components.button.radius")};{tstyle("label-md")};border:1px solid transparent;cursor:pointer}}
.btn.primary{{background:var(--color-primary);color:var(--color-primary-foreground)}}
.btn.secondary{{background:var(--color-muted);color:var(--color-foreground)}}
.btn.ghost{{background:transparent;color:var(--color-foreground)}} .btn.ghost:hover{{border-color:var(--color-border)}}
.btn.destructive{{background:var(--color-destructive);color:var(--color-primary-foreground)}}
.btn:focus-visible,input:focus-visible{{outline:2px solid var(--color-primary);outline-offset:2px}}
input{{padding:{g("components.input.padding-md")};border:{g("components.input.border")};border-radius:{g("components.input.radius")};{tstyle("paragraph-md")};background:var(--color-background);color:var(--color-foreground);width:260px}}
input::placeholder{{color:var(--color-muted-foreground)}} input.err{{border-color:var(--color-destructive)}}
.badge{{display:inline-flex;gap:{g("components.badge.gap")};padding:{g("components.badge.padding")};border-radius:{g("components.badge.radius")};{tstyle("label-xs")}}}
.badge.d{{background:var(--color-muted);border:1px solid var(--color-border)}} .badge.p{{background:var(--color-primary);color:var(--color-primary-foreground)}} .badge.x{{background:var(--color-destructive);color:var(--color-primary-foreground)}}
.card{{padding:{g("components.card.padding")};border:{g("components.card.border")};border-radius:{g("components.card.radius")};width:280px}}
.tabs{{display:flex;border-bottom:{g("components.tabs.list-border")};width:100%}}
.tabs span{{padding:{g("components.tabs.trigger-padding")};{tstyle("label-md")};color:var(--color-muted-foreground);border-bottom:{g("components.tabs.indicator-height")} solid transparent;margin-bottom:-1px}}
.tabs span.on{{color:var(--color-foreground);border-color:var(--color-{g("components.tabs.indicator-color", "primary")})}}
table{{width:100%;border-collapse:collapse}} th{{{tstyle("label-sm")};color:var(--color-muted-foreground);text-align:left}}
td{{{tstyle("paragraph-sm")}}} th,td{{padding:{g("components.table.row-padding")};border-bottom:{g("components.table.row-border")}}}
tr:hover td{{background:var(--color-{g("components.table.hover-background", "muted")})}}
</style></head><body><main>
<header><h1>{html.escape(tone)}</h1><span class="tag">ds4a preview · {html.escape(ptype or "all components")} · generated from tokens</span></header>
<h2>Color</h2><div class="grid">{"".join(swatches)}</div>
<h2>Typography</h2>{types}
<h2>Spacing</h2>{spaces}
<h2>Radius</h2><div class="row">{radii}</div>
<h2>Shadow</h2><div class="row">
  <div class="shadow" style="box-shadow:{shadow(tree, "subtle")}"><code>subtle</code></div>
  <div class="shadow" style="box-shadow:{shadow(tree, "elevated")}"><code>elevated</code></div></div>
<h2>Components</h2>
<div class="row" style="margin-bottom:var(--space-xl)">{btn("primary","Primary")}{btn("secondary","Secondary")}{btn("ghost","Ghost")}{btn("destructive","Destructive")}</div>
<div class="row" style="margin-bottom:var(--space-xl)"><input placeholder="Placeholder text"><input class="err" value="Invalid value">
  <span class="badge d">Default</span><span class="badge p">Primary</span><span class="badge x">Destructive</span></div>
<div class="row" style="margin-bottom:var(--space-xl)"><div class="card"><b>Card</b><p style="margin:var(--space-sm) 0 0">Surface with token padding, border and radius.</p></div>
  <div style="flex:1;min-width:300px"><div class="tabs"><span class="on">Overview</span><span>Activity</span><span>Settings</span></div>
  <table><tr><th>Name</th><th>Status</th><th>Count</th></tr>{rows}</table></div></div>
</main></body></html>"""
    return page


def shadow(tree, name):
    """Shadow values live in tone prose tables, not frontmatter — read them from the tone file."""
    tone_text = (R.SKILL_DIR / "library" / "tones" / f"{shadow.tone}.md").read_text(encoding="utf-8")
    m = re.search(rf"\|\s*`{name}`\s*\|\s*`([^`]+)`", tone_text)
    return html.escape(m.group(1)) if m else "none"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=".")
    ap.add_argument("--library", default=str(R.SKILL_DIR / "library"))
    ap.add_argument("--tone")
    ap.add_argument("--type", dest="ptype")
    ap.add_argument("--out")
    args = ap.parse_args()
    lib, project = Path(args.library), Path(args.project)
    overlay = project / ".ds4a" / "project.md"
    tone, ptype = args.tone, args.ptype
    try:
        if overlay.exists():
            ov_fm, _, _ = R.read_layer(overlay)
            tone = tone or R.leaf_text(ov_fm, "tone") or None
            ptype = ptype or R.leaf_text(ov_fm, "type") or None
        tone = tone or "neutral"
        _, info = R.resolve(lib, tone, overlay if overlay.exists() else None, ptype)
    except R.ResolveError as e:
        print(f"ds4a preview: {e}", file=sys.stderr)
        return 1
    shadow.tone = tone
    out = Path(args.out) if args.out else project / ".ds4a" / "preview.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(info["tree"], tone, ptype), encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

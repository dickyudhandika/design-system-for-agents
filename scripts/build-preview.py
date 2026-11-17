#!/usr/bin/env python3
"""ds4a preview: render the resolved design system as one self-contained HTML page.

Reads the same layers as resolve.py (core + tone + .ds4a/project.md), plus the
project's captured specimens in .ds4a/specimens/, and writes
<project>/.ds4a/preview.html: hero, principles, color with live contrast, type
specimens and scale, spacing, radius, elevation and motion, the project's
specimens, all 13 core contracts with their states, a contracts status matrix,
and the raw resolved tokens with copy-on-click. Sticky nav, search, and a tone
switcher: every library tone is resolved at build time and emitted as CSS
variables under [data-tone], so the whole page re-skins. Components are styled
only through --c-<component>-<key> variables. Nothing is written outside .ds4a/.

Usage:
  python3 scripts/build-preview.py --project . [--tone NAME] [--type TYPE] [--out FILE]
Standard library only.
"""
import argparse
import html
import re
from urllib.parse import quote
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve as R  # noqa: E402
import specimens as SPEC  # noqa: E402

SYSTEM_FONTS = {"system-ui", "-apple-system", "blinkmacsystemfont", "sans-serif", "serif", "monospace",
                "segoe ui", "roboto", "helvetica", "helvetica neue", "arial", "georgia", "ui-sans-serif",
                "ui-serif", "ui-monospace", "ui-rounded", "sf pro", "sf pro display", "sf pro text"}
COLOR_GROUPS = [("Surfaces", ["background", "muted", "border"]),
                ("Text", ["foreground", "secondary", "muted-foreground"]),
                ("Brand", ["primary", "primary-foreground"]),
                ("States", ["destructive"])]
# Contrast is only meaningful for colors that carry text or UI affordances: (against, needed ratio).
AGAINST = {"foreground": ("background", 4.5), "secondary": ("background", 4.5),
           "muted-foreground": ("background", 4.5), "primary": ("background", 3.0),
           "destructive": ("background", 4.5), "primary-foreground": ("primary", 4.5)}
TYPE_SAMPLES = {"title": "Design is how it works", "label": "Save changes",
                "paragraph": "Good interfaces are quiet. They let the content lead."}
TYPE_GROUPS = {"title": "Titles", "label": "Labels", "paragraph": "Paragraphs"}

esc = html.escape


# Icons are CSS masks defined once (see @icon in PAGE_CSS), not inline SVG per button.
ICONS_CSS = {
    "copy": '<rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5V4a1.5 1.5 0 00-1.5-1.5H4A1.5 1.5 0 002.5 4v5A1.5 1.5 0 004 10.5h1.5"/>',
    "done": '<path d="M3.5 8.5l3 3 6-7"/>',
}


def icon_url(n):
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='black' stroke-width='1.6' "
           f"stroke-linecap='round' stroke-linejoin='round'>{ICONS_CSS[n]}</svg>").replace('"', "'")
    return 'url("data:image/svg+xml,' + quote(svg, safe=" '=:/.-") + '")'


def copy_btn(value, label="Copy value", text=""):
    t = f"<span>{esc(text)}</span>" if text else ""
    return (f'<button class="cp{" cpt" if text else ""}" type="button" data-copy="{esc(value)}" aria-label="{esc(label)}" '
            f'title="Copy">{t}</button>')


def md_inline(s):
    s = esc(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


def leaves(node):
    return [(k, R.unquote(v.value), v.comment.lstrip("# ").strip())
            for k, v in (node or {}).items() if isinstance(v, R.Leaf)]


def type_steps(tree):
    return [(n, {k: R.unquote(x.value) for k, x in v.items() if isinstance(x, R.Leaf)})
            for n, v in tree.get("typography", {}).items() if isinstance(v, dict)]


def first_family(stack):
    return stack.split(",")[0].strip().strip("\"'")


def css_safe(s):
    return re.sub(r"[;{}<]", "", s)


def prose_table(text, heading):
    """Rows of the markdown table under `### heading`: {token: (value, use)}."""
    m = re.search(rf"^### {re.escape(heading)}\s*$(.*?)(?=^#{{2,3}} |\Z)", text, re.M | re.S)
    rows = {}
    for line in (m.group(1) if m else "").split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: ") or cells[0] == "Token":
            continue
        rows[cells[0].strip("`")] = (cells[1].strip("`"), cells[2] if len(cells) > 2 else "")
    return rows


# ───────────────────────── per-tone data ─────────────────────────

def make_entry(lib, key, label, tone, overlay, ptype, overlay_colors=()):
    doc, info = R.resolve(lib, tone, overlay, ptype)
    # Shadow and motion values live in prose tables, not frontmatter; an overlay table wins.
    texts = [(lib / "tones" / f"{tone}.md").read_text(encoding="utf-8")]
    if overlay:
        texts.append(Path(overlay).read_text(encoding="utf-8"))
    shadows, motion = {}, {}
    for t in texts:
        shadows.update(prose_table(t, "Shadow tokens"))
        motion.update(prose_table(t, "Motion tokens"))
    return {"key": key, "label": label, "tone": tone, "tree": info["tree"], "doc": doc,
            "layers": info["layers"], "shadows": shadows, "motion": motion,
            "project_colors": set(overlay_colors), "overlay": bool(overlay)}


def tone_vars(e):
    """Flatten a resolved tree to custom properties. Components read only --c-* variables."""
    t, out = e["tree"], []
    colors = leaves(t.get("colors"))
    cnames = {k for k, _, _ in colors}
    out += [f"--color-{k}:{v}" for k, v, _ in colors]
    out += [f"--radius-{k}:{v}" for k, v, _ in leaves(t.get("rounded"))]
    out += [f"--space-{k}:{v}" for k, v, _ in leaves(t.get("spacing"))]
    # One composite `font` value per type step; family stacks are shared through --ff-N.
    fams = {}
    for n, spec in type_steps(t):
        g = spec.get
        stack = g("fontFamily", "system-ui")
        if stack not in fams:
            fams[stack] = f"--ff-{len(fams)}"
            out.append(f"{fams[stack]}:{stack}")
        out.append(f"--t-{n}:{g('fontWeight', '400')} {g('fontSize', '16px')}/{g('lineHeight', 'normal')} var({fams[stack]})")
        out.append(f"--t-{n}-ls:{g('letterSpacing', 'normal')}")
    sh = e["shadows"]
    out += [f"--shadow-{n}:{sh[n][0] if n in sh else 'none'}" for n in sorted(set(sh) | {"subtle", "elevated"})]
    mo = lambda k, d: e["motion"].get(k, (d,))[0]  # noqa: E731
    out += [f"--motion-fast:{mo('duration.fast', '150ms')}", f"--motion-smooth:{mo('duration.smooth', '250ms')}",
            f"--ease-out:{mo('ease.out', 'ease-out')}", f"--ease-in-out:{mo('ease.in-out', 'ease-in-out')}"]
    for comp, node in t.get("components", {}).items():
        if not isinstance(node, dict):
            continue
        for k, v, _ in leaves(node):
            if v.startswith("["):
                continue  # variant lists are docs, not values
            if v in cnames:
                v = f"var(--color-{v})"
            elif k == "shadow" and re.fullmatch(r"[a-z0-9-]+", v):
                v = f"var(--shadow-{v})"
            out.append(f"--c-{comp}-{k}:{v}")
    return ";".join(css_safe(x) for x in out)


# ───────────────────────── per-tone sections ─────────────────────────

def hero(e, ptype):
    t = e["tree"]
    warns = R.contrast_report(t)
    if warns:
        contrast = f'<dd class="bad">{len(warns)} warning{"s" if len(warns) > 1 else ""}</dd>'
        wl = '<ul class="warns">' + "".join(f"<li>{esc(w)}</li>" for w in warns) + "</ul>"
    else:
        contrast, wl = '<dd class="ok">AA pass</dd>', ""
    tag = "this project" if e["key"] == "project" else "library tone"
    values = {k: v for k, v, _ in leaves(t.get("colors"))}
    ribbon = "".join(f'<div><i style="background:var(--color-{c})"></i><b>{c}</b><code>{esc(values[c])}</code></div>'
                     for c in ("background", "muted", "border", "muted-foreground", "foreground", "primary", "destructive")
                     if c in values)
    facts = [("Version", f'v{R.leaf_text(t, "version", "?")}'), ("Project type", ptype or "all types"),
             ("Resolved from", e["layers"])]
    dl = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in facts)
    return f"""<div class="hero">
<h1 class="t-title-h2">{esc(R.leaf_text(t, "name", e["tone"]))}<span class="proj">{tag}</span></h1>
<p class="lead t-paragraph-lg">{md_inline(R.leaf_text(t, "description"))}</p>
<dl class="facts">{dl}<div><dt>Contrast</dt>{contrast}</div></dl>{wl}</div>
<div class="ribbon">{ribbon}</div>"""


def principles(e, core_overview):
    ov = R.split_sections(e["doc"]).get("Overview", "")
    core_start = core_overview.strip().split("\n")[0][:40]
    if core_start and core_start in ov:
        ov = ov[:ov.index(core_start)]
    lead, bullets, paras = "", [], []
    for p in (p.strip() for p in re.split(r"\n\s*\n", ov) if p.strip()):
        if p.startswith(("#", "|", "<!--")):
            continue
        lines = p.split("\n")
        if not any(line.startswith("- ") for line in lines):
            text = " ".join(line.strip() for line in lines)
            if not lead:
                lead = text
            elif not bullets:
                paras.append(text)
            continue
        cur = None  # lines before the first bullet are a list heading; skip them
        for line in lines:
            if line.startswith("- "):
                cur = [line[2:].strip()]
                bullets.append(cur)
            elif cur is not None:
                cur.append(line.strip())
    items = [" ".join(b) for b in bullets][:6] or ([" ".join(paras)] if paras else [])
    cards = []
    for i, b in enumerate(items, 1):
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", b)
        head, body = (m.group(1), m.group(2)) if m else ("", b)
        cards.append(f'<div class="pcard" data-s="principle"><span class="pn">{i:02d}</span>'
                     f'{f"<b>{md_inline(head)}</b>" if head else ""}<p>{md_inline(body)}</p></div>')
    core = core_overview.strip().split("\n\n")[0] if core_overview.strip() else ""
    return (f'<p class="plead t-paragraph-xl">{md_inline(lead)}</p><div class="pgrid">{"".join(cards)}</div>'
            + (f'<p class="pcore">{md_inline(core)}</p>' if core else ""))


def swatch(colors, k, v, role):
    badge = ""
    if k in AGAINST and AGAINST[k][0] in colors:
        other, need = AGAINST[k]
        a, b = R._rgb(v), R._rgb(colors[other])
        if a and b and v.startswith("#"):
            r = R.contrast(a, b)
            lvl = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA large" if r >= 3 else "fail"
            badge = (f'<span class="cr{" bad" if r < need else ""}">{r:.1f}:1 · {lvl}</span>'
                     f'<span class="vs">vs {other}, needs {need:g}:1</span>')
    return (f'<div class="sw" data-s="color"><div class="chip" style="background:{esc(v)}"></div>'
            f'<div class="swb"><b>{esc(k)}</b><div class="valrow"><code>{esc(v)}</code>{copy_btn(v, f"Copy {k}")}</div>'
            f'{f"<p>{esc(role)}</p>" if role else ""}{badge}</div></div>')


def colors(e):
    cols = leaves(e["tree"].get("colors"))
    by = {k: (k, v, r) for k, v, r in cols}
    known = {k for _, ks in COLOR_GROUPS for k in ks}
    groups = [(g, [by[k] for k in ks if k in by]) for g, ks in COLOR_GROUPS]
    extra = [c for c in cols if c[0] not in known]
    groups += [("Palette", [c for c in extra if c[0] not in e["project_colors"]]),
               ("Project", [c for c in extra if c[0] in e["project_colors"]])]
    values = {k: v for k, v, _ in cols}
    return "".join(f'<div class="grp"><h3 class="gh">{g}</h3><div class="sgrid">'
                   + "".join(swatch(values, *c) for c in cs) + "</div></div>" for g, cs in groups if cs)


def typography(e):
    steps = type_steps(e["tree"])
    fams = {}
    for n, spec in steps:
        stack = spec.get("fontFamily", "system-ui")
        f = fams.setdefault(first_family(stack), {"stack": stack, "cats": [], "w": set()})
        cat = TYPE_GROUPS.get(n.split("-")[0], n.split("-")[0])
        if cat not in f["cats"]:
            f["cats"].append(cat)
        f["w"].add(spec.get("fontWeight", ""))
    out = ['<div class="fams">']
    for name, f in fams.items():
        st = esc(f"font-family:{f['stack']}")
        out.append(f'<div class="fam" data-s="font family"><div class="aa" style="{st}">Aa</div><div>'
                   f'<b>{esc(name)}</b><p>{esc(", ".join(f["cats"]))} · weights {esc(", ".join(sorted(f["w"])))}</p>'
                   f'<p class="abc" style="{st}">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 &amp;?!</p>'
                   "</div></div>")
    out.append("</div>")
    cat = None
    for n, spec in steps:
        c = n.split("-")[0]
        if c != cat:
            cat = c
            out.append(f'<h3 class="gh">{TYPE_GROUPS.get(c, c)}</h3>')
        g = spec.get
        shorthand = f'{g("fontWeight", "400")} {g("fontSize", "16px")}/{g("lineHeight", "normal")} {g("fontFamily", "system-ui")}'
        out.append(f'<div class="trow" data-s="type"><div class="tmeta"><code>{esc(n)}</code>'
                   f'<span>{esc(g("fontSize", ""))} · {esc(g("fontWeight", ""))} · {esc(g("lineHeight", ""))} · '
                   f'{esc(g("letterSpacing", ""))}</span>{copy_btn(shorthand, f"Copy {n} font shorthand")}</div>'
                   f'<div class="tsample t-{esc(n)}">{TYPE_SAMPLES.get(c, TYPE_SAMPLES["paragraph"])}</div></div>')
    return "".join(out)


def spacing(e):
    return "".join(f'<div class="srow" data-s="space"><code>{esc(k)}</code><span>{esc(v)}</span>'
                   f'<div><div class="bar" style="width:{esc(v)}"></div></div>'
                   f'{copy_btn(v, f"Copy spacing {k}")}</div>'
                   for k, v, _ in leaves(e["tree"].get("spacing")))


def radius(e):
    return '<div class="rgrid">' + "".join(
        f'<div class="rad" data-s="radius rounded"><div class="rshape" style="border-top-left-radius:{esc(v)}"></div>'
        f'<div class="rmeta"><div><code>{esc(k)}</code><span>{esc(v)}</span></div>{copy_btn(v, f"Copy radius {k}")}</div></div>'
        for k, v, _ in leaves(e["tree"].get("rounded"))) + "</div>"


def elevation(e):
    sh = dict(e["shadows"])
    for n in ("subtle", "elevated"):
        sh.setdefault(n, ("none", "Not defined by this tone."))
    tiles = "".join(f'<div class="sh" data-s="shadow" style="box-shadow:{esc(v)}"><b>{esc(n)}</b>'
                    f'<div class="valrow"><code>{esc(v)}</code>{copy_btn(v, f"Copy shadow {n}")}</div>'
                    f'<span>{esc(u)}</span></div>' for n, (v, u) in sh.items())
    mo = e["motion"]
    ease = mo.get("ease.out", ("ease-out",))[0]
    smooth = mo.get("duration.smooth", ("250ms",))[0]
    rows = []
    for n, (v, u) in mo.items():
        d, ez = (v, ease) if n.startswith("duration") else (smooth, v)
        rows.append(f'<div class="mrow" data-s="motion" style="--d:{esc(d)};--e:{esc(ez)}">'
                    f'<div><code>{esc(n)}</code><span>{esc(v)}</span>{copy_btn(v, f"Copy {n}")}<p>{esc(u)}</p></div>'
                    f'<div class="track"><i></i></div></div>')
    motion = (f'<h3 class="gh">Motion <span class="hint">hover a row to play</span></h3><div class="mlist">{"".join(rows)}</div>'
              if rows else "")
    return f'<h3 class="gh">Shadows</h3><div class="egrid">{tiles}</div>{motion}'


def bare(node):
    return {k: bare(v) if isinstance(v, dict) else R.Leaf(v.value, block=v.block)
            for k, v in node.items() if not isinstance(v, R.Comment)}


def tokens(e):
    if e["key"] != "project":
        return (f'<p class="sub">Library tone, shown without the project overlay. Its raw tokens are the frontmatter '
                f'of <code>library/tones/{esc(e["tone"])}.md</code>; switch back to <em>this project</em> for the '
                f'resolved dump.</p>')
    yaml = "\n".join(R.emit_yaml(bare(e["tree"])))
    return (f'<details class="raw"><summary>Resolved frontmatter · {e["layers"]} · {yaml.count(chr(10)) + 1} lines'
            f'</summary><pre><code>{esc(yaml)}</code></pre></details>'
            f'<div class="rawcopy">{copy_btn(yaml, "Copy resolved tokens", "Copy all")}</div>')


# ───────────────────────── components (rendered once, styled by --c-* vars) ─────────────────────────

ICONS = {"grid": '<rect x="2.5" y="2.5" width="4.5" height="4.5"/><rect x="9" y="2.5" width="4.5" height="4.5"/>'
                 '<rect x="2.5" y="9" width="4.5" height="4.5"/><rect x="9" y="9" width="4.5" height="4.5"/>',
         "inbox": '<path d="M2.5 9.5h3l1 2h3l1-2h3"/><rect x="2.5" y="3" width="11" height="10"/>',
         "chart": '<path d="M3 13V8M8 13V3M13 13V6"/>', "users": '<circle cx="6" cy="6" r="2.5"/><path d="M2 13c0-2.2 1.8-4 4-4s4 1.8 4 4M11 4.5a2 2 0 010 4M12 9.5c1.3.5 2 1.8 2 3.5"/>',
         "gear": '<circle cx="8" cy="8" r="2"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4"/>',
         "panel": '<rect x="2.5" y="2.5" width="11" height="11"/><path d="M6 2.5v11"/>',
         "chev": '<path d="M4 6l4 4 4-4"/>', "x": '<path d="M4 4l8 8M12 4l-8 8"/>'}


def icon(n, cls=""):
    return (f'<svg class="ic {cls}" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>')


def cap(s):
    return f'<span class="cap">{s}</span>'


def block(title, body):
    return f'<div class="blk"><p class="blkh">{title}</p>{body}</div>'


def c_button():
    states = [("default", "", ""), ("hover", " is-hover", ""), ("focus", " is-focus", ""), ("disabled", "", " disabled")]
    grid = ['<div class="mx"><span class="mh"></span>'] + [f'<span class="cap mh">{s}</span>' for s, _, _ in states]
    for v in ("primary", "secondary", "ghost", "destructive"):
        grid.append(f'<span class="cap">{v}</span>')
        grid += [f'<div><button class="btn btn-{v}{c}"{a}>{v.title()}</button></div>' for _, c, a in states]
    grid.append("</div>")
    fig = lambda b, c: f'<figure>{b}<figcaption class="cap">{c}</figcaption></figure>'  # noqa: E731
    sizes = ('<div class="bsizes">'
             + "".join(fig(f'<button class="btn btn-primary btn-{s}">Button</button>', s) for s in ("sm", "md", "lg"))
             + fig(f'<button class="btn btn-secondary btn-icon" aria-label="Settings">{icon("gear")}</button>', "icon")
             + "</div>")
    return block("Variants × states", f'<div class="scroll">{"".join(grid)}</div>') + block("Sizes", sizes)


def c_input():
    cells = [("default", '<input class="inp" placeholder="you@company.com">'),
             ("focus", '<input class="inp is-focus" value="ada@lovelace.dev">'),
             ("error", '<input class="inp err" value="ada@" aria-invalid="true">'),
             ("disabled", '<input class="inp" value="Read only" disabled>')]
    return '<div class="g2">' + "".join(f"<div>{cap(s)}{h}</div>" for s, h in cells) + "</div>"


def c_field():
    return ('<div class="g2"><div class="field"><label for="f1">Workspace name</label><input id="f1" class="inp" value="Acme">'
            '<p class="fdesc">Shown in the sidebar and invites.</p></div>'
            '<div class="field" data-invalid><label for="f2">Workspace URL</label><input id="f2" class="inp" value="acme corp" '
            'aria-invalid="true" aria-describedby="f2err"><div class="ferr" id="f2err" aria-live="polite">'
            'Use letters, numbers and dashes only.</div></div></div>')


def c_fieldset():
    return ('<div class="g2"><fieldset class="fs"><legend>Shipping address</legend>'
            '<div class="field"><label for="s1">Street</label><input id="s1" class="inp" value="1 Infinite Loop"></div>'
            '<div class="field"><label for="s2">City</label><input id="s2" class="inp" placeholder="City"></div></fieldset>'
            '<fieldset class="fs" disabled><legend>Billing (disabled)</legend>'
            '<div class="field"><label for="s3">Street</label><input id="s3" class="inp" value="Same as shipping"></div>'
            '<div class="field"><label for="s4">City</label><input id="s4" class="inp" placeholder="City"></div></fieldset></div>')


def c_form():
    return ('<form class="form" onsubmit="return false"><div class="field"><label for="l1">Email</label>'
            '<input id="l1" class="inp" type="email" placeholder="you@company.com"></div>'
            '<div class="field"><label for="l2">Password</label><input id="l2" class="inp" type="password" value="hunter22">'
            '<p class="fdesc">At least 8 characters.</p></div>'
            '<div class="row"><button class="btn btn-primary" type="submit">Sign in</button>'
            '<button class="btn btn-ghost" type="button">Forgot password?</button></div></form>')


def c_select():
    def sel(open_, i):
        sid = f"freq{i}"
        opts = "".join(
            f'<div class="opt{c}" id="{sid}-o{j}" role="option" aria-selected="{str("selected" in c).lower()}"'
            f'{" aria-disabled=true" if "dis" in c else ""}>{n}</div>'
            for j, (n, c) in enumerate((("Daily", " hl"), ("Weekly", " selected"), ("Monthly", ""), ("Never", " dis"))))
        return (f'<div class="selw"><button class="sel{" open" if open_ else ""}" type="button" id="{sid}" role="combobox" '
                f'aria-haspopup="listbox" aria-expanded="{str(open_).lower()}" aria-controls="{sid}-pop" '
                f'aria-label="Notification frequency"><span class="val">Weekly</span>{icon("chev", "chev")}</button>'
                f'<div class="pop{"" if open_ else " closed"}" id="{sid}-pop" role="listbox" aria-labelledby="{sid}">'
                f'{opts}</div></div>')
    return f'<div class="g2"><div>{cap("closed")}{sel(False, 1)}</div><div>{cap("open")}{sel(True, 2)}</div></div>'


def c_radio():
    radios = "".join(f'<label class="radio{" is-disabled" if d else ""}"><input type="radio" name="rg1"{" checked" if c else ""}'
                     f'{" disabled" if d else ""}>{n}</label>'
                     for n, c, d in (("Email", True, False), ("SMS", False, False), ("Push (disabled)", False, True)))
    cards = "".join(f'<label class="rcard"><input type="radio" name="rg2"{" checked" if c else ""}><div><b>{n}</b>'
                    f'<span>{d}</span></div></label>'
                    for n, d, c in (("Starter", "Free for up to 3 seats.", True), ("Pro", "$12 per seat, billed yearly.", False)))
    return (f'<div class="g2"><div>{cap("radio · checked / unchecked / disabled")}<div class="rg">{radios}</div></div>'
            f'<div>{cap("radio card")}<div class="rg">{cards}</div></div></div>')


def c_card():
    body = lambda t, d: f"<h4>{t}</h4><p>{d}</p>"  # noqa: E731
    return ('<div class="g3">'
            f'<div>{cap("default")}<div class="card">{body("Monthly revenue", "Surface with token padding, border and radius.")}</div></div>'
            f'<div>{cap("elevated")}<div class="card elev">{body("Floating", "Uses shadow.elevated for popover-like content.")}</div></div>'
            f'<div>{cap("flush")}<div class="card flush"><div class="media"></div><div class="fb">{body("Media card", "Content manages its own spacing.")}</div></div></div>'
            "</div>")


def c_badge():
    return ('<div class="row"><span class="badge badge-default">Default</span><span class="badge badge-primary">Active</span>'
            '<span class="badge badge-destructive">Failed</span></div>'
            '<p class="inline">Deploy <code>v2.4.1</code> <span class="badge badge-primary">Live</span> shipped 3 minutes ago.</p>')


def c_modal():
    ghost = "".join(f'<i style="width:{w}%"></i>' for w in (40, 90, 75, 85, 60, 80))
    return (f'<div class="stage"><div class="ghostpage">{ghost}</div><div class="backdrop"></div>'
            '<div class="modal" role="group" aria-labelledby="mt"><div class="mh"><h4 id="mt">Delete project?</h4>'
            f'<button class="btn btn-ghost btn-icon" aria-label="Close">{icon("x")}</button></div>'
            '<div class="mb">This removes the project, its deployments and 14 environment variables. This cannot be undone.</div>'
            '<div class="mf"><button class="btn btn-secondary">Cancel</button><button class="btn btn-destructive">Delete project</button></div>'
            "</div></div>")


def c_tabs():
    tabs = [("Overview", "Traffic is up 12% week over week. Three deploys shipped today."),
            ("Activity", "Ada merged #482 · Grace opened #483 · Linus commented on #479."),
            ("Settings", "Branch protection, environment variables and build hooks."),
            ("Billing", "")]
    def tab(i, n, p):
        controls = f' aria-controls="tp{i}"' if p else ""
        return (f'<button class="tab" role="tab" id="tab{i}"{controls} aria-selected="{str(i == 0).lower()}" '
                f'tabindex="{0 if i == 0 else -1}"{" disabled" if not p else ""}>{n}</button>')
    tl = "".join(tab(i, n, p) for i, (n, p) in enumerate(tabs))
    tp = "".join(f'<div class="tp" role="tabpanel" id="tp{i}" aria-labelledby="tab{i}"{"" if i == 0 else " hidden"}>{p}</div>'
                 for i, (n, p) in enumerate(tabs) if p)
    return f'<div class="tabsx"><div class="tl" role="tablist">{tl}</div>{tp}</div>'


def c_table():
    rows = [("api-gateway", "primary", "Healthy", "Ada L.", "1,204"), ("billing-worker", "default", "Paused", "Grace H.", "87"),
            ("search-index", "destructive", "Failed", "Linus T.", "0"), ("web-frontend", "primary", "Healthy", "Ada L.", "9,310")]
    body = "".join(f'<tr{" class=selected" if i == 1 else ""}><td class="ck"><input type="checkbox" aria-label="Select {n}"'
                   f'{" checked" if i == 1 else ""}></td><td>{n}</td><td><span class="badge badge-{b}">{s}</span></td>'
                   f'<td>{o}</td><td class="num">{r}</td></tr>' for i, (n, b, s, o, r) in enumerate(rows))
    return ('<div class="scroll"><table class="tbl"><thead><tr><th class="ck"><input type="checkbox" aria-label="Select all"></th>'
            f'<th>Service</th><th>Status</th><th>Owner</th><th class="num">Requests {icon("chev")}</th></tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def c_sidebar():
    def item(n, ic, cls="", count=""):
        if "dis" in cls:
            return (f'<span class="sbi{cls}" aria-disabled="true" title="{n}">{icon(ic)}'
                    f'<span class="lbl">{n}</span></span>')
        badge = f'<span class="badge badge-default sbn" aria-label="{count} unread">{count}</span>' if count else ""
        return f'<a class="sbi{cls}" href="#components" title="{n}">{icon(ic)}<span class="lbl">{n}</span>{badge}</a>'
    nav = (f'<nav class="sb" id="sb-demo" aria-label="Sample"><div class="sbh"><i></i><span class="lbl">Acme</span></div>'
           f'<div class="sbs"><div class="sbsh">Workspace</div>{item("Dashboard", "grid", " active")}{item("Inbox", "inbox", "", "3")}'
           f'{item("Analytics", "chart")}</div><div class="sbs"><div class="sbsh">Team</div>{item("Members", "users")}'
           f'{item("Settings", "gear")}{item("Archive", "inbox", " dis")}</div>'
           f'<div class="sbf"><span class="sbu" title="Ada Lovelace"><b aria-hidden="true">AL</b><span class="lbl">'
           f'<span>Ada Lovelace</span><small>ada@acme.dev</small></span></span>'
           f'<button class="btn btn-ghost btn-icon" data-collapse aria-label="Collapse sidebar" '
           f'aria-expanded="true" aria-controls="sb-demo">{icon("panel")}</button></div></nav>')
    def spark(pts):
        step = 80 / (len(pts) - 1)
        line = " ".join(f"{i * step:.0f},{22 - v * 20:.1f}" for i, v in enumerate(pts))
        return (f'<svg class="spark" viewBox="0 0 80 24" preserveAspectRatio="none" aria-hidden="true">'
                f'<polyline points="{line}"/></svg>')
    stats = "".join(
        f'<div class="sbst"><span>{k}</span><b>{v}</b><div class="sbdelta"><em title="vs previous 7 days">{d}</em>{spark(pts)}</div></div>'
        for k, v, d, pts in (("Visitors", "12,480", "▲ 12.4%", (.2, .35, .3, .5, .45, .7, .9)),
                             ("Conversion", "3.2%", "▲ 0.4 pt", (.5, .4, .55, .5, .6, .58, .7)),
                             ("Revenue", "$8,240", "▼ 2.1%", (.7, .8, .6, .65, .5, .55, .45))))
    feed = "".join(f'<li><b aria-hidden="true">{who[0]}</b><p><strong>{who}</strong> {what}</p><time>{when}</time></li>'
                   for who, what, when in (("Grace", "merged #482 into main", "2m"), ("Ada", "deployed v2.4.1 to production", "14m"),
                                           ("Linus", "invited 2 members to Team", "1h"), ("Grace", "opened #483", "3h")))
    bars = "".join(f'<li><div><span>{k}</span><span>{v}%</span></div><i><i style="width:{v}%"></i></i></li>'
                   for k, v in (("Direct", 42), ("Search", 31), ("Referral", 18), ("Social", 9)))
    main = (f'<div class="sbmain"><div class="sbtop"><div><h4>Dashboard</h4><p>Acme workspace · last 7 days vs the week before</p></div>'
            f'<div class="row"><button class="btn btn-secondary btn-sm" type="button">Export</button>'
            f'<button class="btn btn-primary btn-sm" type="button">New report</button></div></div>'
            f'<div class="sbstats">{stats}</div><div class="sbgrid">'
            f'<div class="sbpanel"><h5>Recent activity</h5><ul class="sbfeed">{feed}</ul></div>'
            f'<div class="sbpanel"><h5>Traffic sources</h5><ul class="sbbars">{bars}</ul></div></div></div>')
    return f'{cap("press the panel button to collapse")}<div class="sbdemo">{nav}{main}</div>'


# (name, render, states, wide)
COMPONENTS = [
    ("Button", c_button, True),
    ("Input", c_input, False),
    ("Field", c_field, False),
    ("Fieldset", c_fieldset, False),
    ("Form", c_form, False),
    ("Select", c_select, False),
    ("RadioGroup", c_radio, False),
    ("Card", c_card, True),
    ("Badge", c_badge, False),
    ("Tabs", c_tabs, False),
    ("Modal", c_modal, True),
    ("Table", c_table, True),
    ("Sidebar", c_sidebar, True),
]
COMP_TOKENS = {"RadioGroup": "radio-group"}


def is_off(name, ptype, comp_matrix):
    return bool(ptype) and not comp_matrix.get(R.norm(name), {}).get(ptype, True)


CONTRACTS_HOWTO = (
    '<aside class="note" aria-label="How to change the defaults">'
    '<p class="note-lead"><b>Skill defaults.</b> These are ds4a&#8217;s starting contracts, not your components yet. '
    'Make them yours:</p>'
    '<ol class="note-flow">'
    '<li><span>Modify</span><code>.ds4a/project.md</code></li>'
    '<li><span>Preview</span><code>/ds4a init</code></li>'
    '<li><span>Apply</span><code>/ds4a apply</code></li></ol>'
    '<p class="note-hint">Override any token, like <code>components.button.radius</code> or <code>colors.primary</code>, '
    'switch the tone, or drop a contract with <code>exclude_components</code>.</p></aside>')


def components(tree, ptype, comp_matrix, excluded=frozenset()):
    cards, shown, hidden = [], 0, 0
    for name, render, wide in COMPONENTS:
        key = COMP_TOKENS.get(name, name.lower())
        is_ex = R.norm(name) in excluded
        off = is_off(name, ptype, comp_matrix) and not is_ex
        shown += not off and not is_ex
        hidden += is_ex
        vals = " ".join(f"{k} {v}" for k, v, _ in leaves(tree.get("components", {}).get(key)))
        classes = (" wide" if wide else "") + (" off" if off else "") + (" excluded" if is_ex else "")
        cards.append(
            f'<article class="cmp{classes}" id="c-{key}" data-title="{name}" '
            f'data-s="{esc(name)} {esc(vals)}"><header><h3 class="t-title-h6">{name}</h3></header>'
            f'<div class="demo">{render()}</div></article>')
    total = len(COMPONENTS) - hidden
    note = f" {hidden} excluded by the overlay." if hidden else ""
    if ptype and shown < total:
        bar = (f'<div class="cbar"><p>Showing {shown} of {total} contracts for <strong>{esc(ptype)}</strong> '
               f'(from <code>component-matrix.md</code>).{note}</p><button class="chipbtn" id="all" type="button" '
               f'data-on="Only {esc(ptype)}" data-off="Show all {total}">Show all {total}</button></div>')
    else:
        bar = (f'<div class="cbar"><p>{total} core contracts, styled only from <code>--c-*</code> variables.{note}</p></div>')
    return CONTRACTS_HOWTO + bar + f'<div class="cmps">{"".join(cards)}</div>'


def specimens_section(specimens):
    if not specimens:
        return ('<div class="empty"><p><b>No project specimens yet.</b></p>'
                '<p>Capture the components this project really has — beyond the core contracts:</p>'
                '<pre><code>python3 scripts/specimens.py --project . scan\n'
                'python3 scripts/specimens.py --project . add pill --from src/components/Pill.tsx</code></pre>'
                '<p>A specimen is a static copy, rendered here with the same tokens. '
                '<code>/ds4a diff</code> also proposes candidates.</p></div>')
    cards = []
    for s in specimens:
        drift = ""
        if s["status"] == "changed":
            drift = '<span class="drift">source changed since capture</span>'
        elif s["status"] == "missing":
            drift = '<span class="drift">source file missing</span>'
        contract = f'<span class="sbadge">{esc(s["contract"])}</span>' if s["contract"] else ""
        src = (f'<code>{esc(s["source"])}</code>' if s["source"] else "captured from the project")
        captured = f' · captured {esc(s["captured"])}' if s["captured"] else ""
        cards.append(
            f'<article class="spec" id="spec-{esc(s["slug"])}" data-title="{esc(s["title"])}" '
            f'data-s="specimen {esc(s["title"])} {esc(s["contract"])} {esc(s["source"])}">'
            f'<header><div class="spech"><h3 class="t-title-h6">{esc(s["title"])}</h3>{contract}</div>'
            f'<p class="prov">{src}{captured}{drift}</p></header>'
            f'<div class="specbody">{s["html"]}</div></article>')
    return (f'<div class="cbar"><p>{len(specimens)} project specimen{"s" if len(specimens) != 1 else ""}, '
            f'rendered from captured markup with the same tokens. Edit the copy in <code>.ds4a/specimens/</code>, '
            f'then rebuild.</p></div><div class="specs">{"".join(cards)}</div>')


def contracts_section(proj, ptype, comp_matrix, excluded, specimens):
    comp_body = R.split_sections(proj["doc"]).get("Components", "")
    doc_names = [re.sub(r"\s*\(grown\)\s*$", "", h) for h in re.findall(r"(?m)^### (.+?)\s*$", comp_body)]
    grown = {R.norm(h) for h in re.findall(r"(?m)^### (.+?)\s*$", comp_body) if "(grown)" in h}
    names = [n for n, *_ in COMPONENTS]
    for n in doc_names:
        if R.norm(n) not in {R.norm(x) for x in names}:
            names.append(n)
    rows = []
    for name in names:
        n = R.norm(name)
        sp = next((s for s in specimens if s["contract"] and R.norm(s["contract"]) == n), None)
        if sp and n in excluded:
            status, detail = "specimen", "Project version; core contract excluded by the overlay."
        elif sp:
            status, detail = "specimen", "Project specimen replaces the core rendering in the catalog."
        elif n in excluded:
            status, detail = "excluded", "Dropped by <code>exclude_components</code>."
        elif ptype and comp_matrix.get(n, {}).get(ptype) is False:
            status, detail = "off", "Not used by this project type (matrix)."
        elif n in grown:
            status, detail = "grown", "Grown contract, promoted through review."
        else:
            status, detail = "on", "Included from core."
        label = {"on": "Enforced", "off": "Not for type", "excluded": "Excluded",
                 "specimen": "Specimen", "grown": "Grown"}[status]
        sp_cell = f"<code>{esc(sp['title'])}</code>" if sp else "—"
        rows.append(f'<tr data-s="contract {esc(name)} {status}"><td><code>{esc(name)}</code></td>'
                    f'<td><span class="st st-{status}">{label}</span></td>'
                    f'<td>{sp_cell}</td><td>{detail}</td></tr>')
    return (f'<div class="cbar"><p>{len(rows)} contracts: what the agent is told to build, what the project replaced, '
            f'and what it explicitly dropped.</p></div>'
            f'<div class="scroll"><table class="tbl contract-tbl"><thead><tr><th>Contract</th><th>Status</th>'
            f'<th>Specimen</th><th>Detail</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


# ───────────────────────── page ─────────────────────────

def font_decl(n):
    return f"font:var(--t-{n});letter-spacing:var(--t-{n}-ls)"


TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-tone="{{default}}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{title}}</title>{{fonts}}
<style>
{{tone_css}}
{{page_css}}
</style></head>
<body><a class="skip" href="#main">Skip to content</a><div class="shell">
<aside class="side">
  <a class="brand" href="#overview"><span class="mark"><i></i><i></i><i></i><i></i></span><span><b>ds4a</b>{{brand}}</span></a>
  <nav class="snav" aria-label="Sections">{{side_nav}}</nav>
</aside>
<div class="col">
<header class="top"><div class="topin">
  <div class="crumb"><span>Design system</span><span class="sep">/</span><b id="crumb">Overview</b></div>
  <div class="tools">
    <label class="tsel"><span>Tone</span><select id="tone">{{options}}</select></label>
    <label class="srch"><input id="q" type="search" placeholder="Search tokens and components" autocomplete="off" aria-label="Search"><kbd>/</kbd></label>
  </div>
  <nav class="mnav" aria-label="Sections">{{mobile_nav}}</nav>
</div></header>
<main id="main">
{{sections}}
<p class="nomatch" role="status"></p>
<div class="toast" role="status" aria-live="polite"></div>
<footer class="pfoot">Generated from tokens by ds4a. Edit <code>.ds4a/project.md</code> or the tone, then rebuild.</footer>
</main></div></div>
<script>
{{page_js}}
</script></body></html>
"""

PAGE_CSS = re.sub(r"@t\(([\w-]+)\)", lambda m: font_decl(m.group(1)), """
*,*::before,*::after{box-sizing:border-box}
html{color-scheme:light;scroll-padding-top:80px}
body{margin:0;background:var(--color-background);color:var(--color-foreground);@t(paragraph-md);-webkit-font-smoothing:antialiased;transition:background-color var(--motion-smooth) var(--ease-out)}
[hidden]{display:none!important}
h1,h2,h3,h4,p,ul{margin:0}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px}
p code,li code{padding:1px 4px;background:var(--color-muted);border-radius:var(--radius-xs);color:var(--color-foreground)}
.skip{position:absolute;top:var(--space-lg);left:var(--space-lg);z-index:100;padding:var(--space-sm) var(--space-md);border-radius:var(--radius-sm);background:var(--color-foreground);color:var(--color-background);@t(label-sm);text-decoration:none;transform:translateY(-300%)}
.skip:focus{transform:none;outline:2px solid var(--color-primary);outline-offset:2px}
.shell{display:grid;grid-template-columns:240px minmax(0,1fr);min-height:100vh}
.side{position:sticky;top:0;height:100vh;overflow-y:auto;display:flex;flex-direction:column;gap:var(--space-xl);padding:var(--space-lg) var(--space-md) var(--space-2xl);border-right:1px solid var(--color-border);background:var(--color-background);scrollbar-width:thin}
.brand{display:flex;align-items:center;gap:var(--space-md);padding:var(--space-xs) var(--space-sm);color:inherit;text-decoration:none}
.brand b{display:block;@t(label-md)}.brand small{display:block;@t(paragraph-xs);color:var(--color-muted-foreground)}
.mark{flex:none;display:grid;grid-template-columns:1fr 1fr;width:28px;height:28px;border:1px solid var(--color-border);border-radius:var(--radius-sm);overflow:hidden}
.mark i:nth-child(1){background:var(--color-primary)}.mark i:nth-child(2){background:var(--color-foreground)}
.mark i:nth-child(3){background:var(--color-muted)}.mark i:nth-child(4){background:var(--color-background)}
.snav{position:relative;display:flex;flex-direction:column;gap:var(--space-xl)}
.navpill{position:absolute;top:0;left:0;border-radius:var(--radius-sm);background:var(--color-muted);opacity:0;pointer-events:none;transition:transform var(--motion-smooth) var(--ease-out),opacity var(--motion-fast) var(--ease-out)}
.eyebrow{@t(label-xs);color:var(--color-muted-foreground);text-transform:uppercase;letter-spacing:.06em}
.sg{display:flex;flex-direction:column;gap:1px}
.sg>.eyebrow{display:flex;align-items:center;justify-content:space-between;padding:0 var(--space-sm) var(--space-sm)}
.sg>.eyebrow span{padding:0 6px;border:1px solid var(--color-border);border-radius:var(--radius-full);font-variant-numeric:tabular-nums;letter-spacing:0;line-height:18px}
.sg a{position:relative;@t(paragraph-sm);color:var(--color-foreground);text-decoration:none;padding:6px var(--space-sm);border-radius:var(--radius-sm);transition:color var(--motion-fast) var(--ease-out)}
.sg a.on{font-weight:500}
.sgsub{display:flex;flex-direction:column;gap:1px;margin:2px 0 var(--space-xs) var(--space-md);padding-left:var(--space-xs);border-left:1px solid var(--color-border)}
.sgsub a{@t(paragraph-sm);padding:4px var(--space-sm);color:var(--color-muted-foreground)}
.sgsub a.on{color:var(--color-foreground)}
.sgsub a.on::before{content:"";position:absolute;left:calc(var(--space-xs) * -1 - 1px);top:6px;bottom:6px;width:1px;background:var(--color-foreground)}
.sg a.off{display:none}:root.all .sg a.off{display:block;opacity:.6}
.col{min-width:0;--content-max:1180px}
.top{position:sticky;top:0;z-index:10;padding:var(--space-md) var(--space-3xl);background:var(--color-background);border-bottom:1px solid var(--color-border)}
.topin{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--space-sm) var(--space-lg);width:100%;max-width:calc(var(--content-max) - 2*var(--space-3xl))}
.crumb{display:flex;align-items:center;gap:var(--space-sm);min-width:0;@t(paragraph-sm);color:var(--color-muted-foreground)}
.crumb b{font-weight:500;color:var(--color-foreground)}.sep{opacity:.5}
.tools{display:flex;align-items:center;gap:var(--space-sm)}
.tsel,.srch{position:relative;display:flex;align-items:center;height:36px;border:1px solid var(--color-border);border-radius:var(--radius-sm);background:var(--color-background);@t(paragraph-sm)}
.tsel span{padding:0 var(--space-xs) 0 var(--space-md);color:var(--color-muted-foreground)}
.tsel select{appearance:none;-webkit-appearance:none;height:100%;max-width:260px;padding:0 30px 0 var(--space-xs);border:0;background:transparent;color:var(--color-foreground);font:inherit;font-weight:500;text-overflow:ellipsis;cursor:pointer;outline:0}
.tsel::after{content:"";position:absolute;right:13px;top:50%;width:6px;height:6px;border-right:1.5px solid var(--color-muted-foreground);border-bottom:1.5px solid var(--color-muted-foreground);transform:translateY(-70%) rotate(45deg);pointer-events:none}
.srch input{width:220px;height:100%;padding:0 var(--space-md);border:0;background:transparent;color:var(--color-foreground);font:inherit;outline:0}
.srch kbd{margin-right:var(--space-sm);padding:0 6px;border:1px solid var(--color-border);border-radius:4px;font:11px/18px ui-monospace,monospace;color:var(--color-muted-foreground)}
.tsel:focus-within,.srch:focus-within{outline:2px solid var(--color-primary);outline-offset:1px}
.mnav{display:none}
main{padding:var(--space-3xl) var(--space-3xl) var(--space-2xl);max-width:var(--content-max);min-width:0}
.pfoot{padding-top:var(--space-xl);border-top:1px solid var(--color-border);@t(paragraph-xs);color:var(--color-muted-foreground)}
section{padding-bottom:var(--space-4xl)}
section+section{border-top:1px solid var(--color-border);padding-top:var(--space-3xl)}
.sec{margin:var(--space-sm) 0}
section>.eyebrow{margin:0}
.sub{max-width:64ch;margin-bottom:var(--space-2xl);color:var(--color-muted-foreground)}
.gh{@t(label-sm);color:var(--color-muted-foreground);text-transform:uppercase;letter-spacing:.06em;margin:var(--space-2xl) 0 var(--space-md)}
.tv>.gh:first-child,.grp .gh{margin-top:0}.grp+.grp{margin-top:var(--space-2xl)}
.hint{text-transform:none;letter-spacing:0;font-weight:400;margin-left:var(--space-sm)}
.row{display:flex;flex-wrap:wrap;gap:var(--space-md);align-items:center}
.cap{display:block;@t(label-xs);color:var(--color-muted-foreground);margin-bottom:var(--space-sm)}
.nomatch{color:var(--color-muted-foreground);padding:var(--space-4xl) 0}
.nomatch:empty{padding:0}
/* hero */
.hero{max-width:780px}
.hero h1{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-sm) var(--space-md);margin-bottom:var(--space-lg);overflow-wrap:anywhere}
.proj{@t(label-xs);padding:2px var(--space-sm);border:1px solid var(--color-border);border-radius:var(--radius-full);color:var(--color-muted-foreground)}
.lead{max-width:64ch;color:var(--color-muted-foreground)}
.facts{display:flex;flex-wrap:wrap;gap:var(--space-lg) var(--space-3xl);margin:var(--space-2xl) 0 0;padding-top:var(--space-lg);border-top:1px solid var(--color-border)}
.facts dt{@t(label-xs);color:var(--color-muted-foreground);margin-bottom:var(--space-xs)}
.facts dd{margin:0;@t(label-sm);display:flex;align-items:center;gap:var(--space-sm)}
.facts dd.ok::before,.facts dd.bad::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--color-primary)}
.facts dd.bad{color:var(--color-destructive)}.facts dd.bad::before{background:var(--color-destructive)}
.warns{margin-top:var(--space-md);padding-left:var(--space-lg);@t(paragraph-xs);color:var(--color-destructive)}
.ribbon{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:var(--space-md);margin-top:var(--space-3xl)}
.ribbon i{display:block;height:72px;margin-bottom:var(--space-sm);border:1px solid var(--color-border);border-radius:var(--radius-sm)}
.ribbon b{display:block;@t(label-xs);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.ribbon code{font-size:11px;color:var(--color-muted-foreground)}
/* principles */
.plead{max-width:56ch;margin-bottom:var(--space-2xl)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:var(--space-2xl) var(--space-xl)}
.pcard{padding-top:var(--space-lg);border-top:1px solid var(--color-border)}
.pn{display:block;font:12px/1 ui-monospace,monospace;color:var(--color-muted-foreground);margin-bottom:var(--space-md)}
.pcard b{display:block;@t(label-md);margin-bottom:var(--space-sm)}
.pcard p{@t(paragraph-sm);color:var(--color-muted-foreground)}
.pcore{margin-top:var(--space-2xl);@t(paragraph-sm);color:var(--color-muted-foreground);max-width:72ch}
/* color */
.sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,200px),1fr));gap:var(--space-lg)}
.sw{border:1px solid var(--color-border);border-radius:var(--radius-lg);overflow:hidden}
.chip{height:112px;border-bottom:1px solid var(--color-border)}
.swb{padding:var(--space-md) var(--space-lg) var(--space-lg);display:flex;flex-direction:column;align-items:flex-start;gap:var(--space-xs)}
.swb b{@t(label-sm)}.swb p,.vs{@t(paragraph-xs);color:var(--color-muted-foreground)}
.cr{@t(label-xs);padding:2px var(--space-sm);border-radius:var(--radius-full);background:var(--color-muted);margin-top:var(--space-xs)}
.cr.bad{color:var(--color-primary-foreground);background:var(--color-destructive)}
/* typography */
.fams{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,380px),1fr));gap:var(--space-lg);margin-bottom:var(--space-lg)}
.fam{display:flex;gap:var(--space-xl);padding:var(--space-xl);border:1px solid var(--color-border);border-radius:var(--radius-lg);min-width:0}
.fam .aa{font-size:72px;line-height:1;flex:none}
.fam b{@t(label-md)}.fam p{@t(paragraph-xs);color:var(--color-muted-foreground);margin-top:var(--space-xs)}
.fam .abc{@t(paragraph-sm);color:var(--color-foreground);margin-top:var(--space-md);overflow-wrap:anywhere}
.trow{display:grid;grid-template-columns:200px minmax(0,1fr);gap:var(--space-xl);align-items:baseline;padding:var(--space-md) 0;border-bottom:1px solid var(--color-border)}
.tmeta code{display:block;font-size:13px;color:var(--color-foreground)}
.tmeta span{@t(paragraph-xs);color:var(--color-muted-foreground)}
.tsample{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* spacing, radius, elevation */
.srow{display:grid;grid-template-columns:56px 64px minmax(0,1fr) auto;gap:var(--space-lg);align-items:center;padding:var(--space-xs) 0}
.srow code{color:var(--color-foreground);font-size:13px}.srow span{@t(paragraph-xs);color:var(--color-muted-foreground)}
.bar{height:16px;max-width:100%;background:var(--color-primary);border-radius:var(--radius-xs)}
.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,150px),1fr));gap:var(--space-lg)}
.rad{display:flex;flex-direction:column;gap:var(--space-lg);padding:var(--space-lg);border:1px solid var(--color-border);border-radius:var(--radius-md)}
/* one stroked corner per step: the curve is the token, nothing else is drawn */
.rshape{width:64px;height:64px;border-top:2px solid var(--color-foreground);border-left:2px solid var(--color-foreground)}
.rmeta{display:flex;align-items:center;justify-content:space-between;gap:var(--space-sm)}
.rmeta code{display:block;color:var(--color-foreground);font-size:13px}.rmeta span{@t(paragraph-xs);color:var(--color-muted-foreground)}
.egrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr));gap:var(--space-2xl);padding:var(--space-2xl);background:var(--color-muted);border-radius:var(--radius-lg)}
.sh{min-height:140px;padding:var(--space-lg);background:var(--color-background);border-radius:var(--radius-md);display:flex;flex-direction:column;justify-content:center;gap:var(--space-xs)}
.sh b{@t(label-md)}.sh code{color:var(--color-muted-foreground);overflow-wrap:anywhere}.sh span{@t(paragraph-xs);color:var(--color-muted-foreground)}
.mlist{display:flex;flex-direction:column}
.mrow{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:var(--space-xl);align-items:center;padding:var(--space-md) 0;border-bottom:1px solid var(--color-border)}
.mrow code{font-size:13px;margin-right:var(--space-sm)}.mrow span,.mrow p{@t(paragraph-xs);color:var(--color-muted-foreground)}
.track{position:relative;height:28px;width:260px;max-width:100%;background:var(--color-muted);border-radius:var(--radius-full)}
.track i{position:absolute;left:4px;top:4px;width:20px;height:20px;border-radius:var(--radius-full);background:var(--color-primary);transition:transform var(--d) var(--e)}
.raw{border:1px solid var(--color-border);border-radius:var(--radius-lg);overflow:hidden}
.raw summary{cursor:pointer;padding:var(--space-lg) var(--space-xl);@t(label-sm)}
.raw pre{margin:0;padding:var(--space-xl);background:var(--color-muted);overflow:auto;max-height:640px;line-height:1.6}
.rawcopy{margin-top:var(--space-md)}
/* component cards */
.note{display:flex;flex-direction:column;align-items:flex-start;gap:var(--space-md);margin-bottom:var(--space-2xl);padding:var(--space-lg) var(--space-xl);border-radius:var(--radius-lg);background:var(--color-muted)}
.note-lead{@t(paragraph-md);color:var(--color-foreground)}.note-lead b{font-weight:600}
.note-flow{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-sm) var(--space-2xl);margin:0;padding:0;list-style:none}
.note-flow li{position:relative;display:inline-flex;align-items:center;gap:var(--space-sm);padding:3px var(--space-md) 3px 3px;border:1px solid var(--color-border);border-radius:var(--radius-full);background:var(--color-background)}
.note-flow li+li::before{content:"";position:absolute;right:100%;top:50%;width:calc(var(--space-2xl) - 8px);margin-right:4px;border-top:1px dashed var(--color-muted-foreground);opacity:.6}
.note-flow span{padding:0 var(--space-sm);border-radius:var(--radius-full);background:var(--color-foreground);color:var(--color-background);@t(label-xs);line-height:20px}
.note-flow code{padding:0;background:none;font-size:12px;color:var(--color-foreground)}
.note-hint{@t(paragraph-sm);color:var(--color-muted-foreground)}
.note-hint code{font-size:.92em}
.cbar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--space-md);margin-bottom:var(--space-xl);color:var(--color-muted-foreground);@t(paragraph-sm)}
.chipbtn{@t(label-xs);padding:var(--space-xs) var(--space-md);border:1px solid var(--color-border);border-radius:var(--radius-full);background:var(--color-background);color:var(--color-foreground);cursor:pointer}
:root.all .chipbtn{background:var(--color-foreground);color:var(--color-background)}
.cmps{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:var(--space-xl);align-items:stretch}
.cmp{border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:var(--space-xl);min-width:0}
.cmp.wide{grid-column:1/-1}
.cmp.off{display:none}:root.all .cmp.off{display:block}
.cmp.excluded{display:none!important}
.cmp>header{margin-bottom:var(--space-xl)}
.demo{display:flex;flex-direction:column;gap:var(--space-lg)}
/* project specimens */
.specs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:var(--space-xl);align-items:start}
.spec{border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:var(--space-xl);min-width:0}
.spec>header{margin-bottom:var(--space-lg)}
.spech{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-sm)}
.sbadge{@t(label-xs);padding:2px var(--space-sm);border:1px solid var(--color-border);border-radius:var(--radius-full);color:var(--color-muted-foreground)}
.prov{margin-top:var(--space-xs);@t(paragraph-xs);color:var(--color-muted-foreground);overflow-wrap:anywhere}
.prov code{font-size:11px}
.drift{display:inline-block;margin-left:var(--space-sm);padding:1px var(--space-sm);border-radius:var(--radius-full);background:var(--color-destructive);color:var(--color-primary-foreground);@t(label-xs)}
.specbody{display:flex;flex-direction:column;gap:var(--space-md);min-width:0}
.empty{border:1px dashed var(--color-border);border-radius:var(--radius-lg);padding:var(--space-2xl);color:var(--color-muted-foreground);max-width:72ch}
.empty p+p{margin-top:var(--space-sm)}
.empty pre{margin:var(--space-md) 0;padding:var(--space-md);background:var(--color-muted);border-radius:var(--radius-sm);overflow:auto}
/* copy */
.cp{flex:none;display:inline-flex;align-items:center;justify-content:center;gap:var(--space-xs);vertical-align:middle;min-width:24px;height:24px;margin-left:var(--space-xs);padding:0;border:0;border-radius:var(--radius-sm);background:transparent;color:var(--color-muted-foreground);cursor:pointer;transition:background-color var(--motion-fast) var(--ease-out),color var(--motion-fast) var(--ease-out)}
.cp::before{content:"";flex:none;width:14px;height:14px;background:currentColor;-webkit-mask:@icon(copy) center/contain no-repeat;mask:@icon(copy) center/contain no-repeat}
.cp.done::before{-webkit-mask-image:@icon(done);mask-image:@icon(done);animation:cpdone var(--motion-smooth) var(--ease-out)}
@keyframes cpdone{from{transform:scale(.5);opacity:0}}
.cp:hover,.cp:focus-visible,.cp.done{background:var(--color-muted);color:var(--color-foreground)}
.cpt{padding:0 var(--space-sm);margin:0;border:1px solid var(--color-border);@t(label-xs)}
.valrow{display:flex;align-items:center;gap:var(--space-xs);min-width:0}
.valrow code{overflow-wrap:anywhere}
.tmeta .cp{float:right}
/* contract matrix */
.contract-tbl td:last-child{white-space:normal;min-width:240px;color:var(--color-muted-foreground)}
.st{display:inline-flex;align-items:center;padding:2px var(--space-sm);border-radius:var(--radius-full);@t(label-xs);white-space:nowrap}
.st-on{background:var(--color-muted);color:var(--color-foreground)}
.st-specimen{background:var(--color-primary);color:var(--color-primary-foreground)}
.st-excluded{background:var(--color-destructive);color:var(--color-primary-foreground)}
.st-grown{background:var(--color-foreground);color:var(--color-background)}
.st-off{background:transparent;border:1px solid var(--color-border);color:var(--color-muted-foreground)}
.toast{position:fixed;left:50%;bottom:var(--space-2xl);transform:translate(-50%,12px);z-index:50;padding:var(--space-sm) var(--space-lg);border-radius:var(--radius-full);background:var(--color-foreground);color:var(--color-background);@t(label-sm);opacity:0;pointer-events:none;transition:opacity var(--motion-fast) var(--ease-out),transform var(--motion-fast) var(--ease-out)}
.toast.show{opacity:1;transform:translate(-50%,0)}
.g2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:var(--space-lg);align-items:start}
.g3{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,130px),1fr));gap:var(--space-lg);align-items:start}
.scroll{overflow-x:auto;margin:0 calc(var(--space-xs) * -1);padding:var(--space-xs)}
.ic{flex:none}
/* Button */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--c-button-gap);padding:var(--c-button-padding-md);border:1px solid transparent;border-radius:var(--c-button-radius);@t(label-md);font-size:var(--c-button-font-size-md);font-weight:var(--c-button-font-weight);white-space:nowrap;cursor:pointer;transition:background-color var(--motion-fast) var(--ease-out),border-color var(--motion-fast) var(--ease-out),filter var(--motion-fast) var(--ease-out)}
.btn-sm{padding:var(--c-button-padding-sm);font-size:var(--c-button-font-size-sm)}
.btn-lg{padding:var(--c-button-padding-lg);font-size:var(--c-button-font-size-lg)}
.btn-icon{padding:var(--space-sm)}
.btn-primary{background:var(--color-primary);color:var(--color-primary-foreground)}
.btn-secondary{background:var(--color-muted);color:var(--color-foreground)}
.btn-ghost{background:transparent;color:var(--color-foreground)}
.btn-destructive{background:var(--color-destructive);color:var(--color-primary-foreground)}
.btn-primary.is-hover,.btn-destructive.is-hover{filter:brightness(.9)}
.btn-secondary.is-hover{background:var(--color-border)}
.btn-ghost.is-hover{border-color:var(--color-border)}
.btn:disabled,.inp:disabled,.is-disabled,.sbi.dis{opacity:.5;cursor:not-allowed;pointer-events:none}
.is-focus,.btn:focus-visible,.inp:focus-visible,.sel:focus-visible,.tab:focus-visible,.sbi:focus-visible,.chipbtn:focus-visible,.sg a:focus-visible,.mnav a:focus-visible,.radio input:focus-visible,.rcard input:focus-visible{outline:2px solid var(--color-primary);outline-offset:2px}
.blk{display:flex;flex-direction:column;gap:var(--space-md);min-width:0}
.blk+.blk{border-top:1px solid var(--color-border);padding-top:var(--space-lg)}
.blkh{@t(label-sm);color:var(--color-foreground)}
.mx{display:grid;grid-template-columns:minmax(96px,auto) repeat(4,minmax(max-content,1fr));min-width:560px}
.mx>*{display:flex;align-items:center;padding:var(--space-sm) var(--space-md);border-top:1px solid var(--color-border)}
.mx>:nth-child(5n+1){padding-left:0}
.mx>.mh{border-top:0;padding-top:0}
.mx .cap{margin:0}
.bsizes{display:flex;flex-wrap:wrap;align-items:flex-end;gap:var(--space-xl) var(--space-2xl)}
.bsizes figure{margin:0;display:flex;flex-direction:column;align-items:flex-start;gap:var(--space-sm)}
.bsizes .cap{margin:0}
/* Input, Field, Fieldset, Form */
.inp{display:block;width:100%;padding:var(--c-input-padding-md);border:var(--c-input-border);border-radius:var(--c-input-radius);@t(paragraph-md);font-size:var(--c-input-font-size-md);font-weight:var(--c-input-font-weight);background:var(--color-background);color:var(--color-foreground);transition:border-color var(--motion-fast) var(--ease-out)}
.inp::placeholder{color:var(--color-muted-foreground)}
.inp.err,[data-invalid] .inp{border-color:var(--color-destructive)}
.inp.err.is-focus,.inp.err:focus-visible,[data-invalid] .inp:focus-visible{outline-color:var(--color-destructive)}
.field{display:flex;flex-direction:column;gap:var(--c-field-gap)}
.field>label{@t(label-sm);font-size:var(--c-field-label-font-size);font-weight:var(--c-field-label-font-weight)}
.fdesc{@t(paragraph-sm);font-size:var(--c-field-description-font-size);color:var(--c-field-description-color)}
.ferr{@t(paragraph-sm);font-size:var(--c-field-error-font-size);color:var(--c-field-error-color)}
.fs{border:0;padding:0;margin:0;min-width:0;display:flex;flex-direction:column;gap:var(--c-fieldset-gap)}
.fs legend{@t(label-md);font-size:var(--c-fieldset-legend-font-size);font-weight:var(--c-fieldset-legend-font-weight);padding:0;margin-bottom:var(--c-fieldset-gap)}
.fs:disabled{opacity:.5}
.form{display:flex;flex-direction:column;gap:var(--c-form-gap);max-width:400px}
/* Select */
.sel{display:flex;align-items:center;justify-content:space-between;gap:var(--space-sm);width:100%;padding:var(--c-select-padding);border:var(--c-input-border);border-radius:var(--c-select-radius);@t(paragraph-md);font-size:var(--c-select-font-size);font-weight:var(--c-select-font-weight);background:var(--color-background);color:var(--color-foreground);text-align:left;cursor:pointer}
.sel .chev{transition:transform var(--motion-fast) var(--ease-out)}
.sel.open .chev{transform:rotate(var(--c-select-icon-rotation))}
.selw{position:relative}
#c-select .g2{min-height:260px}
.pop{position:absolute;top:100%;left:0;right:0;z-index:5;transform-origin:top;transition:opacity var(--motion-smooth) var(--ease-in-out),transform var(--motion-smooth) var(--ease-in-out),visibility 0s;margin-top:var(--space-xs);padding:var(--c-select-popup-padding);border-radius:var(--c-select-popup-radius);box-shadow:var(--shadow-elevated);background:var(--color-background);max-height:var(--c-select-popup-max-height);overflow:auto;display:flex;flex-direction:column;gap:2px}
.opt{position:relative;display:flex;align-items:center;justify-content:space-between;padding:var(--space-sm) var(--space-md);border-radius:max(0px,calc(var(--c-select-popup-radius) - var(--c-select-popup-padding)));@t(paragraph-md);font-size:var(--c-select-font-size);cursor:pointer}
.pop.closed{opacity:0;transform:translateY(-4px) scale(.98);visibility:hidden;pointer-events:none;transition:opacity var(--motion-smooth) var(--ease-in-out),transform var(--motion-smooth) var(--ease-in-out),visibility 0s linear var(--motion-smooth)}
.pop:not(.js) .opt.hl{background:var(--color-muted)}
/* one shared highlight that glides to the active option (transform only) */
.flow{position:absolute;top:0;left:var(--c-select-popup-padding);right:var(--c-select-popup-padding);border-radius:max(0px,calc(var(--c-select-popup-radius) - var(--c-select-popup-padding)));background:var(--color-muted);opacity:0;pointer-events:none;transition:transform var(--motion-smooth) var(--ease-out),opacity var(--motion-fast) var(--ease-out)}
.flow.on{opacity:1}
.opt.selected{font-weight:500}
.opt.selected::after{content:"";width:6px;height:6px;border-radius:50%;background:var(--color-primary)}
.opt.dis{opacity:.5;cursor:not-allowed;pointer-events:none}
/* RadioGroup */
.rg{display:flex;flex-direction:column;gap:var(--c-radio-group-gap)}
.radio{display:flex;align-items:center;gap:var(--space-sm);@t(paragraph-md);cursor:pointer}
.radio input,.rcard input{appearance:none;-webkit-appearance:none;margin:0;flex:none;width:16px;height:16px;border:2px solid var(--color-muted-foreground);border-radius:50%;display:grid;place-content:center;cursor:pointer;transition:border-color var(--motion-fast) var(--ease-out)}
.rcard input{width:18px;height:18px;margin-top:2px}
.radio input::before,.rcard input::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--color-primary);transform:scale(0);transition:transform var(--motion-fast) var(--ease-out)}
.radio input:checked,.rcard input:checked{border-color:var(--color-primary)}
.radio input:checked::before,.rcard input:checked::before{transform:scale(1)}
.rcard{display:flex;align-items:flex-start;gap:var(--c-radio-group-radio-card-gap);padding:var(--c-radio-group-radio-card-padding);border:1px solid var(--color-border);border-radius:var(--radius-md);cursor:pointer;transition:border-color var(--motion-fast) var(--ease-out)}
.rcard:has(input:checked){border-color:var(--color-primary)}
.rcard:has(input:checked){background:var(--c-radio-group-checked-background)}
.rcard b{display:block;@t(label-md)}.rcard span{@t(paragraph-sm);color:var(--color-muted-foreground)}
.rcard:has(input:checked) span{color:var(--color-foreground)}
/* Card, Badge */
.card{background:var(--color-background);border:var(--c-card-border);border-radius:var(--c-card-radius);padding:var(--c-card-padding);box-shadow:var(--shadow-subtle)}
.card.elev{box-shadow:var(--shadow-elevated)}
.card.flush{padding:0;overflow:hidden}
.card .media{height:96px;background:var(--color-muted)}.card .fb{padding:var(--space-lg)}
.card h4{@t(title-h6);margin-bottom:var(--space-xs)}.card p{@t(paragraph-sm);color:var(--color-muted-foreground)}
.badge{display:inline-flex;align-items:center;gap:var(--c-badge-gap);padding:var(--c-badge-padding);border:1px solid transparent;border-radius:var(--c-badge-radius);@t(label-xs);font-size:var(--c-badge-font-size);font-weight:var(--c-badge-font-weight);white-space:nowrap;vertical-align:middle}
.badge-default{background:var(--color-muted);color:var(--color-foreground);border-color:var(--color-border)}
.badge-primary{background:var(--color-primary);color:var(--color-primary-foreground)}
.badge-destructive{background:var(--color-destructive);color:var(--color-primary-foreground)}
.inline{@t(paragraph-md)}
/* Modal */
.stage{position:relative;display:grid;place-items:center;min-height:360px;padding:var(--space-3xl) var(--space-lg);background:var(--color-muted);border-radius:var(--radius-md);overflow:hidden}
.ghostpage{position:absolute;inset:var(--space-xl);display:flex;flex-direction:column;gap:var(--space-md)}
.ghostpage i{display:block;height:14px;border-radius:var(--radius-xs);background:var(--color-border)}
.backdrop{position:absolute;inset:0;background:var(--c-modal-backdrop)}
.modal{position:relative;width:min(100%,var(--c-modal-width-md));display:flex;flex-direction:column;gap:var(--space-lg);padding:var(--c-modal-padding);background:var(--color-background);border-radius:var(--c-modal-radius);box-shadow:var(--c-modal-shadow)}
.mh{display:flex;align-items:center;justify-content:space-between;gap:var(--c-modal-header-gap)}.mh h4{@t(title-h6)}
.mb{@t(paragraph-md);color:var(--color-muted-foreground)}
.mf{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:var(--c-modal-footer-gap)}
/* Tabs */
.tl{display:flex;gap:var(--space-xs);border-bottom:var(--c-tabs-list-border);overflow-x:auto;overflow-y:hidden;scrollbar-width:none}
.tab{position:relative;margin-bottom:-1px;padding:var(--c-tabs-trigger-padding);border:0;border-radius:var(--c-tabs-radius) var(--c-tabs-radius) 0 0;background:none;@t(label-md);font-size:var(--c-tabs-trigger-font-size);font-weight:var(--c-tabs-trigger-font-weight);color:var(--color-muted-foreground);white-space:nowrap;cursor:pointer;transition:color var(--motion-fast) var(--ease-out)}
.tab[aria-selected=true]{color:var(--color-foreground)}
.tab::after{content:"";position:absolute;left:0;right:0;bottom:0;height:var(--c-tabs-indicator-height);background:var(--c-tabs-indicator-color);transform:scaleX(0);transition:transform var(--motion-smooth) var(--ease-out)}
.tab[aria-selected=true]::after{transform:scaleX(1)}
.tab:focus-visible{outline-offset:-2px}
.tab:disabled{opacity:.5;cursor:not-allowed}
.tp{padding-top:var(--space-lg);@t(paragraph-sm);color:var(--color-muted-foreground)}
/* Table */
.tbl{width:100%;border-collapse:collapse}
.tbl th{text-align:left;@t(label-sm);font-size:var(--c-table-header-font-size);font-weight:var(--c-table-header-font-weight);color:var(--c-table-header-color)}
.tbl td{@t(paragraph-sm);font-size:var(--c-table-cell-font-size);font-weight:var(--c-table-cell-font-weight)}
.tbl th,.tbl td{padding:var(--c-table-row-padding);border-bottom:var(--c-table-row-border);white-space:nowrap}
.tbl tbody tr{transition:background-color var(--motion-fast) var(--ease-out)}
.tbl tr.selected{background:var(--c-table-selected-background)}
.tbl .num{text-align:right;font-variant-numeric:tabular-nums}
.tbl th .ic{vertical-align:middle}
.tbl .ck{width:16px}.ck input{display:block;width:16px;height:16px;margin:0;accent-color:var(--color-primary)}
/* Sidebar */
.sbdemo{display:flex;border:1px solid var(--color-border);border-radius:var(--radius-md);overflow:hidden}
.sb{flex:none;width:var(--c-sidebar-width);max-width:70%;display:flex;flex-direction:column;gap:var(--space-lg);padding:0 var(--space-sm) var(--space-sm);border-right:var(--c-sidebar-container-border);background:var(--color-background);overflow:hidden;transition:width var(--motion-smooth) var(--ease-in-out)}
.sbh{display:flex;align-items:center;gap:var(--space-sm);padding:var(--space-lg) var(--space-sm);@t(label-md)}
.sbh i{flex:none;width:24px;height:24px;border-radius:var(--radius-sm);background:var(--color-primary)}
.sbs{display:flex;flex-direction:column;gap:2px}
.sbsh{padding:var(--c-sidebar-section-header-padding);@t(label-xs);font-size:var(--c-sidebar-section-header-font-size);color:var(--color-muted-foreground);text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.sbi{display:flex;align-items:center;gap:var(--c-sidebar-item-gap);padding:var(--c-sidebar-item-padding);border-left:var(--c-sidebar-active-indicator);border-left-color:transparent;border-radius:var(--c-sidebar-radius);@t(label-sm);font-size:var(--c-sidebar-item-font-size);font-weight:var(--c-sidebar-item-font-weight);color:var(--color-foreground);text-decoration:none;white-space:nowrap;transition:background-color var(--motion-fast) var(--ease-out)}
.sbi.active{background:var(--color-muted);border-left:var(--c-sidebar-active-indicator)}
.sbf{margin:auto calc(var(--space-sm) * -1) 0;display:flex;align-items:center;gap:var(--space-sm);padding:var(--space-sm) var(--space-sm) 0 var(--space-md);border-top:1px solid var(--color-border)}
.sbu{flex:1;min-width:0;display:flex;align-items:center;gap:var(--space-sm)}
.sbu b{flex:none;display:grid;place-items:center;width:28px;height:28px;border-radius:var(--radius-full);background:var(--color-muted);@t(label-xs);color:var(--color-foreground)}
.sbu .lbl{display:flex;flex-direction:column;min-width:0;@t(label-sm)}
.sbu .lbl>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sbu small{@t(label-xs);color:var(--color-muted-foreground)}
.sb.mini{width:var(--space-4xl)}
.sb.mini .lbl,.sb.mini .sbsh{display:none}
.sb.mini .sbi,.sb.mini .sbh{justify-content:center}
.sb.mini .sbf{flex-direction:column;padding-inline:0}.sb.mini .sbu{flex:none}
.sbmain{flex:1;min-width:0;display:flex;flex-direction:column;gap:var(--space-xl);padding:var(--space-xl);background:var(--color-background)}
.sbtop{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--space-md)}
.sbtop h4{margin:0;@t(title-h6)}.sbtop p{@t(paragraph-sm);color:var(--color-muted-foreground)}
.sbtop .row{gap:var(--space-sm)}
.sbn{margin-left:auto}.sb.mini .sbn{display:none}
.sbstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));gap:var(--space-md)}
.sbst{display:flex;flex-direction:column;gap:var(--space-xs);padding:var(--space-lg);border:var(--c-card-border);border-radius:var(--c-card-radius)}
.sbst>span{@t(label-xs);color:var(--color-muted-foreground)}.sbst b{@t(title-h4)}
.sbdelta{display:flex;align-items:flex-end;justify-content:space-between;gap:var(--space-sm)}
.sbdelta em{min-width:0;font-style:normal;@t(label-xs);color:var(--color-foreground);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.spark{flex:none;width:56px;height:24px;overflow:visible}
.spark polyline{fill:none;stroke:var(--color-secondary);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.sbgrid{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:var(--space-md)}
@media (max-width:1100px){.sbgrid{grid-template-columns:minmax(0,1fr)}}
.sbpanel{display:flex;flex-direction:column;gap:var(--space-sm);padding:var(--space-lg);border:var(--c-card-border);border-radius:var(--c-card-radius)}
.sbpanel h5{margin:0;@t(label-sm)}
.sbfeed,.sbbars{list-style:none;margin:0;padding:0}
.sbfeed li{display:flex;align-items:center;gap:var(--space-sm);padding:var(--space-sm) 0;@t(paragraph-sm)}
.sbfeed li+li{border-top:1px solid var(--color-border)}
.sbfeed b{flex:none;display:grid;place-items:center;width:24px;height:24px;border-radius:var(--radius-full);background:var(--color-muted);@t(label-xs)}
.sbfeed p{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--color-muted-foreground)}
.sbfeed strong{font-weight:500;color:var(--color-foreground)}
.sbfeed time{@t(label-xs);color:var(--color-muted-foreground);white-space:nowrap}
.sbbars{display:flex;flex-direction:column;gap:var(--space-md);padding-top:var(--space-xs)}
.sbbars div{display:flex;justify-content:space-between;@t(paragraph-sm)}.sbbars div span+span{color:var(--color-muted-foreground);font-variant-numeric:tabular-nums}
.sbbars li>i{display:block;height:6px;margin-top:var(--space-xs);border-radius:var(--radius-full);background:var(--color-muted);overflow:hidden}
.sbbars li>i>i{display:block;height:100%;border-radius:inherit;background:var(--color-secondary)}
:root.switching *,:root.switching *::before,:root.switching *::after{transition:none!important}
@media (hover:hover){
  .sgsub a:hover{color:var(--color-foreground)}
  .btn-primary:hover,.btn-destructive:hover{filter:brightness(.9)}
  .btn-secondary:hover{background:var(--color-border)}
  .btn-ghost:hover{border-color:var(--color-border)}
  .pop:not(.js) .opt:hover{background:var(--color-muted)}
  .radio:hover input,.rcard:hover input{border-color:var(--color-primary)}
  .rcard:hover{border-color:var(--color-primary)}
  .tab:hover{color:var(--color-foreground)}
  .tbl tbody tr:hover{background:var(--c-table-hover-background)}
  .sbi:hover{background:var(--color-muted)}
  .mrow:hover .track i{transform:translateX(228px)}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition-duration:0s!important;transition-delay:0s!important;animation-duration:0s!important}
}
@media (max-width:900px){
  .shell{display:block}
  .side,.crumb,.srch kbd{display:none}
  .top{padding:var(--space-sm) var(--space-lg)}
  .tools{width:100%}
  .tsel,.srch{flex:1;min-width:0}.tsel select{max-width:none;width:100%}.srch input{width:100%}
  .mnav{position:relative;display:flex;width:100%;gap:2px;overflow-x:auto;scrollbar-width:none}
  .mnav a{position:relative;@t(label-sm);white-space:nowrap;color:var(--color-muted-foreground);text-decoration:none;padding:var(--space-xs) var(--space-sm);border-radius:var(--radius-sm);transition:color var(--motion-fast) var(--ease-out)}
  .mnav a.on{color:var(--color-foreground)}
  main{padding:var(--space-2xl) var(--space-lg)}
  html{scroll-padding-top:120px}
  .ribbon{grid-template-columns:repeat(4,minmax(0,1fr))}
  .trow{grid-template-columns:1fr;gap:var(--space-xs)}
  .mrow{grid-template-columns:1fr;gap:var(--space-sm)}
  .cmp{padding:var(--space-lg)}
}
@media (max-width:600px){
  .ribbon{grid-template-columns:repeat(2,minmax(0,1fr))}
  .tsample{white-space:normal;overflow:visible;text-overflow:clip}
}
@media (max-width:470px){
  .g3>:last-child{grid-column:1/-1}
}

""").strip()
PAGE_CSS = re.sub(r"@icon\((\w+)\)", lambda m: icon_url(m.group(1)), PAGE_CSS)

PAGE_JS = """
(() => {
  const root = document.documentElement, $ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');

  // Motion tokens as JS: scrolling uses duration.smooth + ease.out like everything else.
  const token = n => getComputedStyle(root).getPropertyValue(n).trim();
  function easing(n) {
    const named = { ease: [.25, .1, .25, 1], 'ease-in': [.42, 0, 1, 1], 'ease-out': [0, 0, .58, 1],
                    'ease-in-out': [.42, 0, .58, 1], linear: [0, 0, 1, 1] };
    const v = token(n), m = v.match(/cubic-bezier\\(([^)]+)\\)/);
    const [x1, y1, x2, y2] = m ? m[1].split(',').map(Number) : named[v] || named.ease;
    const B = (t, a, b) => 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3;
    return x => {  // solve B(t) = x for t by bisection, then return the y at t
      let lo = 0, hi = 1, t = x;
      for (let i = 0; i < 24; i++) { t = (lo + hi) / 2; if (B(t, x1, x2) < x) lo = t; else hi = t; }
      return B(t, y1, y2);
    };
  }
  const runs = new WeakMap();
  function tween(key, from, to, set) {
    const id = {}; runs.set(key, id);
    const v = token('--motion-smooth'), d = v.endsWith('ms') ? parseFloat(v) : parseFloat(v) * 1000;
    if (reduced.matches || !(d > 0) || from === to) return set(to);
    const ease = easing('--ease-out'), t0 = performance.now();
    const step = now => {
      if (runs.get(key) !== id) return;  // a newer tween on the same target wins
      const k = Math.min(1, (now - t0) / d);
      set(from + (to - from) * ease(k));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]'), el = a && document.getElementById(a.hash.slice(1));
    if (!el || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    const pad = parseFloat(getComputedStyle(root).scrollPaddingTop) || 0;
    const max = root.scrollHeight - innerHeight;
    tween(window, scrollY, Math.min(max, Math.max(0, el.getBoundingClientRect().top + scrollY - pad)), y => scrollTo(0, y));
    history.replaceState(null, '', a.hash);
  });
  const tone = document.getElementById('tone'), q = document.getElementById('q');
  tone.addEventListener('change', () => {
    // Suppress transitions for the theme swap, then restore them next frame.
    root.classList.add('switching');
    root.dataset.tone = tone.value;
    void root.offsetWidth;
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('switching')));
    filter();
  });

  // Nav: highlight the section (and component card) in view; mirror it in the breadcrumb.
  const navLinks = $('.snav a, .mnav a'), crumb = document.getElementById('crumb');

  // Nav pill: one highlight per nav (sidebar, mobile bar) that glides to the hovered link
  // and rests on the active one. Only keyboard focus pins it; a mouse click must not.
  function glider(nav) {
    const hl = document.createElement('span');
    hl.className = 'navpill'; nav.prepend(hl);
    const g = {
      hovering: false,
      glide(a) {
        if (!a || !a.getClientRects().length) { hl.style.opacity = 0; return; }
        const jump = hl.style.opacity !== '1';  // appear in place instead of sliding in from the corner
        // Only transform and opacity animate (core: never animate layout); the size snaps.
        if (jump) hl.style.transition = 'none';
        hl.style.transform = `translate(${a.offsetLeft}px, ${a.offsetTop}px)`;
        hl.style.width = a.offsetWidth + 'px'; hl.style.height = a.offsetHeight + 'px';
        if (jump) { hl.getBoundingClientRect(); hl.style.transition = ''; }
        hl.style.opacity = 1;
      },
      rest() {
        if (g.hovering || nav.querySelector(':focus-visible')) return;
        const on = nav.querySelectorAll('a.on'); g.glide(on[on.length - 1]);
      },
    };
    nav.addEventListener('pointerover', e => {
      const a = e.target.closest('a');
      if (a && e.pointerType === 'mouse') { g.hovering = true; g.glide(a); }
    });
    nav.addEventListener('pointerleave', () => { g.hovering = false; g.rest(); });
    nav.addEventListener('focusin', e => { if (e.target.matches(':focus-visible')) g.glide(e.target); });
    nav.addEventListener('focusout', () => setTimeout(g.rest));
    return g;
  }
  const navs = $('.snav, .mnav').map(glider);
  const rest = () => navs.forEach(g => g.rest());
  addEventListener('resize', rest);
  const targets = $('main section[id], main .cmp[id], main .spec[id]'), topBar = document.querySelector('.top');
  let queued = false;
  function spy() {
    queued = false;
    let sec = null, cmp = null;
    const line = topBar.offsetHeight + 40;  // just below the sticky bar, which is taller on mobile
    for (const t of targets) {
      if (!t.getClientRects().length || t.getBoundingClientRect().top > line) continue;
      if (t.tagName === 'SECTION') sec = t; else cmp = t;
    }
    const shown = $('main section:not([hidden])');
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 2) sec = shown[shown.length - 1];  // short last section
    sec = sec || shown[0];
    if (!sec || (sec.id !== 'components' && sec.id !== 'specimens')) cmp = null;
    else if (!cmp) cmp = $('.cmp, .spec', sec).find(c => c.getClientRects().length) || null;
    const on = new Set([sec && sec.id, cmp && cmp.id]);
    navLinks.forEach(a => a.classList.toggle('on', on.has(a.hash.slice(1))));
    rest();
    if (sec) crumb.textContent = cmp ? sec.dataset.title + ' / ' + cmp.dataset.title : sec.dataset.title;
    // Mobile bar: keep the active link centred, scrolling smoothly when it changes.
    const m = document.querySelector('.mnav a.on');
    if (m && m !== lastMobile && m.getClientRects().length) {
      lastMobile = m;
      const bar = m.parentNode;
      const left = Math.min(bar.scrollWidth - bar.clientWidth, Math.max(0, m.offsetLeft - (bar.clientWidth - m.offsetWidth) / 2));
      tween(bar, bar.scrollLeft, left, x => { bar.scrollLeft = x; });
    }
  }
  let lastMobile = null;
  addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(spy); } }, { passive: true });
  addEventListener('keydown', e => {
    const typing = /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName);
    if (e.key === '/' && !typing) { e.preventDefault(); q.focus(); }
    if (e.key === 'Escape' && document.activeElement === q) { q.value = ''; filter(); q.blur(); }
  });

  // Search: hide swatches, type rows and cards whose text and token names miss the query.
  function filter() {
    const t = q.value.trim().toLowerCase();
    $('[data-s]').forEach(el => { el.hidden = !!t && !(el.dataset.s + ' ' + el.textContent).toLowerCase().includes(t); });
    $('main section').forEach(s => { s.hidden = false; });
    $('.grp').forEach(g => { g.hidden = !!t && !$('[data-s]', g).some(i => !i.hidden); });
    $('main section').forEach(s => { s.hidden = !!t && !$('[data-s]', s).some(i => i.getClientRects().length); });
    const any = $('main section').some(s => !s.hidden);
    document.querySelector('.nomatch').textContent = t && !any
      ? `No tokens or components match “${q.value.trim()}”. Clear the search with Esc.` : '';
    spy();
  }
  q.addEventListener('input', filter);
  spy();

  // Project-type filter on components.
  const all = document.getElementById('all');
  if (all) all.addEventListener('click', () => {
    all.textContent = root.classList.toggle('all') ? all.dataset.on : all.dataset.off; filter(); rest();
  });

  // Tabs: click and arrow keys.
  $('[role=tablist]').forEach(list => {
    const tabs = $('[role=tab]:not([disabled])', list);
    const pick = t => tabs.forEach(x => {
      const on = x === t;
      x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      if (on) x.focus();
    });
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => pick(t));
      t.addEventListener('keydown', e => {
        const k = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
        if (k !== undefined) { e.preventDefault(); pick(tabs[(k + tabs.length) % tabs.length]); }
      });
    });
  });

  // Select: listbox keyboard (the button keeps focus, aria-activedescendant tracks the option).
  $('.selw').forEach(w => {
    const b = w.querySelector('.sel'), p = w.querySelector('.pop');
    const opts = $('.opt:not([aria-disabled=true])', w);
    let active = opts.find(o => o.classList.contains('hl')) || opts.find(o => o.getAttribute('aria-selected') === 'true') || opts[0];
    const isOpen = () => b.getAttribute('aria-expanded') === 'true';
    const flow = document.createElement('i');
    flow.className = 'flow'; flow.setAttribute('aria-hidden', 'true');
    p.prepend(flow); p.classList.add('js');
    const place = (o, instant) => {
      if (instant) flow.style.transition = 'none';
      flow.style.height = o.offsetHeight + 'px';
      flow.style.transform = `translateY(${o.offsetTop}px)`;
      flow.classList.add('on');
      if (instant) { void flow.offsetHeight; flow.style.transition = ''; }
    };
    const setActive = (o, instant) => {
      if (!o) return;
      active = o;
      opts.forEach(x => x.classList.toggle('hl', x === o));
      b.setAttribute('aria-activedescendant', o.id);
      place(o, instant);
    };
    if (isOpen()) setActive(active, true);
    new ResizeObserver(() => { if (isOpen()) place(active, true); }).observe(p);
    const open = () => { p.classList.remove('closed'); b.classList.add('open'); b.setAttribute('aria-expanded', 'true'); setActive(active, true); };
    const close = () => { p.classList.add('closed'); b.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.removeAttribute('aria-activedescendant'); };
    const pick = o => {
      opts.forEach(x => {
        const on = x === o;
        x.classList.toggle('selected', on);
        x.setAttribute('aria-selected', String(on));
      });
      b.querySelector('.val').textContent = o.textContent;
      close(); b.focus();
    };
    b.addEventListener('click', () => { if (isOpen()) close(); else open(); });
    b.addEventListener('keydown', e => {
      const i = opts.indexOf(active);
      const k = { ArrowDown: i + 1, ArrowUp: i - 1, Home: 0, End: opts.length - 1 }[e.key];
      if (k !== undefined) {
        e.preventDefault();
        if (!isOpen()) open();
        setActive(opts[(k + opts.length) % opts.length]);
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (isOpen()) pick(active); else open();
      } else if (e.key === 'Escape') close();
      else if (e.key === 'Tab') close();
    });
    opts.forEach(o => {
      o.addEventListener('click', () => pick(o));
      o.addEventListener('pointermove', () => setActive(o));
    });
    document.addEventListener('pointerdown', e => { if (!w.contains(e.target)) close(); });
    if (isOpen()) setActive(active);
  });

  $('.tbl tbody input').forEach(c => c.addEventListener('change', () => c.closest('tr').classList.toggle('selected', c.checked)));
  $('[data-collapse]').forEach(b => b.addEventListener('click', () => {
    const mini = b.closest('.sb').classList.toggle('mini');
    b.setAttribute('aria-expanded', String(!mini));
    b.setAttribute('aria-label', mini ? 'Expand sidebar' : 'Collapse sidebar');
  }));

  // Copy-on-click for token values (swatches, type rows, scale cards, shadows, motion).
  const toastEl = document.querySelector('.toast');
  let toastTimer;
  const toast = msg => {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 1600);
  };
  function legacyCopy(text) {
    const t = document.createElement('textarea');
    t.value = text; t.setAttribute('readonly', ''); t.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(t); t.select();
    try { document.execCommand('copy'); } finally { t.remove(); }
    return Promise.resolve();
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(() => legacyCopy(text));
    }
    return legacyCopy(text);
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-copy]');
    if (!b) return;
    copyText(b.dataset.copy).then(() => {
      toast('Copied ' + b.dataset.copy);
      b.classList.add('done'); clearTimeout(b._t);
      b._t = setTimeout(() => b.classList.remove('done'), 1200);
    }, () => toast('Copy failed'));
  });
})();
""".strip()

SECTIONS = [("overview", "Overview", ""), ("principles", "Principles", "What this tone believes, from its Overview."),
            ("color", "Color", "Semantic roles first, then the tone's palette and project additions. Ratios use the WCAG 2.2 AA thresholds."),
            ("typography", "Typography", "Families, then the full 16-step scale at real size."),
            ("spacing", "Spacing", "The spacing scale. Pick a step; never invent in-between values."),
            ("radius", "Radius", "The radius scale as rendered corners."),
            ("elevation", "Elevation", "Shadow and motion tokens from the tone's prose tables."),
            ("specimens", "Project specimens", "The components this project actually has, captured as static markup and rendered with the same tokens."),
            ("components", "Core contracts", "The skill's default contracts with their states. Shape comes from --c-* tokens, so switching tone or overriding a token changes it."),
            ("contracts", "Contract matrix", "Every contract's status: enforced, replaced by a specimen, excluded by the overlay, or not used by this project type."),
            ("tokens", "Tokens", "The resolved frontmatter this page was built from. Use the copy icon next to a value to copy it.")]


GROUP_OF = {"principles": "Overview", **dict.fromkeys(("color", "typography", "spacing", "radius", "elevation"), "Foundations"),
            "specimens": "Components", "components": "Components", "contracts": "Reference", "tokens": "Reference"}


def build(entries, ptype, core_body, comp_matrix, specimens=(), excluded=frozenset()):
    proj = entries[0]
    core_overview = R.split_sections(core_body).get("Overview", "")
    renderers = {"overview": lambda e: hero(e, ptype), "principles": lambda e: principles(e, core_overview),
                 "color": colors, "typography": typography, "spacing": spacing, "radius": radius,
                 "elevation": elevation, "tokens": tokens}

    def per_tone(fn):
        return "".join(f'<div class="tv" data-for="{e["key"]}">{fn(e)}</div>' for e in entries)

    sections = []
    for sid, title, sub in SECTIONS:
        head = "" if sid == "overview" else (f'<p class="eyebrow">{GROUP_OF[sid]}</p><h2 class="sec t-title-h3">{title}</h2>'
                                             + (f'<p class="sub">{esc(sub)}</p>' if sub else ""))
        if sid == "components":
            body = components(proj["tree"], ptype, comp_matrix, excluded)
        elif sid == "specimens":
            body = specimens_section(specimens)
        elif sid == "contracts":
            body = contracts_section(proj, ptype, comp_matrix, excluded, specimens)
        else:
            body = per_tone(renderers[sid])
        sections.append(f'<section id="{sid}" data-title="{title}">{head}{body}</section>')

    steps = list(dict.fromkeys(n for e in entries for n, _ in type_steps(e["tree"])))
    tone_css = ["".join(f".t-{n}{{{font_decl(n)}}}" for n in steps)]
    for e in entries:
        tone_css.append(f':root[data-tone="{e["key"]}"]{{{tone_vars(e)}}}')
        tone_css.append(f':root:not([data-tone="{e["key"]}"]) .tv[data-for="{e["key"]}"]{{display:none}}')

    families = set()
    for e in entries:
        for _, spec in type_steps(e["tree"]):
            f = first_family(spec.get("fontFamily", ""))
            if f and f.lower() not in SYSTEM_FONTS:
                families.add(f)
    # One link per family (a bad family must not break the others); the plain request is the
    # fallback for static families that lack some of the weights.
    fonts = "".join(f'\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={f.replace(" ", "+")}'
                    f'{w}&amp;display=swap">' for f in sorted(families) for w in (":wght@400;500;600;700", ""))
    if fonts:
        fonts = '\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' + fonts

    options = "".join(f'<option value="{e["key"]}">{esc(e["label"])}</option>' for e in entries)
    titles = {sid: title for sid, title, _ in SECTIONS}
    link = lambda sid, label, cls="": f'<a href="#{sid}"{f" class={cls}" if cls else ""}>{label}</a>'  # noqa: E731
    comps = [(f"c-{COMP_TOKENS.get(n, n.lower())}", n, is_off(n, ptype, comp_matrix))
             for n, *_ in COMPONENTS if R.norm(n) not in excluded]
    shown = sum(not off for *_, off in comps)
    count = f"{shown}/{len(comps)}" if shown < len(comps) else str(len(comps))
    groups = [("Overview", "", [link("overview", "Introduction"), link("principles", "Principles")]),
              ("Foundations", "", [link(s, titles[s]) for s in ("color", "typography", "spacing", "radius", "elevation")]),
              ("Components", count, [link("specimens", "Project specimens"), link("components", "Core contracts"),
                                     '<div class="sgsub">' + "".join(link(cid, n, "off" if off else "") for cid, n, off in comps)
                                     + "</div>"]),
              ("Reference", "", [link("contracts", "Contract matrix"), link("tokens", "Tokens")])]
    side_nav = "".join(f'<div class="sg"><p class="eyebrow">{g}{f"<span>{c}</span>" if c else ""}</p>{"".join(ls)}</div>'
                       for g, c, ls in groups)
    mobile_nav = "".join(link(sid, title) for sid, title, _ in SECTIONS)
    brand = "".join(f'<small class="tv" data-for="{e["key"]}">{esc(e["tone"])} · '
                    f'{"this project" if e["key"] == "project" else "library"}</small>' for e in entries)
    vals = {"default": proj["key"], "title": esc(f"ds4a preview · {proj['tone']}"), "fonts": fonts,
            "tone_css": "\n".join(tone_css), "page_css": PAGE_CSS, "page_js": PAGE_JS, "options": options,
            "side_nav": side_nav, "mobile_nav": mobile_nav, "brand": brand, "sections": "\n".join(sections)}
    # Single pass, so filled-in content is never re-scanned for placeholders.
    return re.sub(r"\{\{(\w+)\}\}", lambda m: vals.get(m.group(1), m.group(0)), TEMPLATE)


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
    overlay = overlay if overlay.exists() else None
    tone, ptype, ov_colors = args.tone, args.ptype, []
    registered, excluded = None, []
    try:
        if overlay:
            ov_fm, _, _ = R.read_layer(overlay)
            tone = tone or R.leaf_text(ov_fm, "tone") or None
            ptype = ptype or R.leaf_text(ov_fm, "type") or None
            if "specimens" in ov_fm:
                registered = R.leaf_list(ov_fm, "specimens")
            excluded = R.leaf_list(ov_fm, "exclude_components")
            if isinstance(ov_fm.get("colors"), dict):
                ov_colors = [k for k, v in ov_fm["colors"].items() if isinstance(v, R.Leaf)]
        tone = tone or "neutral"
        label = f"{tone} · this project"
        entries = [make_entry(lib, "project", label, tone, overlay, ptype, ov_colors)]
    except R.ResolveError as e:
        print(f"ds4a preview: {e}", file=sys.stderr)
        return 1
    specimens = SPEC.load(project, registered)
    excluded_n = {R.norm(x) for x in excluded}

    # Raw library tones for the switcher. Without an overlay the project entry already is the raw tone.
    for p in sorted((lib / "tones").glob("*.md")):
        if p.stem == tone and not overlay:
            continue
        try:
            entries.append(make_entry(lib, "t-" + re.sub(r"[^A-Za-z0-9_-]", "-", p.stem), f"{p.stem} · library",
                                     p.stem, None, ptype))
        except Exception as e:  # a broken tone must not break the page
            print(f"ds4a preview: skipping tone '{p.stem}' in the switcher: {e}", file=sys.stderr)

    core_body = R.read_layer(lib / "core.md")[1]
    comp_matrix = R.load_matrix(R.SKILL_DIR / "references" / "component-matrix.md")[0]
    out = Path(args.out) if args.out else project / ".ds4a" / "preview.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = build(entries, ptype, core_body, comp_matrix, specimens, excluded_n)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page.encode()) // 1024} KB, {len(entries)} tone views, "
          f"{len(specimens)} specimen{'s' if len(specimens) != 1 else ''})", file=sys.stderr)
    for s in specimens:
        if s["status"] in ("changed", "missing"):
            print(f"WARNING specimen '{s['slug']}': source {s['status']} since capture", file=sys.stderr)
    for w in R.contrast_report(entries[0]["tree"]):
        print(f"WARNING contrast: {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

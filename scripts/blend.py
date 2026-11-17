#!/usr/bin/env python3
"""ds4a blend — migrate a hand-written DESIGN.md into the overlay, verified by code.

The doc is a source, never a target: this reads its tokens and prose, compares
them with the values actually in the project (CSS variables, DTCG JSON, typed
token files), reports every conflict with both values and their sources, and
writes the result to <project>/.ds4a/project.md.

  python3 scripts/blend.py --project .                    # report only
  python3 scripts/blend.py --project . --write-overlay     # write the overlay draft
  python3 scripts/blend.py --project . --adopt             # write overlay + regenerate DESIGN.md

--prefer code (default) keeps the value the code uses; --prefer doc keeps the
doc's value. Either way both values are printed. Existing overlay values win
over both: they are the latest decision.

--adopt is the end of the fork: the old DESIGN.md is copied to
.ds4a/DESIGN.md.pre-ds4a.md and replaced by the generated one. Only run it after
the user confirms adoption.

Standard library only.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve as R  # noqa: E402

TOKEN_GROUPS = ("colors", "typography", "rounded", "spacing", "components")
META_KEYS = {"tone", "type", "exclude_components", "specimens", "source-of-truth",
             "adopted", "blended"}
CSS_FILES = ("globals.css", "global.css", "style.css", "tokens.css", "theme.css")
CODE_GLOBS = ("src/**/*.css", "app/**/*.css", "styles/**/*.css", "src/**/*.json",
              "tokens.json", "src/tokens/**/*.json", "src/lib/design-tokens.ts",
              "src/tokens/design-tokens.ts", "design-tokens.ts", "tailwind.config.*")
SKIP_PARTS = {"node_modules", ".git", ".next", "dist", "build", ".ds4a", "coverage"}


class BlendError(Exception):
    pass


# ───────────────────────── parsing ─────────────────────────

def plain(node):
    if isinstance(node, dict):
        return {k: plain(v) for k, v in node.items() if not isinstance(v, R.Comment)}
    if isinstance(node, R.Leaf):
        val = R.unquote(node.value)
        if val.startswith("[") and val.endswith("]"):
            return [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
        return val
    return node


def read_design(path):
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    if text.startswith("---"):
        lines = text.split("\n")
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            fm = plain(R.parse_yaml(lines[1:end]))
            body = "\n".join(lines[end + 1:])
    return fm, body


def table_rows(section, header_word=None):
    rows = {}
    for line in section.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: ") or cells[0] in ("Token", "Category"):
            continue
        if header_word and header_word not in " ".join(cells):
            continue
        rows[cells[0].strip("`*")] = cells[1].strip("`*")
    return rows


def doc_tokens(fm, body):
    """Token groups from frontmatter plus the doc's markdown tables."""
    out = {g: {} for g in TOKEN_GROUPS}
    for g in TOKEN_GROUPS:
        if isinstance(fm.get(g), dict):
            if g in ("typography", "components"):
                out[g] = dict(fm[g])
            else:
                out[g] = {k: v for k, v in fm[g].items() if not isinstance(v, dict)}
    sections = R.split_sections(body)

    for k, v in table_rows(sections.get("Colors", "")).items():
        if re.match(r"^(#|rgb|hsl|oklch|var\()", v, re.I):
            out["colors"].setdefault(k, v)
    for k, v in table_rows(sections.get("Layout", "")).items():
        if re.fullmatch(r"\d+(\.\d+)?(px|rem|em)", v):
            out["spacing"].setdefault(k, v)
    for k, v in table_rows(sections.get("Shapes", "")).items():
        if re.fullmatch(r"\d+(\.\d+)?(px|rem|em|%)", v):
            out["rounded"].setdefault(k, v)

    typ = sections.get("Typography", "")
    m = re.search(r"(?ms)^### Size scale\s*$(.*?)(?=^#{2,3} |\Z)", typ)
    for line in (m.group(1) if m else "").split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`*") for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or set(cells[0]) <= set("-: ") or cells[0] == "Token":
            continue
        token, size, leading, tracking = cells[:4]
        step = out["typography"].setdefault(token, {})
        step.setdefault("fontSize", size)
        step.setdefault("lineHeight", leading)
        step.setdefault("letterSpacing", tracking)
    return out


# ───────────────────────── code extraction ─────────────────────────

def css_tokens(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "Generated by ds4a" in text[:400]:
        return {}
    out = {"colors": {}, "typography": {}, "rounded": {}, "spacing": {}}
    for m in re.finditer(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+);", text):
        name, value = m.group(1), m.group(2).strip()
        if value.startswith("var("):
            continue
        if name.startswith("--color-"):
            out["colors"][name[len("--color-"):]] = value
        elif name.startswith("--spacing-"):
            out["spacing"][name[len("--spacing-"):]] = value
        elif name.startswith("--radius-"):
            out["rounded"][name[len("--radius-"):]] = value
        elif name.startswith("--font-size-"):
            step = name[len("--font-size-"):]
            out["typography"].setdefault(step, {})["fontSize"] = value
    return out


def flatten_json(node, prefix=()):
    if isinstance(node, dict):
        if "$value" in node:
            yield prefix, node["$value"]
        else:
            for k, v in node.items():
                yield from flatten_json(v, prefix + (str(k),))
    elif isinstance(node, list):
        return
    else:
        yield prefix, node


def map_json_path(parts, value, out):
    if not parts:
        return
    group = parts[0].lower()
    if group in ("color", "colors") and len(parts) >= 2:
        out["colors"][parts[-1]] = str(value)
    elif group in ("spacing", "space") and len(parts) >= 2:
        out["spacing"][parts[-1]] = str(value)
    elif group in ("radius", "rounded", "radii") and len(parts) >= 2:
        out["rounded"][parts[-1]] = str(value)
    elif group in ("font-size", "fontsize") and len(parts) >= 2:
        out["typography"].setdefault(parts[-1], {})["fontSize"] = str(value)
    elif group == "typography" and len(parts) >= 3:
        step, prop = parts[-2], parts[-1]
        key = {"fontsize": "fontSize", "lineheight": "lineHeight",
               "letterspacing": "letterSpacing", "fontfamily": "fontFamily",
               "fontweight": "fontWeight"}.get(prop.lower())
        if key:
            out["typography"].setdefault(step, {})[key] = str(value)


def json_tokens(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out = {"colors": {}, "typography": {}, "rounded": {}, "spacing": {}}
    for parts, value in flatten_json(data):
        map_json_path(parts, value, out)
    return out


def balanced(text, start, open_ch="{", close_ch="}"):
    depth, i, quote = 0, start, None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
        i += 1
    return ""


def js_tokens(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    out = {"colors": {}, "typography": {}, "rounded": {}, "spacing": {}}
    for key in ("colors", "spacing", "borderRadius", "radius", "fontSize"):
        m = re.search(rf"\b{key}\s*:\s*\{{", text)
        if not m:
            continue
        body = balanced(text, m.end() - 1)
        for p in re.finditer(r"([A-Za-z0-9_'\"]+)\s*:\s*['\"]([^'\"]+)['\"]", body):
            name, value = p.group(1).strip("'\""), p.group(2)
            if key == "colors":
                out["colors"][name] = value
            elif key == "spacing":
                out["spacing"][name] = value
            elif key in ("borderRadius", "radius"):
                out["rounded"][name] = value
            elif key == "fontSize":
                out["typography"].setdefault(name, {})["fontSize"] = value
    return out


def discover_code(project):
    tokens = {"colors": {}, "typography": {}, "rounded": {}, "spacing": {}}
    sources, seen = [], set()
    candidates = []
    for name in CSS_FILES:
        candidates += list(project.glob(f"**/{name}"))
    for pattern in CODE_GLOBS:
        candidates += list(project.glob(pattern))
    for p in sorted(candidates):
        if not p.is_file() or p in seen:
            continue
        seen.add(p)
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if p.suffix == ".css":
            found = css_tokens(p)
        elif p.suffix == ".json":
            found = json_tokens(p)
        elif p.suffix in (".ts", ".js", ".tsx", ".jsx"):
            found = js_tokens(p)
        else:
            continue
        if not any(found.get(g) for g in found):
            continue
        sources.append(p.relative_to(project).as_posix())
        for g, group in found.items():
            tokens.setdefault(g, {}).update(group)
    return tokens, sources


# ───────────────────────── merge / report ─────────────────────────

def norm_value(v):
    v = str(v).strip().strip("'\"").lower()
    if re.fullmatch(r"#[0-9a-f]{3}", v):
        v = "#" + "".join(c * 2 for c in v[1:])
    return re.sub(r"\s+", " ", v)


def merge_groups(base, other, label, provenance, source_label):
    conflicts = []

    def node(dst, src, prefix):
        for k, v in src.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                cur = dst.setdefault(k, {})
                if not isinstance(cur, dict):
                    cur = {}
                    dst[k] = cur
                node(cur, v, path)
            else:
                old = dst.get(k)
                if old is not None and norm_value(old) != norm_value(v):
                    conflicts.append((path, old, v, provenance.get(path, label), source_label))
                dst[k] = v
                provenance[path] = source_label

    for group in TOKEN_GROUPS:
        if group in other:
            node(base.setdefault(group, {}), other[group], group)
    return conflicts


def norm_line(s):
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"^[\s\-–—✅❌☑]+", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def unique_prose(body, baseline):
    base = {norm_line(line) for line in baseline.split("\n") if line.strip()}
    sections = R.split_sections(body)
    out = {}
    for name in ("Overview", "Colors", "Typography", "Layout", "Elevation & Depth",
                 "Shapes", "Components", "Do's and Don'ts", "Pre-flight Checklist"):
        text = sections.get(name, "")
        if not text:
            continue
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        keep, seen = [], set()
        for line in text.split("\n"):
            s = line.strip()
            if not s.startswith(("-", "☐")):
                continue
            if re.match(r"^-\s*\|", s):
                continue
            n = norm_line(s)
            if len(n) < 12 or n in base or n in seen:
                continue
            seen.add(n)
            keep.append(s)
        if keep:
            out[name] = keep
    return out


def yaml_scalar(v):
    v = str(v)
    if re.fullmatch(r"-?\d+(\.\d+)?(px|rem|em|%|ms|s)?", v):
        return v
    return R.quote(v)


def dump_group(name, node, indent=0):
    pre = " " * indent
    lines = [f"{pre}{name}:"]
    for k, v in node.items():
        if isinstance(v, dict):
            lines += dump_group(k, v, indent + 2)
        elif isinstance(v, list):
            lines.append(f"{pre}  {k}: [{', '.join(str(x) for x in v)}]")
        else:
            lines.append(f"{pre}  {k}: {yaml_scalar(v)}")
    return lines


def write_overlay(project, tokens, prose, existing=None):
    overlay = project / ".ds4a" / "project.md"
    fm = {}
    body_sections = {}
    if existing and existing.exists():
        old_fm, old_body = read_design(existing)
        fm = {k: v for k, v in old_fm.items() if k not in TOKEN_GROUPS}
        body_sections = R.split_sections(old_body)
    fm.setdefault("tone", "neutral")
    fm["blended"] = date.today().isoformat()
    for group in TOKEN_GROUPS:
        if tokens.get(group):
            fm[group] = tokens[group]
    for name, lines in prose.items():
        cur = body_sections.get(name, "").strip()
        add = "\n".join(lines)
        if not cur:
            body_sections[name] = "### Project notes\n\n" + add
        elif "### Project notes" in cur:
            body_sections[name] = cur.rstrip() + "\n" + add
        else:
            body_sections[name] = cur.rstrip() + "\n\n### Project notes\n\n" + add

    known = ["tone", "type", "source-of-truth", "blended"] + list(TOKEN_GROUPS) + \
            ["specimens", "exclude_components"]
    lines = ["---"]
    lines.append(f"# blended from DESIGN.md {date.today().isoformat()}; tokens verified against code.")
    for k in known:
        v = fm.get(k)
        if v in (None, "", [], {}):
            continue
        if isinstance(v, dict):
            lines += dump_group(k, v)
        elif isinstance(v, list):
            lines.append(f"{k}: [{', '.join(str(x) for x in v)}]")
        else:
            lines.append(f"{k}: {v}" if k in ("tone", "type", "blended", "source-of-truth") else f"{k}: {yaml_scalar(v)}")
    for k in fm:
        if k in known or k in ("blended",):
            continue
        if isinstance(fm[k], (dict, list)):
            continue
        lines.append(f"{k}: {yaml_scalar(fm[k])}")
    lines += ["---", ""]
    order = ["Overview", "Colors", "Typography", "Layout", "Elevation & Depth", "Shapes",
             "Components", "Do's and Don'ts", "Pre-flight Checklist"]
    for name in order:
        if name in body_sections:
            lines += [f"## {name}", "", body_sections[name].strip(), ""]
    for name, text in body_sections.items():
        if name not in order:
            lines += [f"## {name}", "", text.strip(), ""]
    overlay.parent.mkdir(parents=True, exist_ok=True)
    if overlay.exists():
        backup = overlay.with_name(f"project.md.{datetime.now():%Y%m%d-%H%M%S}.bak")
        backup.write_text(overlay.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"backup: {backup}")
    overlay.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return overlay


def run_resolve(project, lib, adopt=False, out=None):
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "resolve.py"),
           "--project", str(project), "--library", str(lib)]
    if adopt:
        cmd.append("--adopt")
    if out:
        cmd += ["--out", str(out)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        raise BlendError(res.stderr.strip() or "resolve failed")
    print(res.stderr.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=".")
    ap.add_argument("--library", default=str(R.SKILL_DIR / "library"))
    ap.add_argument("--design", help="hand-written DESIGN.md (default: <project>/DESIGN.md)")
    ap.add_argument("--prefer", choices=("code", "doc"), default="code",
                    help="which value wins a conflict (default: code)")
    ap.add_argument("--write-overlay", action="store_true", help="write .ds4a/project.md")
    ap.add_argument("--adopt", action="store_true", help="write overlay and regenerate DESIGN.md in place")
    ap.add_argument("--check", action="store_true", help="report only (default)")
    args = ap.parse_args()

    project, lib = Path(args.project), Path(args.library)
    design = Path(args.design) if args.design else project / "DESIGN.md"
    if not design.exists():
        print(f"ds4a blend: {design} does not exist", file=sys.stderr)
        return 1
    try:
        doc_fm, doc_body = read_design(design)
    except (R.ResolveError, ValueError) as e:
        print(f"ds4a blend: cannot read {design}: {e}", file=sys.stderr)
        return 1

    doc = doc_tokens(doc_fm, doc_body)
    code, sources = discover_code(project)
    has_doc = {g: bool(doc.get(g)) for g in TOKEN_GROUPS}
    has_code = {g: bool(code.get(g)) for g in TOKEN_GROUPS}

    tokens = {g: {} for g in TOKEN_GROUPS}
    provenance = {}
    conflicts = merge_groups(tokens, doc, "DESIGN.md", provenance, "DESIGN.md")
    conflicts += merge_groups(tokens, code, "code", provenance, "code")
    if args.prefer == "doc":
        tokens = {g: {} for g in TOKEN_GROUPS}
        provenance = {}
        conflicts = merge_groups(tokens, code, "code", provenance, "code")
        conflicts += merge_groups(tokens, doc, "DESIGN.md", provenance, "DESIGN.md")

    overlay = project / ".ds4a" / "project.md"
    if overlay.exists():
        try:
            ov_fm, _ = read_design(overlay)
            ov_tokens = {g: ov_fm.get(g, {}) for g in TOKEN_GROUPS if ov_fm.get(g)}
            if ov_tokens:
                conflicts += merge_groups(tokens, ov_tokens, "existing overlay", provenance, "existing overlay")
                print("note: existing overlay values win over both doc and code")
        except (R.ResolveError, ValueError) as e:
            print(f"ds4a blend: warning: could not read existing overlay: {e}", file=sys.stderr)

    tone = "neutral"
    ptype = None
    if overlay.exists():
        try:
            ov_fm, _ = read_design(overlay)
            tone = ov_fm.get("tone") or tone
            ptype = ov_fm.get("type") or None
        except Exception:
            pass
    try:
        baseline, _ = R.resolve(lib, tone, None, ptype)
    except R.ResolveError as e:
        print(f"ds4a blend: {e}", file=sys.stderr)
        return 1
    prose = unique_prose(doc_body, baseline)

    print("ds4a blend")
    print(f"  doc:  {design}" + (" (frontmatter + tables)" if doc_fm else " (tables)"))
    print(f"  code: {', '.join(sources) if sources else 'no token files found'}")
    imported = ", ".join(
        f"{len(tokens[g])} {label}" for g, label in
        (("colors", "colors"), ("spacing", "spacing"), ("rounded", "radius"),
         ("typography", "type"), ("components", "component groups"))
        if tokens.get(g)) or "nothing"
    print(f"  imported: {imported}")
    if conflicts:
        print(f"  conflicts: {len(conflicts)} ({args.prefer} preferred)")
        for path, old_v, new_v, old_src, new_src in conflicts:
            print(f"    {path}: {old_src} {old_v} / {new_src} {new_v}")
    else:
        print("  conflicts: none — code and doc agree where both define a token")
    if prose:
        print(f"  prose: {sum(len(v) for v in prose.values())} unique project rule(s) kept")
    if not args.write_overlay and not args.adopt:
        print("  wrote: nothing (use --write-overlay or --adopt)")
        return 0

    out = write_overlay(project, tokens, prose, overlay if overlay.exists() else None)
    print(f"  wrote: {out}")
    if args.adopt:
        old = project / "DESIGN.md"
        backup = project / ".ds4a" / "DESIGN.md.pre-ds4a.md"
        if old.exists() and not backup.exists():
            backup.write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"  backup: {backup}")
        run_resolve(project, lib, adopt=True)
        beside = project / "DESIGN.generated.md"
        if beside.exists() and R.MARKER in beside.read_text(encoding="utf-8"):
            beside.unlink()
            print(f"  removed: {beside} (superseded by the adopted DESIGN.md)")
        print(f"  adopted: {old} regenerated from the overlay")
    else:
        old = project / "DESIGN.md"
        generated = old.exists() and R.MARKER in old.read_text(encoding="utf-8")
        if old.exists() and not generated:
            beside = project / "DESIGN.generated.md"
            run_resolve(project, lib, out=beside)
            print(f"  resolved: {beside} (generated beside the hand-written DESIGN.md)")
            print("  adopt: run again with --adopt to replace DESIGN.md after the user confirms")
        else:
            run_resolve(project, lib)
            print(f"  resolved: {old} (generated from the overlay)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BlendError as e:
        print(f"ds4a blend: {e}", file=sys.stderr)
        sys.exit(1)

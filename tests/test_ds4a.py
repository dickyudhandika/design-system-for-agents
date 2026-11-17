#!/usr/bin/env python3
"""Regression tests for the ds4a scripts.

Run from the skill root:
  python3 -m unittest discover -s tests -v
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
LIB = ROOT / "library"
sys.path.insert(0, str(SCRIPTS))

import resolve as R  # noqa: E402
import specimens as SPEC  # noqa: E402
import apply as APPLY  # noqa: E402
import blend as BLEND  # noqa: E402

# build-preview.py cannot be imported by name; load it explicitly once.
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("build_preview_mod", SCRIPTS / "build-preview.py")
build_preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_preview)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        write(self.project / ".ds4a" / "project.md", "---\ntone: neutral\ntype: dashboard\n---\n")

    def tearDown(self):
        self._tmp.cleanup()

    def resolve(self):
        doc, info = R.resolve(LIB, "neutral", self.project / ".ds4a" / "project.md", "dashboard")
        return doc, info


class ResolveTests(Base):
    def test_generated_marker_and_layer_note(self):
        doc, info = self.resolve()
        self.assertIn(R.MARKER, doc)
        self.assertIn("core v1 + tone neutral v1 + project overlay", info["layers"])
        self.assertIn("## Components", doc)

    def test_overlay_metadata_does_not_leak_into_tokens(self):
        write(self.project / ".ds4a" / "project.md",
              "---\ntone: neutral\ntype: dashboard\nspecimens: [pill]\n"
              "source-of-truth: src/lib/design-tokens.ts\n---\n")
        doc, info = self.resolve()
        self.assertNotIn("specimens:", doc)
        self.assertNotIn("source-of-truth:", doc)
        self.assertIn("colors:", doc)

    def test_exclude_components_and_replace_section(self):
        write(self.project / ".ds4a" / "project.md",
              "---\ntone: neutral\ntype: dashboard\nexclude_components: [Tabs]\n---\n\n"
              "## Colors\n\n<!-- replace -->\n\nOnly warm colors here.\n")
        doc, info = self.resolve()
        self.assertEqual(info["excluded"], ["Tabs"])
        self.assertNotIn("### Tabs", doc)
        self.assertNotIn("### Token roles", doc)
        self.assertIn("Only warm colors here.", doc)


class SpecimenTests(Base):
    def make_component(self):
        write(self.project / "src" / "components" / "Pill.tsx",
              'export function Pill({ label = "Live" }) {\n'
              '  return (<span className="pill">{label}</span>);\n}\n')

    def test_add_registers_and_loads(self):
        self.make_component()
        args = type("A", (), {"name": "Pill", "source": "src/components/Pill.tsx", "html": None,
                              "title": None, "contract": None, "captured": None, "force": False,
                              "no_build": True})()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(SPEC.add(args, self.project, LIB), 0)
        text = (self.project / ".ds4a" / "specimens" / "pill.html").read_text()
        self.assertIn("ds4a:specimen", text)
        self.assertIn("source: src/components/Pill.tsx", text)
        self.assertIn("Live", text)
        self.assertIn("specimens: [pill]", (self.project / ".ds4a" / "project.md").read_text())
        loaded = SPEC.load(self.project)
        self.assertEqual(loaded[0]["title"], "Pill")
        self.assertEqual(loaded[0]["status"], "ok")

    def test_scan_finds_uncovered_components_and_skips_contracts(self):
        self.make_component()
        write(self.project / "src" / "components" / "Button.tsx", "export const Button = () => <button />;")
        rows = SPEC.scan(self.project, LIB)
        self.assertEqual([r["slug"] for r in rows], ["pill"])

    def test_registered_filter_hides_unlisted_files(self):
        self.make_component()
        write(self.project / ".ds4a" / "specimens" / "pill.html",
              "<!-- ds4a:specimen\ntitle: Pill\n-->\n<span>one</span>")
        write(self.project / ".ds4a" / "specimens" / "other.html",
              "<!-- ds4a:specimen\ntitle: Other\n-->\n<span>two</span>")
        self.assertEqual([s["slug"] for s in SPEC.load(self.project, ["pill"])], ["pill"])
        self.assertEqual(len(SPEC.load(self.project, None)), 2)


class ApplyTests(Base):
    def test_apply_writes_tokens_and_check_is_clean(self):
        _, info = self.resolve()
        tokens = APPLY.expected_tokens(info, APPLY.layer_texts(LIB, "neutral", None))
        out = self.project / APPLY.DEFAULT_OUT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(APPLY.css_file(info, tokens), encoding="utf-8")
        self.assertIn("--color-primary", out.read_text())
        self.assertIn(APPLY.MARKER, out.read_text())
        with redirect_stdout(io.StringIO()):
            self.assertEqual(APPLY.check(self.project, out, tokens), 0)

    def test_check_reports_drift_and_hardcoded_values(self):
        _, info = self.resolve()
        tokens = APPLY.expected_tokens(info, APPLY.layer_texts(LIB, "neutral", None))
        out = self.project / APPLY.DEFAULT_OUT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(APPLY.css_file(info, tokens).replace("#2563EB", "#000000"), encoding="utf-8")
        write(self.project / "src" / "app.css", ".x { color: #2563EB; padding: 24px; }\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = APPLY.check(self.project, out, tokens)
        report = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("drift: --color-primary", report)
        self.assertIn("candidate: src/app.css:1 uses #2563EB", report)
        self.assertIn("candidate: src/app.css:1 uses 24px", report)


class PreviewTests(Base):
    def test_preview_has_specimens_contracts_and_copy(self):
        write(self.project / ".ds4a" / "project.md",
              "---\ntone: neutral\ntype: dashboard\nexclude_components: [Tabs]\n"
              "specimens: [pill]\n---\n")
        write(self.project / ".ds4a" / "specimens" / "pill.html",
              "<!-- ds4a:specimen\ntitle: Pill\nsource: src/components/Pill.tsx\n"
              f"captured: 2026-11-17\ncontract: Badge\n-->\n<span class=\"pill\">Live</span>")
        write(self.project / "src" / "components" / "Pill.tsx", "export const Pill = () => <span />;")
        _, info = self.resolve()
        entries = [build_preview.make_entry(LIB, "project", "neutral · this project", "neutral",
                                           self.project / ".ds4a" / "project.md", "dashboard")]
        core_body = R.read_layer(LIB / "core.md")[1]
        matrix = R.load_matrix(ROOT / "references" / "component-matrix.md")[0]
        page = build_preview.build(entries, "dashboard", core_body, matrix,
                                   SPEC.load(self.project), {R.norm("Tabs")})
        self.assertIn('id="specimens"', page)
        self.assertIn("Project specimens", page)
        self.assertIn('id="contracts"', page)
        self.assertIn("st-specimen", page)
        self.assertIn("st-excluded", page)
        self.assertIn("data-copy=", page)
        self.assertIn('class="cmp excluded"', page)


class BlendTests(Base):
    def setUp(self):
        super().setUp()
        write(self.project / "src" / "styles" / "globals.css",
              ":root { --color-primary: #1A5EFF; --spacing-xl: 24px; --radius-md: 0px; }\n")
        write(self.project / "DESIGN.md",
              "# Hand-written\n\n## Colors\n\n| Token | Value | Role |\n|---|---|---|\n"
              "| `primary` | `#2563EB` | CTA |\n\n## Layout\n\n### Spacing system\n\n"
              "| Token | Value | Typical use |\n|---|---|---|\n| `xl` | 24px | Cards |\n\n"
              "## Do's and Don'ts\n\n- ✅ **Do** keep one primary action per screen.\n"
              "- ❌ **Don't** add shadows to cards.\n")

    def test_report_finds_conflict(self):
        doc_fm, doc_body = BLEND.read_design(self.project / "DESIGN.md")
        doc = BLEND.doc_tokens(doc_fm, doc_body)
        code, sources = BLEND.discover_code(self.project)
        tokens = {g: {} for g in BLEND.TOKEN_GROUPS}
        conflicts = BLEND.merge_groups(tokens, doc, "DESIGN.md", {}, "DESIGN.md")
        conflicts += BLEND.merge_groups(tokens, code, "code", {}, "code")
        self.assertEqual(tokens["colors"]["primary"], "#1A5EFF")
        self.assertTrue(any(c[0] == "colors.primary" for c in conflicts))

    def test_write_overlay_keeps_hand_written_doc(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            sys.argv = ["blend.py", "--project", str(self.project), "--library", str(LIB), "--write-overlay"]
            self.assertEqual(BLEND.main(), 0)
        overlay = (self.project / ".ds4a" / "project.md").read_text()
        self.assertIn("primary: \"#1A5EFF\"", overlay)
        self.assertIn("Project notes", overlay)
        self.assertTrue((self.project / "DESIGN.md").read_text().startswith("# Hand-written"))
        self.assertTrue((self.project / "DESIGN.generated.md").exists())
        self.assertIn(R.MARKER, (self.project / "DESIGN.generated.md").read_text())

    def test_adopt_replaces_doc_and_backs_it_up(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            sys.argv = ["blend.py", "--project", str(self.project), "--library", str(LIB), "--adopt"]
            self.assertEqual(BLEND.main(), 0)
        self.assertIn(R.MARKER, (self.project / "DESIGN.md").read_text())
        self.assertTrue((self.project / ".ds4a" / "DESIGN.md.pre-ds4a.md").exists())
        self.assertFalse((self.project / "DESIGN.generated.md").exists())


if __name__ == "__main__":
    unittest.main()

"""Regression tests for the static site checker using temporary site trees."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_site import check

INDEX = """<!doctype html>
<html lang="en"><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A local project">
<meta property="og:image:alt" content="An illustrated local lamp">
<meta name="color-scheme" content="light">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'">
<link rel="canonical" href="https://example.github.io/afterlit-site/">
<link rel="stylesheet" href="styles.css?v=20261026-1">
<script src="site.js?v=20261026-1" defer></script>
<title>afterlit</title></head>
<body><main id="top"><h1>afterlit</h1><p>Pre-alpha. The source is private.</p><p>Use --json and a -10px offset.</p>
<a href="#top">Back to top</a></main></body></html>
"""
NOT_FOUND = """<!doctype html><html lang="en"><head>
<link rel="stylesheet" href="/afterlit-site/styles.css?v=20261026-1">
<link rel="icon" href="/afterlit-site/assets/icon.svg">
<title>Page not found</title></head><body>
<a href="/afterlit-site/">Home</a></body></html>
"""
CSS = 'body { margin-left: -10px; border-top: 1px solid #222; } a::after { content: "+"; }'
SVG = '<svg xmlns="http://www.w3.org/2000/svg"><path d="M-1 0h12"/></svg>'


class SiteCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        (self.site / "assets").mkdir()
        (self.site / "index.html").write_text(INDEX, encoding="utf-8")
        (self.site / "404.html").write_text(NOT_FOUND, encoding="utf-8")
        (self.site / "styles.css").write_text(CSS, encoding="utf-8")
        (self.site / "site.js").write_text('"use strict";', encoding="utf-8")
        (self.site / "assets/icon.svg").write_text(SVG, encoding="utf-8")

    def test_valid_project_paths_and_ordinary_hyphens(self) -> None:
        self.assertEqual(check(self.site), [])

    def test_missing_or_empty_asset_versions_are_rejected(self) -> None:
        for filename, template, asset in (
            ("index.html", INDEX, "styles.css"),
            ("index.html", INDEX, "site.js"),
            ("404.html", NOT_FOUND, "/afterlit-site/styles.css"),
        ):
            for version in ("", "?v=", "?v=+", "?v=one&v=two"):
                with self.subTest(filename=filename, asset=asset, version=version):
                    path = self.site / filename
                    path.write_text(
                        template.replace(asset + "?v=20261026-1", asset + version),
                        encoding="utf-8",
                    )
                    self.assertTrue(any("needs one non-empty ?v= version" in error for error in check(self.site)))
                    path.write_text(template, encoding="utf-8")

    def test_mismatched_css_and_js_versions_are_rejected_across_pages(self) -> None:
        for filename, template, asset in (
            ("index.html", INDEX, "styles.css"),
            ("index.html", INDEX, "site.js"),
            ("404.html", NOT_FOUND, "/afterlit-site/styles.css"),
        ):
            with self.subTest(filename=filename, asset=asset):
                path = self.site / filename
                path.write_text(
                    template.replace(asset + "?v=20261026-1", asset + "?v=older"),
                    encoding="utf-8",
                )
                self.assertTrue(any("asset versions differ" in error for error in check(self.site)))
                path.write_text(template, encoding="utf-8")

    def test_required_social_alt_and_color_scheme_metadata(self) -> None:
        for key, tag in (
            ("og:image:alt", '<meta property="og:image:alt" content="An illustrated local lamp">'),
            ("color-scheme", '<meta name="color-scheme" content="light">'),
        ):
            empty_tag = tag[: tag.index('content="')] + 'content=" ">'
            for replacement in ("", empty_tag):
                with self.subTest(key=key, replacement=replacement):
                    (self.site / "index.html").write_text(INDEX.replace(tag, replacement), encoding="utf-8")
                    self.assertTrue(any(f"non-empty {key} meta tag" in error for error in check(self.site)))

    def test_color_scheme_must_be_light(self) -> None:
        (self.site / "index.html").write_text(
            INDEX.replace('content="light"', 'content="dark"'), encoding="utf-8"
        )
        self.assertTrue(any("color-scheme must be light" in error for error in check(self.site)))

    def test_encoded_html_dash_in_404_is_rejected(self) -> None:
        (self.site / "404.html").write_text(
            NOT_FOUND.replace("Home", "Back &#x2014; home"), encoding="utf-8"
        )
        self.assertTrue(
            any("404.html" in error and "U+2014" in error for error in check(self.site))
        )

    def test_svg_text_entity_is_rejected_but_path_coordinates_are_allowed(self) -> None:
        (self.site / "assets/icon.svg").write_text(
            SVG.replace("</svg>", "<title>Life &#x2013; local</title></svg>"), encoding="utf-8"
        )
        self.assertTrue(
            any("icon.svg" in error and "U+2013" in error for error in check(self.site))
        )

    def test_css_escaped_content_dash_is_rejected(self) -> None:
        (self.site / "styles.css").write_text(
            CSS + r' a::before { content: ";\2014"; }', encoding="utf-8"
        )
        self.assertTrue(
            any("styles.css content" in error and "U+2014" in error for error in check(self.site))
        )

    def test_css_escaped_minus_sign_is_rejected(self) -> None:
        (self.site / "styles.css").write_text(
            CSS + r' a::before { content: "\2212"; }', encoding="utf-8"
        )
        self.assertTrue(any("U+2212" in error for error in check(self.site)))

    def test_escaped_backslash_is_not_a_unicode_escape(self) -> None:
        (self.site / "styles.css").write_text(
            CSS + r' a::before { content: "\\2212"; }', encoding="utf-8"
        )
        self.assertEqual(check(self.site), [])

    def test_out_of_range_unicode_escape_is_replaced_without_crashing(self) -> None:
        (self.site / "styles.css").write_text(
            CSS + r' a::before { content: "\FFFFFF"; }', encoding="utf-8"
        )
        self.assertEqual(check(self.site), [])

    def test_unrelated_root_path_and_dangling_anchor_are_rejected(self) -> None:
        (self.site / "404.html").write_text(
            NOT_FOUND.replace("/afterlit-site/styles.css", "/other/styles.css").replace(
                '/afterlit-site/">Home', '/afterlit-site/#missing">Home'
            ),
            encoding="utf-8",
        )
        errors = check(self.site)
        self.assertTrue(any("unrelated site-root path" in error for error in errors))
        self.assertTrue(any("dangling anchor" in error for error in errors))


    def write_index(self, extra: str) -> None:
        (self.site / "index.html").write_text(
            INDEX.replace("</main>", extra + "</main>"), encoding="utf-8"
        )

    def test_pre_without_scroll_region_attributes_is_rejected(self) -> None:
        for extra, message in (
            ("<pre>commands</pre>", "pre needs"),
            ('<pre role="region" aria-label="Commands">commands</pre>', "pre needs"),
            ('<pre tabindex="0" aria-label="Commands">commands</pre>', "pre needs"),
            ('<pre tabindex="-1" role="region" aria-label="Commands">commands</pre>', "pre needs"),
            ('<pre tabindex="0" role="region" aria-label=" ">commands</pre>', "pre needs"),
            ('<pre tabindex="0" role="region" aria-label="Commands"></pre>' * 2,
             "duplicate pre aria-label"),
        ):
            with self.subTest(extra=extra):
                self.write_index(extra)
                self.assertTrue(any(message in error for error in check(self.site)))

    def test_inline_style_handler_and_script_are_rejected(self) -> None:
        for extra, message in (
            ('<p style="color:red">text</p>', "style attribute"),
            ('<button onclick="run()">Run</button>', "event handler"),
            ('<style>body {color:red}</style>', "style element"),
            ('<script>alert(1)</script>', "script needs src"),
        ):
            with self.subTest(extra=extra):
                (self.site / "404.html").write_text(
                    NOT_FOUND.replace("</body>", extra + "</body>"), encoding="utf-8"
                )
                self.assertTrue(any(message in error for error in check(self.site)))

    def test_csp_meta_required_with_exact_directives(self) -> None:
        meta = next(line for line in INDEX.splitlines() if "http-equiv=" in line)
        for replacement, message in (
            ("", "expected one Content-Security-Policy"),
            (meta + meta, "expected one Content-Security-Policy"),
            (meta.replace("script-src 'self'", "script-src 'self' https://cdn.example"),
             "CSP script-src"),
            (meta.replace("connect-src 'none'; ", ""), "CSP connect-src"),
            (meta.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'"),
             "unsafe-"),
            (meta.replace("script-src 'self'", "script-src 'self'; script-src 'self'"),
             "duplicate CSP directive"),
        ):
            with self.subTest(replacement=replacement):
                (self.site / "index.html").write_text(
                    INDEX.replace(meta, replacement), encoding="utf-8"
                )
                self.assertTrue(any(message in error for error in check(self.site)))
        (self.site / "index.html").write_text(
            INDEX.replace("Content-Security-Policy", "CONTENT-SECURITY-POLICY"),
            encoding="utf-8",
        )
        self.assertEqual(check(self.site), [])

    def test_external_link_needs_https_and_noopener_noreferrer(self) -> None:
        for link, message in (
            ('<a href="http://example.com" rel="noopener noreferrer">Link</a>', "HTTPS"),
            ('<a href="https://example.com">Link</a>', "noopener noreferrer"),
            ('<a href="https://example.com" rel="noopener">Link</a>', "noopener noreferrer"),
        ):
            with self.subTest(link=link):
                self.write_index(link)
                self.assertTrue(any(message in error for error in check(self.site)))
        self.write_index('<a href="https://example.com" rel="noopener noreferrer">Link</a>')
        self.assertEqual(check(self.site), [])

    def test_dangling_aria_and_label_references_are_rejected(self) -> None:
        for extra in (
            '<p aria-labelledby="top missing">text</p>',
            '<p aria-describedby="missing">text</p>',
            '<button aria-controls="missing">Run</button>',
            '<label for="missing">Name</label>',
            '<output for="top missing">Value</output>',
        ):
            with self.subTest(extra=extra):
                self.write_index(extra)
                self.assertTrue(any("dangling id reference" in error for error in check(self.site)))
        self.write_index('<label for="later">Name</label><input id="later">')
        self.assertEqual(check(self.site), [])

    def test_index_needs_exactly_one_h1(self) -> None:
        for replacement in ("", "<h1>afterlit</h1><h1>Again</h1>"):
            with self.subTest(replacement=replacement):
                (self.site / "index.html").write_text(
                    INDEX.replace("<h1>afterlit</h1>", replacement), encoding="utf-8"
                )
                self.assertTrue(any("exactly one h1" in error for error in check(self.site)))

    def test_font_size_below_11px_or_non_px_is_rejected(self) -> None:
        for value in ("10px", "clamp(10px,2vw,20px)", "1rem", "1em", "100%", "2vw", "small"):
            with self.subTest(value=value):
                (self.site / "styles.css").write_text(
                    CSS + " p {font-size:" + value + ";}", encoding="utf-8"
                )
                self.assertTrue(any("font-size" in error for error in check(self.site)))
        (self.site / "styles.css").write_text(
            CSS + " p {font-size:clamp(12px,2vw,20px);} /* font-size: 1rem; */",
            encoding="utf-8",
        )
        self.assertEqual(check(self.site), [])

    def test_dash_in_js_is_rejected(self) -> None:
        (self.site / "assets/extra.js").write_text('const label = "\u2014";', encoding="utf-8")
        self.assertTrue(any("extra.js js" in error and "U+2014" in error for error in check(self.site)))

    def test_honesty_floor_requires_prealpha_and_private(self) -> None:
        for word in ("Pre-alpha", "private"):
            with self.subTest(word=word):
                (self.site / "index.html").write_text(
                    INDEX.replace(word, "unavailable")
                    .replace("</main>", "<script>Pre-alpha private</script></main>"),
                    encoding="utf-8",
                )
                self.assertTrue(any("visible text must contain" in error for error in check(self.site)))
        (self.site / "index.html").write_text(
            INDEX.replace("private", "<strong>priv</strong>ate"), encoding="utf-8"
        )
        self.assertEqual(check(self.site), [])

    def test_never_claim_phrase_is_rejected(self) -> None:
        for phrase in (
            "pip install", "pypi", "brew install", "homebrew", "compatible with",
            "works with afterlit", "supported devices", "gate 1 passed", "download now",
        ):
            for location in ("visible", "meta"):
                with self.subTest(phrase=phrase, location=location):
                    if location == "visible":
                        self.write_index("<p>" + phrase.upper() + "</p>")
                    else:
                        (self.site / "index.html").write_text(
                            INDEX.replace('content="A local project"', 'content="' + phrase + '"'),
                            encoding="utf-8",
                        )
                    self.assertTrue(any("forbidden claim" in error for error in check(self.site)))
        for extra in (
            "<p>download <strong>now</strong></p>",
            "<p>down<strong>load</strong> now</p>",
            "<p>download\n  now</p>",
        ):
            with self.subTest(extra=extra):
                self.write_index(extra)
                self.assertTrue(any("forbidden claim: download now" in error for error in check(self.site)))


if __name__ == "__main__":
    unittest.main()

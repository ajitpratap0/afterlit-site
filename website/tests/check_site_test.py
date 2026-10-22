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
<link rel="canonical" href="https://example.github.io/afterlit-site/">
<link rel="stylesheet" href="styles.css">
<title>afterlit</title></head>
<body><main id="top"><p>Use --json and a -10px offset.</p>
<a href="#top">Back to top</a></main></body></html>
"""
NOT_FOUND = """<!doctype html><html lang="en"><head>
<link rel="stylesheet" href="/afterlit-site/styles.css">
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
        (self.site / "assets/icon.svg").write_text(SVG, encoding="utf-8")

    def test_valid_project_paths_and_ordinary_hyphens(self) -> None:
        self.assertEqual(check(self.site), [])

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


if __name__ == "__main__":
    unittest.main()

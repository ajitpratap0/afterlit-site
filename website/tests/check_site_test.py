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


    def test_kicker_and_eyebrow_classes_are_rejected(self) -> None:
        for markup in ('<p class="eyebrow">Label</p>', '<p class="small KICKER">Label</p>'):
            with self.subTest(markup=markup):
                self.write_index(markup)
                self.assertTrue(any("kicker or eyebrow" in error for error in check(self.site)))
        self.write_index('<p class="eyebrowse">Not a kicker</p>')
        self.assertEqual(check(self.site), [])

    def test_short_label_directly_before_a_heading_is_rejected(self) -> None:
        for markup in (
            '<span class="number">01 / CAPTURE</span><h3>Observe first.</h3>',
            '<div><small>Step one</small>\n<h2>Observe first.</h2></div>',
            '<p>STAGE ONE</p><h2>Observe first.</h2>',
        ):
            with self.subTest(markup=markup):
                self.write_index(markup)
                self.assertTrue(any("short label element directly before" in error for error in check(self.site)))
        for markup in (
            '<h3><span class="number">01</span> Capture: observe first.</h3>',
            '<p>Observe the vendor app first.</p><h3>Next</h3>',
            '<span>Label</span> then prose<h3>Next</h3>',
            '<span></span><h3>Next</h3>',
            '<span>Label</span><br><p>Body</p><h3>Next</h3>',
        ):
            with self.subTest(markup=markup):
                self.write_index(markup)
                self.assertEqual(check(self.site), [])

    def test_nav_labels_must_not_invite_unavailable_actions(self) -> None:
        for label in ("Contribute", " Download ", "Get <b>started</b>"):
            with self.subTest(label=label):
                self.write_index(f'<nav><a href="#top">{label}</a></nav>')
                self.assertTrue(any("nav label invites" in error for error in check(self.site)))
        self.write_index('<nav><a href="#top">For contributors</a></nav><p><a href="#top">Contribute</a></p>')
        self.assertEqual(check(self.site), [])

    def test_letter_spacing_below_floor_is_rejected(self) -> None:
        css = self.site / "styles.css"
        for value in ("-.05em", "-0.075em", "-1em"):
            with self.subTest(value=value):
                css.write_text(CSS + " h1 { letter-spacing:" + value + " }", encoding="utf-8")
                self.assertTrue(any("letter-spacing tighter" in error for error in check(self.site)))
        css.write_text(
            CSS + " h1 { letter-spacing:-.04em } h2 { letter-spacing:-0.035em } p { letter-spacing:.09em; word-spacing:-1em }",
            encoding="utf-8",
        )
        self.assertEqual(check(self.site), [])

    def test_lamp_light_initial_value_must_match_warm_tone(self) -> None:
        css = self.site / "styles.css"
        registered = "@property --light { syntax:'<color>'; inherits:true; initial-value:%s; } :root { --tone-warm:#efbd7b; }"
        css.write_text(CSS + registered % "#efbd7b", encoding="utf-8")
        self.assertEqual(check(self.site), [])
        css.write_text(CSS + registered % "#e7b477", encoding="utf-8")
        self.assertTrue(any("initial-value must match" in error for error in check(self.site)))


    def test_valid_status_first_hero(self) -> None:
        body = ('<section class="hero"><h1>afterlit</h1>'
                '<p class="hero-status">Pre-alpha. The source is private and there is no public download.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        (self.site / "index.html").write_text(before + '<main id="top">' + body + '</main>' + after, encoding="utf-8")
        self.assertEqual(check(self.site), [])

    def test_hero_without_status_is_rejected(self) -> None:
        body = ('<section class="hero"><h1>afterlit</h1><p>Pre-alpha. The source is private.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        (self.site / "index.html").write_text(before + '<main id="top">' + body + '</main>' + after, encoding="utf-8")
        self.assertIn("index.html: hero must contain exactly one .hero-status", check(self.site))

    def test_hero_status_without_download_status_is_rejected(self) -> None:
        body = ('<section class="hero"><h1>afterlit</h1>'
                '<p class="hero-status">Pre-alpha. The source is private.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        (self.site / "index.html").write_text(before + '<main id="top">' + body + '</main>' + after, encoding="utf-8")
        self.assertIn("index.html: .hero-status must state pre-alpha and no public download", check(self.site))

    def test_hero_status_after_actions_is_rejected(self) -> None:
        body = ('<section class="hero"><h1>afterlit</h1><div class="hero-actions"></div>'
                '<p class="hero-status">Pre-alpha. The source is private and there is no public download.</p>'
                '<p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        (self.site / "index.html").write_text(before + '<main id="top">' + body + '</main>' + after, encoding="utf-8")
        self.assertIn("index.html: hero must lead with status (h1, then .hero-status, then .hero-actions, then .hero-pitch)", check(self.site))

    def test_hero_status_collects_nested_text_and_counts_global_duplicates(self) -> None:
        body = ('<section class="hero other"><h1>afterlit</h1>'
                '<p class="hero-status extra"><strong>Pre-alpha.</strong> The source is private and there is '
                '<span>no public <em>download</em></span>.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        for extra in ('', '<p class="hero-status">Duplicate outside hero.</p>'):
            with self.subTest(extra=extra):
                (self.site / "index.html").write_text(before + '<main id="top">' + body + extra + '</main>' + after, encoding="utf-8")
                errors = check(self.site)
                if extra:
                    self.assertIn("index.html: hero must contain exactly one .hero-status", errors)
                else:
                    self.assertEqual(errors, [])

    def test_hero_missing_actions_or_pitch_is_out_of_order(self) -> None:
        body = ('<section class="hero"><h1>afterlit</h1>'
                '<p class="hero-status">Pre-alpha. The source is private and there is no public download.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p></section><section id="today"></section>')
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        for missing in ('<div class="hero-actions"></div>', '<p class="hero-pitch">x</p>'):
            with self.subTest(missing=missing):
                (self.site / "index.html").write_text(before + '<main id="top">' + body.replace(missing, '') + '</main>' + after, encoding="utf-8")
                self.assertIn("index.html: hero must lead with status (h1, then .hero-status, then .hero-actions, then .hero-pitch)", check(self.site))

    def write_main_body(self, body: str) -> None:
        before, main = INDEX.split('<main id="top">', 1)
        _, after = main.split('</main>', 1)
        (self.site / "index.html").write_text(
            before + '<main id="top">' + body + '</main>' + after, encoding="utf-8"
        )

    def test_today_must_be_first_section_after_hero_closes(self) -> None:
        hero = ('<section class="hero"><h1>afterlit</h1>'
                '<p class="hero-status">Pre-alpha. The source is private and there is no public download.</p>'
                '<div class="hero-actions"></div><p class="hero-pitch">x</p>{nested}</section>')
        message = 'index.html: "What you can do today" (#today) must directly follow the hero'
        for nested, following, valid in (
            ('', '<section id="today"></section>', True),
            ('<section id="nested"><section></section></section>', '<div>Intervening prose</div><section id="today"></section>', True),
            ('<section id="today"></section>', '<section id="other"></section>', False),
            ('', '<section id="other"></section><section id="today"></section>', False),
            ('', '', False),
        ):
            with self.subTest(nested=nested, following=following):
                self.write_main_body(hero.format(nested=nested) + following)
                errors = check(self.site)
                if valid:
                    self.assertEqual(errors, [])
                else:
                    self.assertIn(message, errors)

    def readback_markup(self) -> str:
        return ('<div class="readback"><div class="readback-title"><span>SIMULATED</span> state</div>'
                '<div><span id="req-power"></span><span id="req-level"></span><span id="req-color"></span></div>'
                '<div class="readback-reported" aria-live="polite"><span id="state-power"></span>'
                '<span id="state-level"></span><span id="state-color"></span></div></div>'
                '<p id="color-off-note" hidden>Color stays selected while power is off.</p>')

    def test_valid_simulated_readback_with_one_reported_live_region(self) -> None:
        self.write_index(self.readback_markup())
        self.assertEqual(check(self.site), [])

    def test_readback_sibling_title_and_live_region_do_not_satisfy_each_other(self) -> None:
        markup = self.readback_markup()
        title = '<div class="readback-title"><span>SIMULATED</span> state</div>'
        self.write_index(markup.replace(title, '') + '<div class="readback">' + title + '</div>')
        message = 'index.html: lamp readback must be labelled simulated, with one live region on the reported-back step'
        self.assertEqual(check(self.site).count(message), 2)

    def test_today_follow_rule_requires_a_hero_section(self) -> None:
        self.write_main_body(
            '<div class="hero"><h1>afterlit</h1>'
            '<p class="hero-status">Pre-alpha. The source is private and there is no public download.</p>'
            '<div class="hero-actions"></div><p class="hero-pitch">x</p></div>'
        )
        self.assertEqual(check(self.site), [])

    def test_readback_rejects_missing_or_misplaced_live_region(self) -> None:
        markup = self.readback_markup()
        message = 'index.html: lamp readback must be labelled simulated, with one live region on the reported-back step'
        for broken in (
            markup.replace(' aria-live="polite"', ''),
            markup.replace('class="readback-reported"', 'class="other"'),
            markup.replace('<div><span id="req-power">', '<div aria-live="polite"><span id="req-power">'),
            markup.replace('class="readback"', 'class="readback" aria-live="polite"'),
            markup.replace('class="readback"', 'class="readback" aria-live="polite"').replace(' aria-live="polite"><span id="state-power">', '><span id="state-power">'),
            markup.replace(' aria-live="polite"', '') + '<div class="readback-reported" aria-live="polite"></div>',
        ):
            with self.subTest(broken=broken):
                self.write_index(broken)
                self.assertIn(message, check(self.site))

    def test_readback_requires_simulated_descendant_title_and_all_state_ids(self) -> None:
        markup = self.readback_markup()
        message = 'index.html: lamp readback must be labelled simulated, with one live region on the reported-back step'
        broken_cases = [
            markup.replace('SIMULATED', 'Preview'),
            markup.replace('<div class="readback-title"><span>SIMULATED</span> state</div>', '') + '<div class="readback-title">SIMULATED</div>',
        ]
        broken_cases.extend(markup.replace('id="' + marker + '"', '') for marker in (
            'req-power', 'req-level', 'req-color', 'state-power', 'state-level', 'state-color'
        ))
        for broken in broken_cases:
            with self.subTest(broken=broken):
                self.write_index(broken)
                self.assertIn(message, check(self.site))

    def test_readback_requires_hidden_color_off_note(self) -> None:
        markup = self.readback_markup()
        for broken in (
            markup.replace(' hidden', ''),
            markup.replace('id="color-off-note"', 'id="other-note"'),
        ):
            with self.subTest(broken=broken):
                self.write_index(broken)
                self.assertIn('index.html: lamp readback requires #color-off-note with the hidden attribute', check(self.site))

    def test_new_structure_rules_apply_only_to_index(self) -> None:
        extra = '<section class="hero"></section><div class="readback"></div>'
        (self.site / "404.html").write_text(NOT_FOUND.replace('</body>', extra + '</body>'), encoding="utf-8")
        self.assertEqual(check(self.site), [])

if __name__ == "__main__":
    unittest.main()

"""Check static site references, metadata, and visible typography."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

DASHES = {"\u2013": "en dash", "\u2014": "em dash", "\u2212": "minus sign"}
NEVER_CLAIM = (
    "pip install", "pypi", "brew install", "homebrew", "compatible with",
    "works with afterlit", "supported devices", "gate 1 passed", "download now",
)
CSS_QUOTED = r"""(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')"""
CSS_CONTENT = re.compile(
    r"\bcontent\s*:\s*((?:" + CSS_QUOTED + r"|[^;}])*)", re.IGNORECASE | re.DOTALL
)
CSS_STRING = re.compile(CSS_QUOTED)
CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)""", re.IGNORECASE)


def dash_errors(text: str, source: str) -> list[str]:
    """Report visible dash glyphs without rejecting ASCII flags or CSS values."""
    return [
        f"{source}: {name} (U+{ord(char):04X}) in visible text"
        for char, name in DASHES.items()
        if char in text
    ]


def decode_css_string(raw: str) -> str:
    """Decode CSS escapes left to right so an escaped backslash stays literal."""
    output: list[str] = []
    position = 0
    while position < len(raw):
        if raw[position] != "\\" or position + 1 == len(raw):
            output.append(raw[position])
            position += 1
            continue
        position += 1
        if raw[position] in "\r\n\f":
            if raw[position : position + 2] == "\r\n":
                position += 2
            else:
                position += 1
            continue
        start = position
        while (
            position < len(raw)
            and position - start < 6
            and raw[position] in "0123456789abcdefABCDEF"
        ):
            position += 1
        if position > start:
            codepoint = int(raw[start:position], 16)
            if codepoint == 0 or codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
                codepoint = 0xFFFD
            output.append(chr(codepoint))
            if position < len(raw) and raw[position] in " \t\r\n\f":
                if raw[position : position + 2] == "\r\n":
                    position += 2
                else:
                    position += 1
        else:
            output.append(raw[position])
            position += 1
    return "".join(output)


class SiteParser(HTMLParser):
    """Collect references without executing page content."""

    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.errors: list[str] = []
        self.html_lang = ""
        self.title_count = 0
        self.in_title = False
        self.title_text = ""
        self.meta: dict[str, list[str]] = {}
        self.canonical: list[str] = []
        self.hidden_depth = 0
        self.visible_text: list[str] = []
        self.meta_content: list[str] = []
        self.csp: list[str] = []
        self.h1_count = 0
        self.pre_labels: set[str] = set()
        self.idrefs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attribute, _ in attrs:
            if attribute == "style":
                self.errors.append(f"{self.source}: inline style attribute is not allowed")
            if attribute.startswith("on"):
                self.errors.append(f"{self.source}: inline event handler is not allowed: {attribute}")
        if tag == "style":
            self.errors.append(f"{self.source}: inline style element is not allowed")
        if tag == "script" and not values.get("src"):
            self.errors.append(f"{self.source}: script needs src; inline script is not allowed")
        if tag in {"script", "style"}:
            self.hidden_depth += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "pre":
            label = (values.get("aria-label") or "").strip()
            if values.get("tabindex") != "0" or values.get("role") != "region" or not label:
                self.errors.append(f'{self.source}: pre needs tabindex="0", role="region" and a non-empty aria-label')
            if label:
                if label in self.pre_labels:
                    self.errors.append(f"{self.source}: duplicate pre aria-label: {label}")
                self.pre_labels.add(label)
        for attribute in ("aria-labelledby", "aria-describedby", "aria-controls"):
            self.idrefs.extend((attribute, token) for token in (values.get(attribute) or "").split())
        if tag in {"label", "output"}:
            self.idrefs.extend(("for", token) for token in (values.get("for") or "").split())
        if tag == "a":
            try:
                scheme = urlsplit(values.get("href") or "").scheme
            except ValueError:
                scheme = ""  # Reference validation reports malformed URLs later.
            if scheme in {"http", "https"}:
                if scheme != "https":
                    self.errors.append(f"{self.source}: external link must use HTTPS")
                if not {"noopener", "noreferrer"} <= set((values.get("rel") or "").lower().split()):
                    self.errors.append(f"{self.source}: external link needs rel noopener noreferrer")
        if tag == "html":
            self.html_lang = values.get("lang") or ""
        if tag == "title":
            self.title_count += 1
            self.in_title = True
        element_id = values.get("id")
        if element_id is not None:
            if not element_id:
                self.errors.append(f"{self.source}: empty id")
            elif element_id in self.ids:
                self.errors.append(f"{self.source}: duplicate id: {element_id}")
            else:
                self.ids.add(element_id)
        for attribute in ("href", "src"):
            if attribute in values:
                self.references.append((attribute, values[attribute] or ""))
        for attribute in ("alt", "title", "aria-label"):
            if values.get(attribute):
                self.errors.extend(
                    dash_errors(values[attribute] or "", f"{self.source} {attribute}")
                )
        if tag == "meta":
            self.meta_content.append(values.get("content") or "")
            if (values.get("http-equiv") or "").lower() == "content-security-policy":
                self.csp.append(values.get("content") or "")
            key = values.get("name") or values.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(values.get("content") or "")
        if tag == "link" and (values.get("rel") or "").lower() == "canonical":
            self.canonical.append(values.get("href") or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag in {"script", "style"}:
            self.hidden_depth = max(0, self.hidden_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data
        if not self.hidden_depth:
            self.visible_text.append(data)
            self.errors.extend(dash_errors(data, f"{self.source}:{self.getpos()[0]}"))


def project_prefix(index: SiteParser, errors: list[str]) -> str | None:
    """Map published Pages paths back to this site's directory."""
    if len(index.canonical) > 1:
        errors.append("index.html: duplicate canonical link")
    if not index.canonical:
        return None
    try:
        url = urlsplit(index.canonical[0])
    except ValueError:
        errors.append("index.html: malformed canonical URL")
        return None
    if url.scheme != "https" or not url.netloc or url.fragment or not url.path.endswith("/"):
        errors.append("index.html: canonical URL must be absolute HTTPS with a directory path")
        return None
    return url.path


def resolve_reference(
    raw: str, site: Path, current: Path, prefix: str | None, source: str, errors: list[str]
) -> tuple[Path | None, str]:
    """Resolve local paths without traversal or unrelated site-root paths."""
    if not raw.strip():
        errors.append(f"{source}: empty reference")
        return None, ""
    try:
        url = urlsplit(raw)
    except ValueError:
        errors.append(f"{source}: malformed URL {raw}")
        return None, ""
    if raw.startswith("//") or url.scheme in {"javascript", "data", "file"}:
        errors.append(f"{source}: unsafe reference {raw}")
        return None, ""
    if url.scheme or url.netloc:
        if url.scheme not in {"http", "https", "mailto", "tel"}:
            errors.append(f"{source}: unsupported URL scheme {raw}")
        return None, ""
    path = unquote(url.path)
    if ".." in Path(path).parts or "\\" in path:
        errors.append(f"{source}: unsafe relative path {raw}")
        return None, ""
    if path.startswith("/"):
        if prefix is None or not path.startswith(prefix):
            errors.append(f"{source}: unrelated site-root path {raw}")
            return None, ""
        target = site / path[len(prefix) :]
    else:
        target = current.parent / path if path else current
    target = target.resolve()
    if not target.is_relative_to(site):
        errors.append(f"{source}: unsafe relative path {raw}")
        return None, ""
    if target.is_dir():
        target /= "index.html"
    if not target.is_file():
        errors.append(f"{source}: missing local file {raw}")
        return None, ""
    return target, unquote(url.fragment)


def check(site: Path) -> list[str]:
    site = site.resolve()
    index = site / "index.html"
    if not index.is_file():
        return [f"missing {index}"]
    errors: list[str] = []
    pages: dict[Path, SiteParser] = {}
    for html in sorted(site.rglob("*.html")):
        parser = SiteParser(str(html.relative_to(site)))
        parser.feed(html.read_text(encoding="utf-8"))
        parser.close()
        pages[html] = parser
        errors.extend(parser.errors)
        for attribute, token in parser.idrefs:
            if token not in parser.ids:
                errors.append(f"{parser.source}: dangling id reference in {attribute}: {token}")

    parser = pages[index]
    if parser.h1_count != 1:
        errors.append("index.html: expected exactly one h1")
    if len(parser.csp) != 1:
        errors.append("index.html: expected one Content-Security-Policy meta tag")
    for policy in parser.csp:
        directives: dict[str, list[str]] = {}
        for directive in policy.split(";"):
            parts = directive.split()
            if not parts:
                continue
            name, tokens = parts[0].lower(), parts[1:]
            if name in directives:
                errors.append(f"index.html: duplicate CSP directive: {name}")
            directives[name] = tokens
            if any("unsafe-" in token.lower() for token in tokens):
                errors.append(f"index.html: CSP {name} contains an unsafe- token")
        for name in ("default-src", "script-src", "style-src", "connect-src", "form-action", "object-src", "base-uri"):
            required = ["'self'"] if name in {"script-src", "style-src"} else ["'none'"]
            if directives.get(name) != required:
                errors.append(f"index.html: CSP {name} must be exactly {' '.join(required)}")
    visible = " ".join("".join(parser.visible_text).lower().split())
    for required in ("pre-alpha", "private"):
        if required not in visible:
            errors.append(f"index.html: visible text must contain {required}")
    claims = visible + " " + " ".join(parser.meta_content).lower()
    for phrase in NEVER_CLAIM:
        if phrase in claims:
            errors.append(f"index.html: forbidden claim: {phrase}")
    if not parser.html_lang.strip():
        errors.append("index.html: missing html lang")
    if parser.title_count != 1 or not parser.title_text.strip():
        errors.append("index.html: expected one non-empty title")
    for key in ("viewport", "description", "og:image:alt", "color-scheme"):
        if len(parser.meta.get(key, [])) != 1 or not parser.meta[key][0].strip():
            errors.append(f"index.html: expected one non-empty {key} meta tag")
    if parser.meta.get("color-scheme") and parser.meta["color-scheme"] != ["light"]:
        errors.append("index.html: color-scheme must be light")
    prefix = project_prefix(parser, errors)
    asset_versions: set[str] = set()

    for html, page in pages.items():
        for attribute, raw in page.references:
            target, anchor = resolve_reference(
                raw, site, html, prefix, f"{page.source} {attribute}", errors
            )
            if target is not None and target.suffix.lower() in {".css", ".js"}:
                versions = parse_qs(urlsplit(raw).query, keep_blank_values=True).get("v", [])
                if len(versions) != 1 or not versions[0].strip():
                    errors.append(f"{page.source}: local CSS/JS reference needs one non-empty ?v= version: {raw}")
                else:
                    asset_versions.add(versions[0])
            if target is not None and raw.endswith("#"):
                errors.append(f"{page.source}: empty anchor {raw}")
            elif target in pages and anchor and anchor not in pages[target].ids:
                errors.append(f"{page.source}: dangling anchor {raw}")

    if len(asset_versions) > 1:
        errors.append("local CSS/JS asset versions differ: " + ", ".join(sorted(asset_versions)))

    for css in site.rglob("*.css"):
        source = str(css.relative_to(site))
        content = re.sub(r"/\*.*?\*/", "", css.read_text(encoding="utf-8"), flags=re.DOTALL)
        for value in re.findall(r"(?<![\w-])font-size\s*:\s*([^;}]+)", content, re.IGNORECASE):
            value = value.strip()
            size = re.fullmatch(r"(\d+(?:\.\d+)?)px", value, re.IGNORECASE)
            if not size:
                size = re.match(r"clamp\(\s*(\d+(?:\.\d+)?)px\s*,", value, re.IGNORECASE)
            if not size or float(size.group(1)) < 11:
                errors.append(f"{source}: font-size must use px or clamp with a minimum of 11px: {value}")
        for value in CSS_CONTENT.findall(content):
            for match in CSS_STRING.finditer(value):
                decoded = decode_css_string(match.group()[1:-1])
                errors.extend(dash_errors(decoded, f"{source} content"))
        for raw in CSS_URL.findall(content):
            resolve_reference(raw.strip(), site, css, prefix, f"{source} url()", errors)

    for js in site.rglob("*.js"):
        errors.extend(dash_errors(js.read_text(encoding="utf-8"), f"{js.relative_to(site)} js"))

    for svg in site.rglob("*.svg"):
        source = str(svg.relative_to(site))
        try:
            data = svg.read_bytes()
            if len(data) > 1_000_000 or b"<!DOCTYPE" in data or b"<!ENTITY" in data:
                errors.append(f"{source}: SVG is too large or contains a DTD")
                continue
            root = ET.fromstring(data)  # noqa: S314 - bounded local SVG without DTD/entities
        except ET.ParseError as exc:
            errors.append(f"{source}: invalid SVG: {exc}")
            continue
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] in {"text", "title", "desc"}:
                errors.extend(dash_errors("".join(element.itertext()), f"{source} text"))
    return errors


def main() -> int:
    site = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "website"
    )
    errors = check(site)
    if errors:
        for error in errors:
            print(f"site check: {error}", file=sys.stderr)
        return 1
    print(f"site check: OK ({site})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

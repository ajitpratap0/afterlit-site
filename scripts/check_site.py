"""Check the static landing page's local links and essential metadata."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class SiteParser(HTMLParser):
    """Collect references without executing page content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.errors: list[str] = []
        self.html_lang = ""
        self.title_count = 0
        self.in_title = False
        self.title_text = ""
        self.meta: dict[str, list[str]] = {}
        self.canonical: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang") or ""
        if tag == "title":
            self.title_count += 1
            self.in_title = True
        element_id = values.get("id")
        if element_id is not None:
            if not element_id:
                self.errors.append("empty id")
            elif element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            else:
                self.ids.add(element_id)
        for attribute in ("href", "src"):
            if attribute in values:
                self.references.append((attribute, values[attribute] or ""))
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(values.get("content") or "")
        if tag == "link" and (values.get("rel") or "").lower() == "canonical":
            self.canonical.append(values.get("href") or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data


def local_reference(raw: str, site: Path, source: str, errors: list[str]) -> None:
    """Validate a local URL without allowing it to leave the static site tree."""
    if not raw.strip():
        errors.append(f"{source}: empty reference")
        return
    url = urlsplit(raw)
    if raw.startswith("//") or url.scheme in {"javascript", "data", "file"}:
        errors.append(f"{source}: unsafe reference {raw}")
        return
    if url.scheme or url.netloc:
        if url.scheme not in {"http", "https", "mailto", "tel"}:
            errors.append(f"{source}: unsupported URL scheme {raw}")
        return
    path = unquote(url.path)
    if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
        errors.append(f"{source}: unsafe relative path {raw}")
        return
    if path:
        target = (site / path).resolve()
        if not target.is_relative_to(site.resolve()) or not target.is_file():
            errors.append(f"{source}: missing local file {raw}")


def check(site: Path) -> list[str]:
    index = site / "index.html"
    if not index.is_file():
        return [f"missing {index}"]
    parser = SiteParser()
    parser.feed(index.read_text(encoding="utf-8"))
    parser.close()
    errors = parser.errors
    if not parser.html_lang.strip():
        errors.append("missing html lang")
    if parser.title_count != 1 or not parser.title_text.strip():
        errors.append("expected one non-empty title")
    for key in ("viewport", "description"):
        if len(parser.meta.get(key, [])) != 1 or not parser.meta[key][0].strip():
            errors.append(f"expected one non-empty {key} meta tag")
    if len(parser.canonical) > 1:
        errors.append("duplicate canonical link")
    for canonical in parser.canonical:
        url = urlsplit(canonical)
        if url.scheme != "https" or not url.netloc or url.fragment:
            errors.append("canonical URL must be absolute HTTPS without a fragment")
    for attribute, raw in parser.references:
        if raw.startswith("#"):
            anchor = unquote(raw[1:])
            if not anchor or anchor not in parser.ids:
                errors.append(f"dangling anchor: {raw}")
        else:
            local_reference(raw, site, attribute, errors)
    for css in site.rglob("*.css"):
        for raw in re.findall(r"url\(\s*['\"]?([^'\")]+)", css.read_text(encoding="utf-8")):
            local_reference(raw.strip(), site, f"{css.relative_to(site)} url()", errors)
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

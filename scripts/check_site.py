#!/usr/bin/env python3
"""Check local links, fragments, images, scripts and CSS in a rendered Commons site."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.links.append((tag, attrs[key]))
        if attrs.get('srcset') and not attrs['srcset'].startswith('data:'):
            self.links.extend((tag, item.strip().split()[0]) for item in attrs['srcset'].split(',') if item.strip())


def check(root: Path) -> tuple[int, list[str]]:
    root = root.resolve()
    documents = {path: Document(path.read_text(encoding='utf-8')) for path in root.rglob('*.html')}
    problems = []
    count = 0

    def inspect(source: Path, tag: str, href: str):
        nonlocal count
        url = urlsplit(href)
        if url.scheme or url.netloc or href.startswith('#/'):
            return
        count += 1
        target = (root / unquote(url.path).lstrip('/') if url.path.startswith('/')
                  else source.parent / unquote(url.path)) if url.path else source
        target = target.resolve()
        if target.is_dir():
            target /= 'index.html'
        label = f'{source.relative_to(root)}: {href}'
        if not target.is_relative_to(root) or not target.is_file():
            problems.append('Missing target: ' + label)
        elif tag == 'a' and url.fragment and target in documents:
            if unquote(url.fragment) not in documents[target].ids:
                problems.append('Missing fragment: ' + label)

    for path, document in documents.items():
        for tag, href in document.links:
            inspect(path, tag, href)
    for path in root.rglob('*.css'):
        for match in re.finditer(r'url\(\s*[\'"]?([^\)\'"\s]+)', path.read_text(encoding='utf-8')):
            if not match[1].startswith('#'):
                inspect(path, 'css', match[1])
    for required in ['index.html', 'tas2/index.html', 'tej3-4/index.html', 'ttj3-4/index.html',
                     'lore/index.html', 'lore/from-a-pen-and-paper-mark-to-a-crest.html',
                     'resources/nice-design-process.html', 'resources/nice-design-process-slides.html',
                     'tools/nice-design-tool.html', 'glossary/index.html']:
        if not (root / required).is_file():
            problems.append('Missing main page: ' + required)
    for path in root.rglob('*.webp'):
        content = path.read_bytes()
        if content[:4] != b'RIFF' or content[8:12] != b'WEBP' or int.from_bytes(content[4:8], 'little') + 8 != len(content):
            problems.append('Invalid or truncated WebP: ' + str(path.relative_to(root)))
    return count, sorted(set(problems))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', type=Path, default=Path('site/_site'))
    args = parser.parse_args()
    count, problems = check(args.output)
    for problem in problems:
        print(problem)
    print(f'Checked {count} local references; {len(problems)} failures.')
    raise SystemExit(bool(problems))

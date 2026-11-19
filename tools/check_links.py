"""Checks every internal link and asset in site/ resolves to a file, the way Cloudflare Pages
serves them (/about -> about.html, /ograder/ -> ograder/index.html), and that #anchors exist.

External links are checked separately by lychee in .github/workflows/links.yml.
Run: python3 tools/check_links.py
"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        for key in ('href', 'src'):
            if a.get(key):
                self.links.append((tag, a[key]))
        if a.get('srcset'):
            self.links += [(tag, part.split()[0]) for part in a['srcset'].split(',') if part.strip()]


def parse(path):
    p = Links()
    p.feed(open(path, encoding='utf-8').read())
    return p


def resolve(page, target):
    """The file a same-site link points to, or None if nothing serves it."""
    path = unquote(urlsplit(target).path)
    if path.startswith('/'):
        base = os.path.join(SITE, path.lstrip('/'))
    else:
        base = os.path.join(os.path.dirname(page), path) if path else page
    base = os.path.normpath(base)
    for cand in (base, base + '.html', os.path.join(base, 'index.html')):
        if os.path.isfile(cand) and cand.startswith(SITE):
            return cand
    return None


def main():
    pages = [os.path.join(d, f) for d, _, fs in os.walk(SITE) for f in fs if f.endswith('.html')]
    parsed = {p: parse(p) for p in pages}
    errors = []
    for page, info in sorted(parsed.items()):
        rel = os.path.relpath(page, SITE)
        for tag, link in info.links:
            if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)', link):
                continue
            target = resolve(page, link)
            if target is None:
                errors.append(f'{rel}: <{tag}> {link} -> no such file')
                continue
            frag = urlsplit(link).fragment
            if frag and target.endswith('.html'):
                ids = parsed[target].ids if target in parsed else set()
                # The O-Grader uses #climb-name hashes that its script resolves at runtime.
                if frag not in ids and '/ograder/' not in target:
                    errors.append(f'{rel}: {link} -> no element with id "{frag}"')
    for e in errors:
        print('BROKEN', e)
    print(f'{len(pages)} pages checked, {len(errors)} broken internal links')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

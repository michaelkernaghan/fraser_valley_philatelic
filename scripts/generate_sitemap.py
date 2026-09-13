#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages actually present in the repo.

Run from the repo root:  python scripts/generate_sitemap.py

A page is included unless it carries a `noindex` robots tag (the script reads the
file to decide, so there is no list to keep in sync) or appears in EXCLUDE below
with a stated reason.

URLs are written without the .html extension, because Netlify's Pretty URLs
rewrites internal links that way and serves both forms with a 200. The canonical
tags in each page use the same form, so the two cannot disagree. If this site ever
moves off Netlify, set EXTENSIONLESS = False and re-run: .html works anywhere,
/meetings does not.

`lastmod` comes from each file's last git commit, falling back to its mtime for a
file that is not committed yet - dating a new page 1970 would tell search engines
it is ancient.
"""
import datetime
import pathlib
import re
import subprocess

SITE = 'https://fraser-valley-philatelic.netlify.app'
EXTENSIONLESS = True
ROOT = pathlib.Path(__file__).resolve().parents[1]

EXCLUDE = {}   # nothing deliberately withheld beyond the noindex pages


def url_for(filename: str) -> str:
    if filename == 'index.html':
        return SITE + '/'
    slug = filename[:-5] if EXTENSIONLESS and filename.endswith('.html') else filename
    return f'{SITE}/{slug}'


def lastmod(path: pathlib.Path) -> str:
    out = subprocess.run(
        ['git', 'log', '-1', '--format=%ad', '--date=short', '--', path.name],
        capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if out:
        return out
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def main() -> None:
    included, skipped = [], []
    for p in sorted(ROOT.glob('*.html')):
        txt = p.read_text(encoding='utf-8', errors='ignore')
        if re.search(r'<meta\s+name="robots"[^>]*noindex', txt, re.I):
            skipped.append((p.name, 'noindex'))
        elif p.name in EXCLUDE:
            skipped.append((p.name, EXCLUDE[p.name]))
        else:
            included.append(p)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in included:
        lines += ['    <url>',
                  f'        <loc>{url_for(p.name)}</loc>',
                  f'        <lastmod>{lastmod(p)}</lastmod>',
                  '    </url>']
    lines.append('</urlset>')

    (ROOT / 'sitemap.xml').write_text('\n'.join(lines) + '\n',
                                      encoding='utf-8', newline='')
    print(f'sitemap.xml: {len(included)} urls')
    for name, why in skipped:
        print(f'  skipped {name}  ({why})')


if __name__ == '__main__':
    main()

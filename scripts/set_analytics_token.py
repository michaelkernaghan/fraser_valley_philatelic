#!/usr/bin/env python3
"""Set the Cloudflare Web Analytics beacon token across every page.

The beacon ships with the placeholder CF_BEACON_TOKEN, so analytics is installed
but inert. To turn it on:

  1. dash.cloudflare.com -> Analytics & Logs -> Web Analytics -> Add a site
  2. Enter fraservalleystampclub.com. Cloudflare shows a snippet
     containing a 32-character hex token.
  3. From the repo root:

       python scripts/set_analytics_token.py <token>

  4. Commit and push. Data appears in the Cloudflare dashboard within minutes.

This site needs its own token; a token from another site will not report here.
Re-run with a new token to rotate, or --clear to put the placeholder back, which
switches analytics off without removing the tag.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLACEHOLDER = 'CF_BEACON_TOKEN'
PATTERN = re.compile(r'(data-cf-beacon=\'\{"token": ")([^"]*)("\}\')')


def main() -> None:
    args = [a for a in sys.argv[1:] if a]
    if not args:
        sys.exit('usage: set_analytics_token.py <token> | --clear')

    if args[0] == '--clear':
        token = PLACEHOLDER
    else:
        token = args[0]
        if not re.fullmatch(r'[0-9a-f]{32}', token):
            sys.exit(f'refusing: {token!r} is not a 32-character hex token. '
                     'Copy it from the snippet Cloudflare shows you.')

    changed = 0
    for p in sorted(ROOT.glob('*.html')):
        txt = p.read_text(encoding='utf-8', errors='ignore')
        new, n = PATTERN.subn(lambda m: m.group(1) + token + m.group(3), txt)
        if n and new != txt:
            p.write_text(new, encoding='utf-8', newline='')
            changed += 1

    state = 'placeholder (analytics off)' if token == PLACEHOLDER else 'live token'
    print(f'set {state} on {changed} pages')
    if not changed:
        print('nothing to do - every page already carries that value')


if __name__ == '__main__':
    main()

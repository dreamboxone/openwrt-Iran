#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_cf_logo.py  --  Passwall2 status page: Baidu -> Cloudflare

Passwall2's connection-check widget (luasrc/view/passwall2/global/status.htm)
embeds every check logo as an inline base64 data-URI, NOT as a separate image
file. That is why the old "find *baidu*.png and overwrite it" approach never
changed anything: there is no such file. This script edits the base64 inline.

It does three things, scoped ONLY to the Baidu check block:
  1. Repoints the ping URL   : https://www.baidu.com -> https://www.cloudflare.com
  2. Renames the label       : "Baidu Connection"     -> "Cloudflare Connection"
  3. Swaps the embedded logo : Baidu base64            -> official Cloudflare base64

The embedded logo below is the OFFICIAL Cloudflare cloud mark (64x64 PNG with
transparent background, colors #F6821F / #FBAD41). A 256px copy is kept in
assets/cloudflare-logo-256.png for reference.

Usage: python3 patch_cf_logo.py /path/to/status.htm
"""
import re
import sys

CF_B64 = "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"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch_cf_logo.py <status.htm>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()
    orig = html

    # 1) ping target
    html = html.replace("https://www.baidu.com", "https://www.cloudflare.com")
    # 2) visible label
    html = html.replace("Baidu Connection", "Cloudflare Connection")

    # 3) logo: first data-URI <img> AFTER the baidu check handler
    idx = html.find("check_connect('baidu'")
    if idx == -1:
        print("ERROR: baidu connection block not found in status.htm", file=sys.stderr)
        return 1

    m = re.search(r'src="data:image/[^;]+;base64,[^"]*"', html[idx:])
    if not m:
        print("ERROR: baidu logo data-URI not found in status.htm", file=sys.stderr)
        return 1

    start, end = idx + m.start(), idx + m.end()
    html = html[:start] + 'src="data:image/png;base64,' + CF_B64 + '"' + html[end:]

    if html == orig:
        print("ERROR: nothing was changed (already patched?)", file=sys.stderr)
        return 1

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("OK: Cloudflare logo, label and ping URL applied to", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

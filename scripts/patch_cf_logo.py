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
  3. Swaps the embedded logo : Baidu base64            -> Cloudflare base64

Usage: python3 patch_cf_logo.py /path/to/status.htm
"""
import re
import sys

# 64x64 Cloudflare cloud logo (PNG), base64-encoded and embedded so the build
# needs no image tooling. Source SVG lives in assets/cloudflare-icon.svg.
CF_B64 = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAAEdklEQVR4nO2ZXWwUVRTHf+fubAGLLAUJSrRUolGIGhWNBIq0QCAkJHyUFqPBiFEDDz7qm9I2RDEaH4xGovIAGh4W2oLwooaySpDw4osmRg0B8SNEDCKlXbpz9x4fAJOWpd3Z7mwr3t/TZO455/7PmTtnZu6A5/+NjNbEmm5OWDk3H6OLQOuBmcBUYArwJ3AWOI3IYefk86qmQ9+KoOXWUfECaOeSqdbp8yq6SS4nXRzCDwKvJWp0tzRmbLn0VKwA2tpqwvu/fE5gG1BTahyBE+rMxmTzoSPl0FWRAmh64TSbCPYAi8oU0qLyStDU/cZIb4vYC9Df+fjshCYOKswqd2xR3R6sy2weSQxTLjGFyHY11BlNdMeRPICKbAo7GraMJEZsK0C7GiZblaMoc+Ka4yqiuiZYl9lXim9sKyDv5O1KJA/gRN7RdMPEUnxjKUDY2bhI4Zk4YhdC4A4byKul+MazApS3qPQ7hrJZ9y+4OapbENUh3LNkoRi3UZF5oLcCl0C/U2RfMsh9bPPj70PdI1HjloGJoU2uBz6K4lT0VdKD9TW2P9gBsmYIs9+BX4DHoogoH3os2ZSZH8WjqAJoevkUG+SOVKqpjQAXBLnJsupoT7EORfUAa8Kd/4HkAYy14x6K5DCcQdjRsBTRlaVrqiwqOjeK/bAFUJFnS5dTeQRuj2I//C2gLChZzWigsj+K+bAFELitdDWVRn4K1nZH+kwupgnmSlRTeYQPon4eF3wR0l3LqsNqe48xTHdOzwlUl0dhfCicStrse1H9/i2AppdPsSZ8AaHFEj4gkFA3ipuG0bgozjwtLceyUR0FwHYtXqFOdwG3lF1azCicEidPJZu7vx48lm2dVasm/z1wFuU34LgY+XR8/tRX0ooDkFxX41xxHAOSFdZeDOfhmnu6VyCn8KsiXckLbrtszFwq5NzbXrdJ0PevGRC+EacvT9hy+lAgjjbiT/54nsSTAOPyto+bbP+A0b4glJbMxXJPKrCi4IDysIp80ds2c6uEHY3ngVS5Jx8C5fKVHXyyx4C9fCx/C5pSyAKDr24IckaE3Yk13XuH6vp97TP/AKYNJSYAqiKnMDKEAtviAjVXMulB+VCF168fQlFlte1s/EzTuk5aMhc13ZyQlj35QYbDruwgL+ZBIy7yRkJcJMOqk9bkHi3SfLk18gmwGi6kgHMDRoUDKBuGCjAmn3L9exvuNYZVxdqrSg9of1VTZseA8613TcomwndRVnKdnzFjsgBRyXUsfhHR+qq1h9cXGtdWTG/yzmlBKKm8CVMJkVReeUmQZZG3xMYiRtxJpzJv8Hl9c3p1X9+EpVlx88S56c4wCUzKKTUCs6GEPcExiZNxCAMaYLatdkM2K9tEdAYIcqXDDl7ysf4ZqhSK3H31EQrQ217XpiK7gBnD+d4QBQic2a3CXwB97XVPCFr0P4IbogkC9KeXzKk68/OJ7PnwR6C2WL8bpgAA2a219epk52jr8Hg8Ho/H4/F4PB6Px+PxeDwej8fj8XjGIP8Avyd7kUKNYNAAAAAASUVORK5CYII="


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

#!/usr/bin/env python3
"""Find the latest stable OpenWrt and Passwall2 releases for the build."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request


OPENWRT_RELEASES_API = "https://api.github.com/repos/openwrt/openwrt/releases?per_page=100"
PASSWALL2_RELEASES_API = (
    "https://api.github.com/repos/Openwrt-Passwall/openwrt-passwall2/releases?per_page=100"
)
DEVICE_IMAGE = (
    "https://downloads.openwrt.org/releases/{version}/targets/ipq40xx/chromium/"
    "openwrt-{version}-ipq40xx-chromium-google_wifi-squashfs-sysupgrade.bin"
)
STABLE_OPENWRT_TAG = re.compile(r"^v(\d+\.\d+\.\d+)$")


def request_json(url: str, token: str = "") -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "openwrt-Iran-update-checker",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def url_exists(url: str) -> bool:
    request = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "openwrt-Iran-update-checker"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return 200 <= response.status < 400
    except urllib.error.HTTPError:
        return False


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def latest_openwrt(releases: object) -> str:
    candidates: list[str] = []
    for release in releases if isinstance(releases, list) else []:
        if release.get("draft") or release.get("prerelease"):
            continue
        match = STABLE_OPENWRT_TAG.fullmatch(release.get("tag_name", ""))
        if match:
            candidates.append(match.group(1))

    for version in sorted(set(candidates), key=version_key, reverse=True):
        if url_exists(DEVICE_IMAGE.format(version=version)):
            return version
    raise RuntimeError("No stable OpenWrt release containing the Google WiFi image was found")


def latest_passwall2(releases: object) -> str:
    for release in releases if isinstance(releases, list) else []:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "").strip()
        if tag:
            return tag
    raise RuntimeError("No stable Passwall2 release was found")


def release_exists(repository: str, tag: str, token: str) -> bool:
    url = f"https://api.github.com/repos/{repository}/releases/tags/{tag}"
    try:
        request_json(url, token)
        return True
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise


def write_output(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"{name}={value}\n")
    else:
        print(f"{name}={value}")


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    requested_openwrt = os.environ.get("INPUT_OPENWRT_VERSION", "").strip().removeprefix("v")
    requested_passwall2 = os.environ.get("INPUT_PASSWALL2_TAG", "").strip()
    force = os.environ.get("INPUT_FORCE_BUILD", "false").lower() == "true"

    openwrt_version = requested_openwrt or latest_openwrt(
        request_json(OPENWRT_RELEASES_API, token)
    )
    passwall2_tag = requested_passwall2 or latest_passwall2(
        request_json(PASSWALL2_RELEASES_API, token)
    )

    safe_passwall2_tag = re.sub(r"[^0-9A-Za-z._-]+", "-", passwall2_tag).strip("-")
    release_tag = f"gale-openwrt-{openwrt_version}-passwall2-{safe_passwall2_tag}"
    already_released = bool(
        repository and release_exists(repository, release_tag, token)
    )
    should_build = force or not already_released

    write_output("openwrt_version", openwrt_version)
    write_output("openwrt_tag", f"v{openwrt_version}")
    write_output("passwall2_tag", passwall2_tag)
    write_output("release_tag", release_tag)
    write_output("should_build", str(should_build).lower())

    print(f"OpenWrt:  {openwrt_version}")
    print(f"Passwall2: {passwall2_tag}")
    print(f"Release:   {release_tag}")
    print(f"Build:     {should_build}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

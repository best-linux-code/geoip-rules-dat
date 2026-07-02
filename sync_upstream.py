from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Optional, Sequence

from geoip_gen.upstream import (
    GEOIP_SHA_URL,
    GEOIP_URL,
    GEOSITE_SHA_URL,
    GEOSITE_URL,
    UPSTREAM_RELEASE_API_URL,
    parse_sha256sum,
    verify_sha256,
)


class Asset(NamedTuple):
    name: str
    data_url: str
    checksum_url: str


ASSETS = (
    Asset("geoip.dat", GEOIP_URL, GEOIP_SHA_URL),
    Asset("geosite.dat", GEOSITE_URL, GEOSITE_SHA_URL),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def release_tag(response_url: str) -> str:
    marker = "/releases/download/"
    if marker not in response_url:
        return "latest"
    tail = response_url.split(marker, 1)[1]
    return tail.split("/", 1)[0]


def fetch(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "geoip-rules-dat"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read(), response.geturl()


def latest_release_tag() -> str:
    data, _ = fetch(UPSTREAM_RELEASE_API_URL)
    payload = json.loads(data.decode("utf-8"))
    return str(payload["tag_name"])


def sync_asset(root: Path, asset: Asset) -> tuple[str, str]:
    checksum_text, _ = fetch(asset.checksum_url)
    expected = parse_sha256sum(checksum_text.decode("utf-8"))
    data, resolved_url = fetch(asset.data_url)
    verify_sha256(data, expected)
    (root / asset.name).write_bytes(data)
    (root / (asset.name + ".sha256")).write_text(expected + "  " + asset.name + "\n", encoding="utf-8")
    return expected, release_tag(resolved_url)


def sync(root: Path) -> dict[str, object]:
    root.mkdir(parents=True, exist_ok=True)
    checksums = {}
    tag = latest_release_tag()
    for asset in ASSETS:
        checksum, _ = sync_asset(root, asset)
        checksums[asset.name] = checksum
    payload: dict[str, object] = {
        "source": "Loyalsoldier/v2ray-rules-dat",
        "release_tag": tag,
        "timestamp_utc": utc_now(),
        "assets": checksums,
        "urls": {asset.name: asset.data_url for asset in ASSETS},
    }
    (root / "UPSTREAM_PROVENANCE.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync full v2ray-rules-dat GeoIP and GeoSite artifacts.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    payload = sync(args.root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

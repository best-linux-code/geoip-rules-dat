from __future__ import annotations

import hashlib
from typing import Final


UPSTREAM_BASE_URL: Final = "https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download"
UPSTREAM_RELEASE_API_URL: Final = "https://api.github.com/repos/Loyalsoldier/v2ray-rules-dat/releases/latest"
GEOIP_URL: Final = UPSTREAM_BASE_URL + "/geoip.dat"
GEOIP_SHA_URL: Final = UPSTREAM_BASE_URL + "/geoip.dat.sha256sum"
GEOSITE_URL: Final = UPSTREAM_BASE_URL + "/geosite.dat"
GEOSITE_SHA_URL: Final = UPSTREAM_BASE_URL + "/geosite.dat.sha256sum"


def parse_sha256sum(text: str) -> str:
    digest = text.strip().split()[0]
    if len(digest) != 64:
        raise ValueError("sha256 digest must be 64 hex characters")
    int(digest, 16)
    return digest.lower()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_sha256(data: bytes, expected: str) -> None:
    actual = sha256_bytes(data)
    if actual != expected.lower():
        raise ValueError("sha256 mismatch: expected " + expected + ", got " + actual)

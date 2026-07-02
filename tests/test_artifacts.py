from __future__ import annotations

import unittest
from pathlib import Path

from geoip_gen.codec import decode_geoip_list


ROOT = Path(__file__).resolve().parents[1]


class ArtifactTest(unittest.TestCase):
    def test_slim_geoip_when_decoded_has_only_cn_and_private(self) -> None:
        entries = decode_geoip_list((ROOT / "geoip-only-cn-private.dat").read_bytes())
        self.assertEqual(tuple(entry.code for entry in entries), ("CN", "PRIVATE"))

    def test_full_geoip_when_decoded_has_many_tags(self) -> None:
        geoip = ROOT / "geoip.dat"
        if not geoip.exists():
            self.skipTest("geoip.dat has not been synced yet")
        entries = decode_geoip_list(geoip.read_bytes())
        self.assertGreater(len(entries), 50)

    def test_geosite_when_synced_is_non_empty_binary(self) -> None:
        geosite = ROOT / "geosite.dat"
        if not geosite.exists():
            self.skipTest("geosite.dat has not been synced yet")
        self.assertGreater(geosite.stat().st_size, 100_000)
        self.assertFalse(geosite.read_bytes().startswith(b"#"))


if __name__ == "__main__":
    unittest.main()

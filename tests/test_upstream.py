from __future__ import annotations

import unittest

from geoip_gen.upstream import parse_sha256sum, verify_sha256


class UpstreamTest(unittest.TestCase):
    def test_parse_sha256sum_when_standard_file_line(self) -> None:
        digest = "0" * 64
        self.assertEqual(parse_sha256sum(digest + "  geoip.dat\n"), digest)

    def test_verify_sha256_when_data_matches(self) -> None:
        verify_sha256(b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_verify_sha256_when_data_differs(self) -> None:
        with self.assertRaises(ValueError):
            verify_sha256(b"abc", "0" * 64)


if __name__ == "__main__":
    unittest.main()

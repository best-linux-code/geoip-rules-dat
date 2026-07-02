#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional, Sequence

from geoip_gen.builder import generate, inspect
from geoip_gen.models import BuildResult, Paths, build_paths


def print_result(result: BuildResult, paths: Paths) -> None:
    payload = {
        "output": str(paths.output),
        "sha256": result.output_sha256,
        "counts": {"CN": result.cn_count, "PRIVATE": result.private_count},
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build and inspect a CN plus PRIVATE GeoIP dat.")
    parser.add_argument("mode", nargs="?", choices=("generate", "inspect"), default="generate")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent))
    args = parser.parse_args(argv)
    paths = build_paths(Path(args.root))
    result = generate(paths) if args.mode == "generate" else inspect(paths)
    print_result(result, paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

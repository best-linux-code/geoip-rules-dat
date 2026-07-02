# geoip-rules-dat

V2Ray/Xray rule artifacts with two update paths:

- full upstream `geoip.dat` and `geosite.dat`, synced from `Loyalsoldier/v2ray-rules-dat`
- custom slim `geoip-only-cn-private.dat`, generated locally from `17mon/china_ip_list` plus PRIVATE ranges

The custom generator is pure Python standard library code. No Go, protoc, Docker, pip, uv, or protobuf package is required.

## Artifacts

```text
geoip.dat                    full upstream GeoIP data
geosite.dat                  full upstream GeoSite domain data
geoip-only-cn-private.dat    custom slim GeoIP file
```

The slim file contains only two tags:

- `geoip:cn`, generated from `17mon/china_ip_list`
- `geoip:private`, generated from the standard private and special-purpose IP ranges used by V2Ray-compatible GeoIP data

## Current Artifact

```text
geoip-only-cn-private.dat
CN:      7456
PRIVATE: 21
SHA256:  303d175dad44a2c342645504e3ac50f95c4fa5c798901737bdb84e7a8a8071f6
```

`PROVENANCE.json` records the source URL, input checksum, output checksum, generation timestamp, entry counts, and private CIDR list.

`UPSTREAM_PROVENANCE.json` records the upstream `Loyalsoldier/v2ray-rules-dat` release tag and checksums used for `geoip.dat` and `geosite.dat`.

## Usage

Regenerate from the committed `china_ip_list.txt`:

```bash
python3 generate_geoip_cn_private.py generate
```

Inspect and validate the committed artifact without network access:

```bash
python3 generate_geoip_cn_private.py inspect
```

Sync the full upstream files:

```bash
python3 sync_upstream.py
```

All commands use only the Python standard library.

## v2rayNG

Put the required files in v2rayNG's assets directory, usually:

```text
Android/data/com.v2ray.ang/files/assets/
```

For normal rules that use `geoip:` and `geosite:`, place the full upstream files there as:

```text
geoip.dat
geosite.dat
```

Reference the custom slim file with `ext:` rules:

```text
ext:geoip-only-cn-private.dat:cn
ext:geoip-only-cn-private.dat:private
```

This file is intentionally slim. It does not contain other country or service tags such as `geoip:us`, `geoip:jp`, or `geoip:telegram`.

## Automatic Updates

`.github/workflows/update.yml` runs weekly and can also be started manually. The workflow:

1. Fetches the latest `china_ip_list.txt` from the source URL in `geoip_gen/models.py`.
2. Regenerates `geoip-only-cn-private.dat`, checksum, and provenance.
3. Syncs full upstream `geoip.dat` and `geosite.dat` from `Loyalsoldier/v2ray-rules-dat`.
4. Runs offline inspectors and checksum verification.
5. Commits only when one of the generated dat artifacts changed.

If upstream data changes but the generated `.dat` bytes stay identical, the workflow reverts the timestamp-only provenance change and exits without a commit.

## Repository Layout

```text
china_ip_list.txt
generate_geoip_cn_private.py
sync_upstream.py
geoip_gen/
geoip.dat
geoip.dat.sha256
geosite.dat
geosite.dat.sha256
geoip-only-cn-private.dat
geoip-only-cn-private.dat.sha256
PROVENANCE.json
UPSTREAM_PROVENANCE.json
.github/workflows/update.yml
LICENSE
NOTICE
```

## License And Attribution

Code in this repository is licensed under MIT. See `LICENSE`.

The `CN` data comes from `17mon/china_ip_list` and is licensed under CC-BY-NC-SA 4.0. The generated `.dat` is derived from that data, so redistribution carries the same attribution, non-commercial, and share-alike obligations. See `NOTICE` for source links and details.

The `PRIVATE` ranges are standard private and special-purpose ranges from IANA/RFC sources, represented in the same shape as V2Ray-compatible GeoIP private data.

The full `geoip.dat` and `geosite.dat` files are synchronized from `Loyalsoldier/v2ray-rules-dat`; their upstream data sources and licensing terms are separate from this repository's MIT-licensed code.

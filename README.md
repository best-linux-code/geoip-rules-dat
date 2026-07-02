# geoip-cn-private

Pure-Python generator for a slim Xray/V2Ray `geoip.dat` file containing only two tags:

- `geoip:cn`, generated from `17mon/china_ip_list`
- `geoip:private`, generated from the standard private and special-purpose IP ranges used by V2Ray-compatible GeoIP data

The generated artifact is committed as `geoip-only-cn-private.dat`. It can be used by v2rayNG as an external GeoIP file.

## Current Artifact

```text
geoip-only-cn-private.dat
CN:      7456
PRIVATE: 21
SHA256:  303d175dad44a2c342645504e3ac50f95c4fa5c798901737bdb84e7a8a8071f6
```

`PROVENANCE.json` records the source URL, input checksum, output checksum, generation timestamp, entry counts, and private CIDR list.

## Usage

Regenerate from the committed `china_ip_list.txt`:

```bash
python3 generate_geoip_cn_private.py generate
```

Inspect and validate the committed artifact without network access:

```bash
python3 generate_geoip_cn_private.py inspect
```

Both commands use only the Python standard library. No Go, protoc, Docker, pip, uv, or protobuf package is required.

## v2rayNG

Put `geoip-only-cn-private.dat` in v2rayNG's assets directory, usually:

```text
Android/data/com.v2ray.ang/files/assets/geoip-only-cn-private.dat
```

Reference it with `ext:` rules:

```text
ext:geoip-only-cn-private.dat:cn
ext:geoip-only-cn-private.dat:private
```

This file is intentionally slim. It does not contain other country or service tags such as `geoip:us`, `geoip:jp`, or `geoip:telegram`.

## Automatic Updates

`.github/workflows/update.yml` runs weekly and can also be started manually. The workflow:

1. Fetches the latest `china_ip_list.txt` from the source URL in `geoip_gen/models.py`.
2. Regenerates `geoip-only-cn-private.dat`, checksum, and provenance.
3. Runs the offline inspector.
4. Commits only when `geoip-only-cn-private.dat` changed.

If upstream data changes but the generated `.dat` bytes stay identical, the workflow reverts the timestamp-only provenance change and exits without a commit.

## Repository Layout

```text
china_ip_list.txt
generate_geoip_cn_private.py
geoip_gen/
geoip-only-cn-private.dat
geoip-only-cn-private.dat.sha256
PROVENANCE.json
.github/workflows/update.yml
LICENSE
NOTICE
```

## License And Attribution

Code in this repository is licensed under MIT. See `LICENSE`.

The `CN` data comes from `17mon/china_ip_list` and is licensed under CC-BY-NC-SA 4.0. The generated `.dat` is derived from that data, so redistribution carries the same attribution, non-commercial, and share-alike obligations. See `NOTICE` for source links and details.

The `PRIVATE` ranges are standard private and special-purpose ranges from IANA/RFC sources, represented in the same shape as V2Ray-compatible GeoIP private data.

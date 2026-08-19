# Pipeline Execution Environment

Pins the KiCad CLI environment Stage 1 of `validation-pipeline.md` runs
against, and records why the obvious local options don't work.

## Why not native/apt

This workspace's base image is Ubuntu 24.04 (noble). Its default apt
candidate is `kicad` **7.0.11+dfsg-1build4**. The vendored reference project
(`hardware/reference/mosaicG5-HAT/`) is KiCad 10.0 format (`generator_version
"10.0"`, schematic format `20260306`, PCB format `20260206`) — a KiCad 7
install cannot open it. A native apt install is not a viable path here
without adding KiCad's own PPA/repo, which is a heavier and less
reproducible option than pinning a container image.

## Pinned image

`kicad/kicad:10.0.5` (Docker Hub / GHCR mirror `ghcr.io/kicad/kicad:10.0.5`),
confirmed to exist as a published tag. This matches:
- the vendored project's file-format version (KiCad 10.0.x), and
- the KiCad 10.0.5 patch level referenced in this workspace's prior status
  notes (not independently verifiable from the vendored files' headers
  alone, but consistent with them).

A `-full` variant (`kicad/kicad:10.0.5-full`) also exists, adding 3D content
(symbol/footprint 3D models used by the 3D viewer). Stage 1 only needs
`kicad-cli sch erc` and `kicad-cli pcb drc`, neither of which renders 3D —
**use the base tag, not `-full`**, unless a later pipeline stage needs 3D
export. Revisit this if that changes.

## Example invocation (for whoever runs Stage 1)

```sh
docker run --rm \
  -v "$(pwd)/hardware/reference/mosaicG5-HAT:/work:ro" \
  kicad/kicad:10.0.5 \
  kicad-cli sch erc "/work/Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_sch" \
    --format json --output /work/erc.json

docker run --rm \
  -v "$(pwd)/hardware/reference/mosaicG5-HAT:/work:ro" \
  kicad/kicad:10.0.5 \
  kicad-cli pcb drc "/work/Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_pcb" \
    --format json --output /work/drc.json
```

Mounting the source tree read-only reflects Stage 1's fail-closed intent: the
runner reads the pinned input and writes its output elsewhere, it does not
mutate the vendored KiCad source. Exact `kicad-cli` flags (e.g. severity
filtering, units) are TBD until Stage 1's runner script is actually written.

## Known limitation: this session cannot execute the pipeline

The Docker CLI is present in this workspace, but there is no running Docker
daemon (`docker info` fails to connect to `/var/run/docker.sock`) — this is a
sandboxed session without container execution capability. Everything above
is a **pinned, documented environment spec**, not something this session has
run or can run natively. Stage 1 needs to run on a developer machine or in
CI where a Docker daemon is available; do not claim ERC/DRC output exists
until someone (or something) has actually run these commands.

## CI now provides that execution path

`.github/workflows/kicad-baseline.yml` runs `reproducibility_check.py`
inside `container: kicad/kicad:10.0.5` on every push/PR touching
`hardware/reference/**` or `automation/**`, and uploads
`evidence/reproducibility-checks/` as a build artifact. This is where the
real `erc.json`/`drc.json` and the actual D2 pass/fail result will first
exist — this development sandbox still can't produce or inspect them
directly, only trigger the workflow by pushing.

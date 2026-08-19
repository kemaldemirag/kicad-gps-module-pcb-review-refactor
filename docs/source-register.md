# Source Register

Tracks the exact, verifiable identity of every external source this workspace
depends on. An entry only belongs here once it has been independently
re-verified in this workspace (cloned, hashed) — not copied from a prior
claim without re-checking.

## Reference candidate: septentrio-gnss/mosaicG5-HAT

- **Repository**: `https://github.com/septentrio-gnss/mosaicg5-hat`
- **Pinned commit**: `4936e8169b24b613ead996b778399cd3cce22721`
- **Verification method**: shallow clone (`git clone --depth 1`) on 2026-08-19;
  `git rev-parse HEAD` on the default branch matched this hash exactly.
- **License**: CC BY-SA 4.0, stated open source hardware (per the source
  repo's own `README.md`). Attribution required on any derived/republished
  content; no separate `LICENSE` file was found at the repo root, only the
  README statement.
- **KiCad version**: `generator_version "10.0"` in both `.kicad_sch` and
  `.kicad_pcb` file headers (schematic format version `20260306`, PCB format
  version `20260206`). This confirms KiCad 10.0.x; the specific patch level
  (10.0.5, per prior status notes) is not independently derivable from the
  file header alone.
- **Vendoring status**: Vendored under `hardware/reference/mosaicG5-HAT/`
  (KiCad project tree, custom footprint, referenced 3D STEP models, BOM).
  All five hashed files re-hashed post-copy and matched this manifest
  byte-for-byte. See `hardware/reference/mosaicG5-HAT/ATTRIBUTION.md` for
  license/attribution terms. Pictures, firmware helper scripts, and prose
  documentation from the source repo were intentionally not vendored.

### File manifest (SHA-256, core KiCad + BOM sources)

| File | SHA-256 |
| --- | --- |
| `Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_pro` | `9e8613709c8b093200f91cd5fe0ed0b1b9d2612d1750db3cc15d856bd4f331d5` |
| `Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_sch` | `b95157dda3393170038c97b711a854b39379e9ee580b01f66011e24e53260f59` |
| `Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_pcb` | `5b5f13a4ea0cac1e25a0aa58c7cfd02423d5cf2dde5a2da25c5df4a54e86e3cb` |
| `Kicad/mosaci-G5/LGA54_MOSAIC-MINI_SEP.kicad_mod` | `15ea6c8edea7cd8e9e37724fb835fab8700efac1bffb541710af3dde6ffdf2f7` |
| `BOM.xlsx` | `e130ac908154d3e4f5d9092485914d9f93fff96652cfe1a9c4e846ba48703459` |

Paths are relative to the reference repository root. Not covered by this
manifest: the `.STEP`/`.step` 3D models, `pictures/`, and the two Python
scripts under `Python code/` — none of those feed the ERC/DRC baseline
pipeline, so they're out of scope for reproducibility hashing.

### What this unblocks

`automation/validation-pipeline.md` Stage 1 (baseline runner) can now target
a concrete, hash-pinned input: `Kicad/mosaicG5 HAT/mosaicG5_RPi_HAT.kicad_pro`
at the commit above. Stage 1's fail-closed hash check should compare against
the four KiCad-file hashes in this manifest.

## Rejected sources

### SRC-AI-001 — Quectel LC76G AI Overview material

- **Status**: REJECTED
- **Date**: 2026-08-19
- **Description**: Screen captures and pin/value tables attributed to Quectel
  LC76G, sourced from a Google AI Overview. Included an 18-pin LCC pin table
  (VCC\_RF pin 1, ANT\_IN pin 4, V\_BCKP pin 7) and a "Standard Reference
  Circuit Checklist" (10 µF + 100 nF decoupling, 50 Ω coplanar/microstrip,
  feed inductor for active antenna, coin-cell on V\_BCKP).
- **Rejection grounds**:
  1. No document number, revision, or manufacturer source link.
  2. Device family is Quectel LC76G — a different module from the project
     target (Septentrio mosaic-G5 P3H). Mixing the two would produce incorrect
     rules and values.
  3. AI-generated summaries without a primary manufacturer document do not meet
     the workspace source-acceptance criteria.
- **Decision reference**: DEC-007 in `docs/decision-log.md`.
- **Historical note**: The LC76G was apparently under consideration at some
  point. This entry is preserved to prevent future module-identity confusion.

---

## Target client board

Not yet supplied. No entry until real KiCad source files are received from
the client — see `SCOPE-MVP.md` and `README.md` (`INPUT-BLOCKED` gate).

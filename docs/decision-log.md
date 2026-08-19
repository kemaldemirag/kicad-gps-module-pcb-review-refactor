# Decision Log

Records adopted decisions that close an open question, fix a source, or change
the direction of a pipeline stage. Each entry is immutable once its status
moves from `PROPOSED` to `ADOPTED`; a superseding entry must be created
instead of editing the original.

---

## DEC-006 — Power and RF requirement closure via Manual v2.0.0

- **Date**: 2026-08-18
- **Decision**: The following values from *mosaic-G5 Hardware Manual v2.0.0*
  (28 May 2026) are accepted as authoritative for the reference pipeline:

  | Requirement | Value | Section |
  | --- | --- | --- |
  | Min. supply drive capacity (peak) | 500 mA | §3.5 |
  | VDD\_3V3 decoupling | ≥22 µF, rated voltage | §5.3 |
  | Power-rail resistance limit | R < (V\_min − 3.135 V) / 0.5 A | §5.4.2 |
  | Antenna trace topology | Ground-referenced 50 Ω CPWG | §5.4.3 |
  | VANT feed current limit (ANT\_1 + ANT\_2) | 150 mA total | §4.2 |
  | Part number confirmation | mosaic-G5 P3H = 410502 | §3.1.3 |

  These values verify OBS-001 (CPWG conflict) and close action-sequence item 2
  of `current-state-assessment.md`. The 0.1427 mm RF trace cannot be confirmed
  as 50 Ω until the target board stack-up is supplied; RULE-001…RULE-010 remain
  unfrozen.
- **Impact**: Reference track advances; target finding lifecycle does not open.
- **Status**: PROPOSED

---

## DEC-007 — Rejection of AI-generated source records (SRC-AI-001)

- **Date**: 2026-08-19
- **Decision**: Quectel LC76G AI Overview screen captures and pin/value data
  observed in the shared research folder are recorded as `SRC-AI-001` with
  status `REJECTED`. Rejection grounds: no document number, no revision, no
  manufacturer source link, and the device family (Quectel LC76G) is different
  from the project module (Septentrio mosaic-G5 P3H). No pin assignments,
  component values, or rules shall be derived from this material. The LC76G was
  a candidate at some point; this entry is made to prevent future identity
  confusion.
- **Impact**: SRC-AI-001 material is permanently excluded from the evidence
  chain. See `docs/source-register.md` for the rejected entry.
- **Status**: PROPOSED

---

## DEC-008 — Single canonical work stream for the reference anchor

- **Date**: 2026-08-19
- **Decision**: Commit `4936e8169b24b613ead996b778399cd3cce22721` of
  `septentrio-gnss/mosaicG5-HAT` is fixed as the reference anchor by the D2
  package produced on 2026-08-18. Parallel agent sessions must not re-derive
  or re-verify this anchor independently; they must reference the existing
  `docs/source-register.md` entry and the D2 reproducibility record. Re-pinning
  is only warranted if the source repository changes or the hash is found to be
  incorrect.
- **Impact**: Eliminates regression risk from a second session regenerating
  already-closed work. `docs/source-register.md` remains the single source of
  truth for the pinned commit and file hashes.
- **Status**: PROPOSED

---

## DEC-009 — G-ANNOT's five-record entry criterion does not match real erc.json

- **Date**: 2026-08-19
- **Decision**: Not a decision -- a flagged discrepancy pending one. Stage 1
  of `automation/validation-pipeline.md` was executed for real against the
  pinned reference candidate in CI (`kicad-baseline.yml`, run #6/#7, both
  green): `kicad-cli sch erc` against `mosaicG5_RPi_HAT.kicad_sch` produced
  **221 violations across 1 sheet**, not the five records
  `docs/gates/g-annot-contract.md`'s entry criterion requires ("The artifact
  contains exactly five records for this run"). `automation/scripts/
  signal_plane_extract.py`'s ERC summary (`by_type`/`by_severity` counts) is
  the source of this number, itself built from the same erc.json schema
  documented in `automation/validation-pipeline.md` Stage 3.
- **Options, not yet chosen between**:
  1. G-ANNOT's "five records" referred to a specific triage batch (e.g. a
     manually curated subset, matching `docs/label-dictionary.md`'s
     `P1-RF-ADJACENT` / `REF-F-009` references) rather than the full ERC
     output -- the gate's entry criterion needs rewording to say so.
  2. The gate was scoped against stale or partial data and needs its
     criterion changed to match real erc.json volume (e.g. "N records" or
     a filtered subset by severity/type).
- **Impact**: G-ANNOT cannot run as literally specified against the real
  erc.json. Not resolved here -- `docs/gates/g-annot-contract.md` and
  `docs/decision-log.md` DEC-007 (which anticipated a five-record run) were
  authored by a different session; changing them unilaterally risks
  contradicting a decision already in flight. Left `PROPOSED` for whoever
  owns that gate to reconcile.
- **Status**: PROPOSED

# Validation Pipeline Scope

## Purpose

Define the automation that turns a KiCad project (reference candidate today, target
client board once supplied) into reproducible, machine-checkable review evidence:
normalized ERC/DRC output, a signal/plane snapshot, and a reproducibility record.
This is infrastructure work — it does not itself produce review findings on the
target board, and it must not be presented as such.

## Environment constraint

`kicad-cli` is not installed in this workspace. The pipeline must be runnable from
a pinned, documented environment (container image or a recorded local install with
version pin) so that "byte-identical across two runs" is actually checkable by
anyone reproducing the work, not just asserted. Recording the KiCad version and
exact CLI invocation is a hard requirement of Stage 1, not an implementation detail.

## Stages

### Stage 1 — Baseline runner

Input: a KiCad project pinned to an exact commit (currently the reference
candidate, `septentrio-gnss/mosaicG5-HAT` at the commit recorded in
`docs/source-register.md`, once that file exists).

Actions:
- Run `kicad-cli sch erc` and `kicad-cli pcb drc` against the pinned project,
  both with `--format json`.
- Record the exact KiCad version, CLI flags, and project file hashes (SHA-256)
  alongside the output.
- Fail closed: if the project hash doesn't match the pinned commit, the runner
  refuses to produce a baseline.

Output: `erc.json`, `drc.json`, and a manifest of input hashes + tool version.

### Stage 2 — Contract fixture / reproducibility check (D2)

Purpose: prove Stage 1 is deterministic before anyone treats its output as
evidence.

Actions:
- Run Stage 1 twice, independently, against the same pinned input.
- Normalize both `drc.json` outputs (stable key ordering, no timestamps/paths
  that vary by run) into a signal/plane JSON representation.
- Diff the two normalized outputs. A pass requires byte-identical output; any
  difference blocks the gate and must be triaged as a runner bug, not waived.

This is the check the README's "D2 reproducibility" claim refers to. It belongs
in this pipeline as a repeatable, re-runnable script — not as a one-time claim
in prose.

### Stage 3 — Signal/plane analysis (read-only)

Purpose: extract a normalized, reviewable summary of nets, planes, and
proximity-relevant geometry from the DRC baseline, for human triage — without
mutating the KiCad source.

Actions:
- Parse `drc.json` (and PCB geometry as needed) into the same normalized
  signal/plane JSON schema used in Stage 2.
- No numeric RF/DFM thresholds are invented here; the tool reports what the
  KiCad rules already flagged plus structural facts (net class, plane
  adjacency), and leaves rule authorship to the frozen rule set (`RULES-FROZEN`
  gate), sourced from real datasheets/stack-up once available.

Output: the signal/plane JSON consumed by `docs/reference-signal-plane-triage.md`-
style triage records.

### Stage 4 — G-ANNOT hookup

Purpose: connect this pipeline's `erc.json` output to the gate already defined
in `docs/gates/g-annot-contract.md`.

Actions:
- Stage 1's `erc.json` is the artifact `G-ANNOT` expects. The gate's entry
  criterion (exactly five records for a run) is a property of the reference
  candidate's current ERC state, not a pipeline parameter — the runner does
  not filter or truncate to force that count.
- Each of the five records gets disposed per the gate contract (confirms a
  finding / creates a debt correction / rejected) and logged in the documents
  that already own that decision (`docs/label-dictionary.md` conventions).

## Non-goals

- No Gerber/BOM/CPL generation (conditional scope, per `SCOPE-MVP.md`).
- No fabricated numeric RF/DFM rules without a real datasheet or stack-up.
- No claim of validated behavior on the actual client target board — this
  pipeline currently only has the reference candidate as input.

## Open dependencies before Stage 1 can run

1. Pin and record the reference candidate commit + file hashes in
   `docs/source-register.md` (does not yet exist).
2. Pin the KiCad CLI version and document how to obtain it (container image
   recommended, since it's absent from this workspace).
3. Decide where pipeline scripts live under `automation/` (this doc scopes
   them; no implementation script exists yet).

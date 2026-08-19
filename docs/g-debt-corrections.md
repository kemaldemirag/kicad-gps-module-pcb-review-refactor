# G Debt Corrections

> Temporary implementation list. Delete this file after every unchecked item below is resolved.

## Current debt list

- [x] Place the four review documents in the committed `docs/` layout:
  - `docs/label-dictionary.md`
  - `docs/proposed-backlog.md`
  - `docs/gates/g-annot-contract.md`
  - `docs/g-debt-corrections.md`
- [x] Record `REF-F-009` as `CONFIRMED · MINOR`.
- [x] Keep these portfolio-facing review documents in English.
- [x] `erc.json` has landed (CI `kicad-baseline.yml`, run #6/#7) -- but with
      221 records, not the expected five. See DEC-009 in
      `docs/decision-log.md`: `G-ANNOT`'s entry criterion needs reconciling
      before it can run against real data.
- [ ] Reconcile `docs/gates/g-annot-contract.md`'s five-record entry
      criterion against DEC-009, then run `G-ANNOT`.
- [ ] Remove this file once the remaining debt item is closed.

## Notes

- The `REF-F-009` decision is closed on the current evidence basis because the `P1-RF-ADJACENT` count is zero.
- `CAM` can corroborate that status, but it is not the source of the RF finding.

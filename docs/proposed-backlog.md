# Proposed Backlog

This backlog captures the next concrete work after the current documentation drop.

## Immediate actions (action-revision v2, 2026-08-19)

These items were identified or re-prioritised by the action revision and must be
addressed before the ready-next list below.

### R-01 — Synchronise the two work streams (PRIORITY: HIGH)

A second agent session was found to be re-deriving the reference anchor and
treating `docs/source-register.md` as missing. The D2 package produced on
2026-08-18 already fixed commit `4936e8169b24b613ead996b778399cd3cce22721`,
verified two independent DRC runs, and published `source-register.md`.

**Action**: Inform the parallel session of the D2 package location and the
current state of `docs/source-register.md`. Regression risk: if the second
stream continues unaware, it will reproduce already-closed work and may
overwrite or contradict the pinned anchor. Decision: DEC-008.

### R-02 — Record AI-generated source as REJECTED (PRIORITY: HIGH)

Quectel LC76G AI Overview material (pin tables, circuit checklist) in the
shared research folder carries no document number, no manufacturer source, and
belongs to a different module family. It must not feed into any rule, value, or
finding for this project.

**Action**: Closed — `SRC-AI-001` recorded as `REJECTED` in
`docs/source-register.md` (DEC-007). No further work required unless new
AI-sourced material appears.

### R-03 — PDF filing and licence hygiene (PRIORITY: MEDIUM)

The `003-Referans Kaynaklar/002-PDF'ler` folder is empty while three PDFs sit
in the general research folder:

| File | Assessment |
| --- | --- |
| `un0rick_open_source_fpga_board_for_singl.pdf` | Out of scope — ultrasound FPGA board |
| `CryptKi_Mobile_Hardware_Wallet.pdf` | Out of scope — crypto hardware wallet thesis |
| `Clyde_Coombs_Printed_Circuits_Handbook…pdf` | PCB domain; see note below |

*Printed Circuits Handbook* (McGraw-Hill, 6th ed., 2008) is a general
reference and cannot produce numeric fab rules for a specific JLCPCB stack-up.
The `ElectroVolt.ir_` filename prefix suggests an unlicensed copy, which
conflicts with the workspace source-acceptance policy (manufacturer PDFs are
recorded by document number, revision, and direct URL rather than
redistributed).

**Action**: Mark the first two files as out-of-scope in any source inventory.
Do not use the Handbook as a rule source; cite a licensed copy with section
reference if background context is needed.

---

## Ready next

1. Commit the `erc.json` artifact once the expected five records are available.
2. Run the `G-ANNOT` contract against that five-record input set.
3. Classify each annotation outcome into one of three buckets: accepted finding, debt correction, or rejected noise.
4. Apply any required repository-side corrections that fall out of the contract run.
5. Remove `docs/g-debt-corrections.md` after every listed debt item has been closed.

## Follow-on work

1. Refresh any affected gate or finding records after the `G-ANNOT` run.
2. Preserve the current `REF-F-009 = CONFIRMED · MINOR` decision unless new evidence changes the zero-count RF adjacency basis.
3. Keep new portfolio-facing review documents in English unless there is an explicit translation request.

## Action-sequence status (action-revision v2)

| # | Action | Status |
| --- | --- | --- |
| R-01 | Synchronise work streams; notify second stream of D2 package | NEW — DO FIRST |
| R-02 | Record LC76G AI Overview material as REJECTED | CLOSED — SRC-AI-001 recorded |
| R-03 | File/mark PDFs; keep Handbook out of rule sources | NEW |
| 1 | Separate 5 power\_pin\_not\_driven records from PWR\_FLAG/pin-type annotation | ACTIONABLE |
| 2 | Link 500 mA / 22 µF to manual + section | CLOSED (DEC-006) |
| 3 | Confirm target repo access / correct URL | BLOCKED (G0-01) |
| 4 | Run runner against target source | BLOCKED |
| 5 | Cover ANT\_MAIN + ANT\_AUX in scope | ACTIONABLE |
| 6 | Prove target module/antenna/cable assembly | BLOCKED |
| 7 | JLC04161H-3313 order profile + RF/USB geometry calculation | ACTIONABLE |
| 8 | Library table / 3D path correction plan | ACTIONABLE |
| 9 | Open target findings in review-findings.md | BLOCKED |

Items 3, 4, 6, and 9 share a single root cause: G0-01 (target repo access not yet provided). These are business-development decisions, not process gaps.

## Not in scope for this step

- Reopening `REF-F-009` without new evidence.
- Claiming RF behaviour from `CAM` output alone.
- Promoting the temporary debt list to a permanent repository document.

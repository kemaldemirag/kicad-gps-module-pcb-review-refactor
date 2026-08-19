# Label Dictionary

This repository uses short, explicit labels so review findings, gate states, and debt items stay traceable across documents.

## Finding status

| Label | Meaning |
| --- | --- |
| `CANDIDATE` | Observed signal that still needs confirmation before it can count as a finding. |
| `CONFIRMED` | Verified finding backed by committed evidence. |
| `REJECTED` | Reviewed item that does not qualify as a finding. |
| `WAIVED` | Accepted deviation with an explicit rationale and boundary. |

## Severity

| Label | Meaning |
| --- | --- |
| `CRITICAL` | Release-blocking defect with immediate functional, safety, or manufacturing risk. |
| `MAJOR` | Important defect that should be fixed before advancing the design gate. |
| `MINOR` | Real issue with limited impact; track and resolve without overstating risk. |

## Gate and workflow state

| Label | Meaning |
| --- | --- |
| `INPUT-BLOCKED` | Required source inputs are still missing. |
| `INPUT-READY` | Minimum source package is usable for controlled review work. |
| `BASELINED` | Reference inputs and tool outputs are fixed and reproducible. |
| `RULES-FROZEN` | Review and validation rules are stable enough to enforce. |
| `REFACTORED` | Intended schematic or PCB changes have been applied. |
| `VERIFIED` | Post-change validation is complete for the active scope. |
| `FAB-READY` | Manufacturing package is ready, subject to scope approval. |
| `PROTOTYPE-VALIDATED` | Physical prototype evidence exists for the claimed behavior. |
| `RELEASED` | Approved release package has been published. |

## Evidence and source vocabulary

| Label | Meaning |
| --- | --- |
| `CAM` | Manufacturing-view corroboration only; useful to confirm a condition, not to originate it. |
| `ERC` | Electrical rules check output used for schematic annotation and triage work. |
| `DRC` | Design rules check output used for PCB rule verification. |
| `RF` | Radio-frequency design context, including antenna proximity and keepout concerns. |
| `DEBT` | Known correction or cleanup item that must be resolved to keep records aligned. |

## Finding identifier conventions

| Pattern | Meaning |
| --- | --- |
| `REF-F-###` | Reference-review finding identifier. |
| `P0-*`, `P1-*` | Priority or bucket prefixes used by triage records and counters. |
| `P1-RF-ADJACENT` | Bucket for RF-adjacent proximity cases counted during triage. |

## Current explicit decision

- `REF-F-009` is classified as `CONFIRMED · MINOR`.
- Rationale: the RF proximity exit metric is zero for `P1-RF-ADJACENT`, so there is no remaining basis to leave the item pending.
- `CAM` may corroborate that outcome, but it does not generate the RF finding by itself.

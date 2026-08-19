# G-ANNOT Contract

## Purpose

`G-ANNOT` is the review gate for turning an `erc.json` annotation set into traceable repository actions.

## Entry criteria

The gate starts only when all of the following are true:

1. An `erc.json` artifact is committed to the repository.
2. The artifact contains exactly five records for this run.
3. The records are stable enough to review as a single batch.

## Required handling

For each of the five records:

1. Identify the annotation and its source context.
2. Decide whether it confirms an existing finding, creates a debt correction, or is rejected as non-actionable noise.
3. Record the result in the repository documents that own that decision.
4. Avoid using `CAM` as the origin of an RF finding; `CAM` may confirm, but not create, that class of evidence.

## Exit criteria

`G-ANNOT` passes only when all of the following are true:

1. All five records have an explicit disposition.
2. Any accepted actions are transferred into the standing backlog or correction list.
3. No annotation record is left unclassified.
4. Any affected finding status remains internally consistent across the updated documents.

## Outputs

A completed `G-ANNOT` run should leave behind:

- updated decision records where needed,
- an updated backlog or debt list when action is required,
- no ambiguous annotation leftovers from the five-record batch.

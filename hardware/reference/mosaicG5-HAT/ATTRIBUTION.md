# Attribution — mosaicG5 HAT reference candidate

The files under this directory are vendored from an external, independently
authored open-hardware project. They exist here solely as a reference
candidate for developing this workspace's review/validation pipeline — they
are **not** the client's target board and carry no claim of being reviewed
or corrected.

- **Source repository**: https://github.com/septentrio-gnss/mosaicg5-hat
- **Pinned commit**: `4936e8169b24b613ead996b778399cd3cce22721`
- **License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/),
  stated open source hardware, per the source repository's own `README.md`.
  No separate `LICENSE` file exists at the source repo root.
- **Original author**: Septentrio (septentrio-gnss on GitHub).
- **Verification record**: see `docs/source-register.md` in this repository
  for the SHA-256 manifest these vendored files were checked against.

## What was vendored and why

Only the files needed to run the automation pipeline's ERC/DRC baseline and
BOM cross-checks: the KiCad project/schematic/PCB, the custom footprint, the
3D step models referenced by the PCB, and the bill of materials. Pictures,
Python firmware helper scripts, and the prose design/user documentation from
the source repository were intentionally left out — they don't feed the
pipeline and vendoring them would widen this change beyond its purpose.

## Redistribution

Any redistribution of this directory's contents outside this repository
must preserve the CC BY-SA 4.0 attribution above.

#!/usr/bin/env python3
"""Stage 2 of automation/validation-pipeline.md (the "D2" reproducibility
check): run the Stage 1 baseline runner twice against the same pinned input
and prove the two runs agree.

Canonicalization strips VOLATILE_KEYS and sorts list contents. Both rules
below are backed by an actual CI run (kicad-cli 10.0.5 against
hardware/reference/mosaicG5-HAT), not guessed in advance:

- erc.json/drc.json both carry a top-level "date" field set to wall-clock
  time -- always different between two runs, never a real content change.
- drc.json's "violations" array is not stably ordered: two runs found the
  exact same violations (same descriptions, positions, UUIDs) but listed
  in a different sequence. Sorting every list by its canonicalized content
  makes order-independent report entries compare equal without hiding an
  actual change in *which* violations were found.
"""

import argparse
import difflib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).resolve().parent / "baseline_runner.py"

# Keys to blank out anywhere in the JSON tree before comparing, because
# they're expected to vary run-to-run without indicating a real difference.
# Confirmed against a real kicad-cli 10.0.5 run -- see module docstring.
VOLATILE_KEYS: set[str] = {"date"}


def canonicalize(obj):
    if isinstance(obj, dict):
        return {k: canonicalize(v) for k, v in sorted(obj.items()) if k not in VOLATILE_KEYS}
    if isinstance(obj, list):
        items = [canonicalize(v) for v in obj]
        items.sort(key=lambda x: json.dumps(x, sort_keys=True))
        return items
    return obj


def canonical_json(path: Path) -> str:
    data = json.loads(path.read_text())
    return json.dumps(canonicalize(data), indent=2, sort_keys=True)


def run_baseline(output_dir: Path) -> int:
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--output-dir", str(output_dir)]
    )
    return result.returncode


def diff_runs(dir_a: Path, dir_b: Path) -> bool:
    """Return True if erc.json and drc.json are canonically identical."""
    ok = True
    for name in ("erc.json", "drc.json"):
        file_a, file_b = dir_a / name, dir_b / name
        if not file_a.exists() or not file_b.exists():
            print(f"MISSING: {name} in one of the two runs", file=sys.stderr)
            ok = False
            continue
        canon_a, canon_b = canonical_json(file_a), canonical_json(file_b)
        if canon_a != canon_b:
            print(f"NOT BYTE-IDENTICAL after canonicalization: {name}", file=sys.stderr)
            print(f"  run A: {file_a}", file=sys.stderr)
            print(f"  run B: {file_b}", file=sys.stderr)
            diff_lines = list(
                difflib.unified_diff(
                    canon_a.splitlines(),
                    canon_b.splitlines(),
                    fromfile=f"run-a/{name}",
                    tofile=f"run-b/{name}",
                    lineterm="",
                )
            )
            for line in diff_lines[:60]:
                print(f"  {line}", file=sys.stderr)
            if len(diff_lines) > 60:
                print(f"  ... ({len(diff_lines) - 60} more diff lines omitted)", file=sys.stderr)
            ok = False
        else:
            print(f"OK: {name} matches across both runs.")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-a", type=Path, default=None, help="Existing run A dir (skip re-running)"
    )
    parser.add_argument(
        "--run-b", type=Path, default=None, help="Existing run B dir (skip re-running)"
    )
    args = parser.parse_args()

    if args.run_a and args.run_b:
        dir_a, dir_b = args.run_a, args.run_b
    else:
        base = REPO_ROOT / "evidence" / "reproducibility-checks"
        dir_a, dir_b = base / "run-a", base / "run-b"
        print("Running Stage 1 twice, independently ...")
        rc_a = run_baseline(dir_a)
        rc_b = run_baseline(dir_b)
        if rc_a != 0 or rc_b != 0:
            print(f"Stage 1 did not complete cleanly (exit {rc_a}, {rc_b}).", file=sys.stderr)
            return max(rc_a, rc_b)

    identical = diff_runs(dir_a, dir_b)
    if identical:
        print("D2 reproducibility check PASSED: two independent runs agree.")
        return 0
    print("D2 reproducibility check FAILED.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

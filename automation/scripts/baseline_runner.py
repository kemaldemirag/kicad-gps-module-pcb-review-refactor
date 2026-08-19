#!/usr/bin/env python3
"""Stage 1 of automation/validation-pipeline.md: run kicad-cli ERC/DRC
against a hash-pinned KiCad project and record the output as evidence.

Fails closed: refuses to invoke kicad-cli at all if any manifest file's
SHA-256 doesn't match what's recorded, so a baseline can never be produced
against source that silently drifted from what was reviewed.

Requires `kicad-cli` on PATH -- run this inside the pinned environment
documented in automation/environment.md (kicad/kicad:10.0.5). This script
does not itself start Docker; that's a deliberate separation of concerns
between "what environment" (environment.md) and "what the runner does"
(this file).
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest(manifest: dict, project_root: Path) -> list[str]:
    """Return a list of mismatch descriptions; empty list means clean."""
    mismatches = []
    for rel_path, expected_hash in manifest["files"].items():
        full_path = project_root / rel_path
        if not full_path.is_file():
            mismatches.append(f"MISSING: {rel_path}")
            continue
        actual_hash = sha256_of(full_path)
        if actual_hash != expected_hash:
            mismatches.append(
                f"HASH MISMATCH: {rel_path}\n"
                f"    expected {expected_hash}\n"
                f"    actual   {actual_hash}"
            )
    return mismatches


def run_kicad_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=REPO_ROOT / "automation" / "reference-manifest.json",
        help="Path to the hash manifest (default: reference-manifest.json)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Where to write erc.json/drc.json/run-manifest.json "
        "(default: evidence/baseline-runs/<UTC timestamp>)",
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    project_root = REPO_ROOT / manifest["vendored_root"]

    print(f"Verifying {len(manifest['files'])} file hashes against {project_root} ...")
    mismatches = verify_manifest(manifest, project_root)
    if mismatches:
        print("FAIL CLOSED: source does not match the pinned manifest.", file=sys.stderr)
        for m in mismatches:
            print(f"  {m}", file=sys.stderr)
        print("Refusing to run kicad-cli against unverified source.", file=sys.stderr)
        return 2
    print("All file hashes match the manifest.")

    kicad_cli = shutil.which("kicad-cli")
    if kicad_cli is None:
        print(
            "kicad-cli not found on PATH. This script must run inside the "
            "pinned environment described in automation/environment.md "
            "(kicad/kicad:10.0.5) -- it will not run natively in this "
            "workspace, which only has KiCad 7 available via apt.",
            file=sys.stderr,
        )
        return 3

    output_dir = args.output_dir or (
        REPO_ROOT
        / "evidence"
        / "baseline-runs"
        / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    version_result = run_kicad_cli([kicad_cli, "--version"])
    kicad_version = version_result.stdout.strip() or version_result.stderr.strip()

    erc_path = output_dir / "erc.json"
    drc_path = output_dir / "drc.json"
    sch_path = project_root / manifest["sch_entry"]
    pcb_path = project_root / manifest["pcb_entry"]

    erc_result = run_kicad_cli(
        [kicad_cli, "sch", "erc", str(sch_path), "--format", "json", "--output", str(erc_path)]
    )
    drc_result = run_kicad_cli(
        [kicad_cli, "pcb", "drc", str(pcb_path), "--format", "json", "--output", str(drc_path)]
    )

    run_manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "kicad_cli_version": kicad_version,
        "kicad_cli_path": kicad_cli,
        "pinned_commit": manifest["commit"],
        "input_hashes": manifest["files"],
        "erc": {
            "exit_code": erc_result.returncode,
            "stderr": erc_result.stderr.strip(),
        },
        "drc": {
            "exit_code": drc_result.returncode,
            "stderr": drc_result.stderr.strip(),
        },
    }
    (output_dir / "run-manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")

    print(f"ERC: kicad-cli exit {erc_result.returncode} -> {erc_path}")
    print(f"DRC: kicad-cli exit {drc_result.returncode} -> {drc_path}")
    print(f"Run manifest: {output_dir / 'run-manifest.json'}")

    # A nonzero kicad-cli exit here typically just means "violations found",
    # not that the runner failed -- the JSON output is still evidence.
    # The runner's own success is about whether it produced that evidence.
    if not erc_path.exists() or not drc_path.exists():
        print("Runner failed to produce expected output files.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

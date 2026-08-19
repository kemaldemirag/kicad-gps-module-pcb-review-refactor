#!/usr/bin/env python3
"""Stage 3 of automation/validation-pipeline.md: read-only signal/plane
extraction. Turns a Stage 1 run's erc.json/drc.json into a normalized,
triage-ready summary -- without touching the KiCad source.

Schema this is written against (confirmed from a real kicad-cli 10.0.5 run,
CI run #6, 2026-08-19 -- not guessed):

  erc.json top level: $schema, coordinate_units, date, ignored_checks,
    included_severities, kicad_version, sheets, source
    sheets: [{path, uuid_path, violations: [...]}]  -- violations nest
    per-sheet, there is no top-level "violations" key in erc.json.

  drc.json top level: $schema, coordinate_units, date, ignored_checks,
    included_severities, kicad_version, schematic_parity, source,
    unconnected_items, violations
    violations: flat list, each {description, items, severity, type}
    items: [{description, pos: {x, y}, uuid}]

Scope limit: net-class and copper-plane-adjacency facts (mentioned as a
pipeline goal) require parsing the raw .kicad_pcb geometry/zone/net-class
data, not just the ERC/DRC report JSON. That parser doesn't exist yet --
this script only derives what's actually present in the report JSON: violation
counts, and net names recoverable from violation item descriptions like
"Track [Net-(L2-Pad1)] on F.Cu". Extending to true plane-adjacency is future
work, not claimed here.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Matches the leading "[...]" bracket in a DRC item description, e.g.
# "Track [Net-(L2-Pad1)] on F.Cu, length 0.1270 mm" -> "Net-(L2-Pad1)"
# "Polygon [<no net>] of U3 on F.Cu" -> "<no net>" (filtered out below)
#
# This convention is DRC-specific: a copper item (track/via/pad/polygon) is
# tagged with the net it belongs to. It does NOT apply to ERC item
# descriptions -- those bracket the pin's electrical type instead, e.g.
# "Symbol #PWR2 Pin 1 [Power input, Line]", which is not a net name and
# must not be reported as one. Confirmed from real kicad-cli 10.0.5 output
# (CI run #6) -- see module docstring.
DRC_NET_RE = re.compile(r"\[([^\]]*)\]")


def extract_nets(violation: dict) -> list[str]:
    nets = set()
    for item in violation.get("items", []):
        m = DRC_NET_RE.search(item.get("description", ""))
        if m and m.group(1) and m.group(1) != "<no net>":
            nets.add(m.group(1))
    return sorted(nets)


def summarize_violations(violations: list[dict], include_nets: bool) -> dict:
    by_type = Counter(v.get("type", "unknown") for v in violations)
    by_severity = Counter(v.get("severity", "unknown") for v in violations)
    normalized = []
    for v in violations:
        entry = {
            "type": v.get("type"),
            "severity": v.get("severity"),
            "description": v.get("description"),
            "item_count": len(v.get("items", [])),
        }
        if include_nets:
            entry["nets"] = extract_nets(v)
        normalized.append(entry)
    return {
        "total": len(violations),
        "by_type": dict(sorted(by_type.items())),
        "by_severity": dict(sorted(by_severity.items())),
        "violations": normalized,
    }


def extract_erc(erc: dict) -> dict:
    sheets = []
    all_violations = []
    for sheet in erc.get("sheets", []):
        sheet_violations = sheet.get("violations", [])
        all_violations.extend(sheet_violations)
        sheets.append(
            {
                "path": sheet.get("path"),
                "violation_count": len(sheet_violations),
            }
        )
    summary = summarize_violations(all_violations, include_nets=False)
    summary["sheets"] = sheets
    return summary


def extract_drc(drc: dict) -> dict:
    summary = summarize_violations(drc.get("violations", []), include_nets=True)
    summary["unconnected_items"] = len(drc.get("unconnected_items", []))
    summary["schematic_parity_issues"] = len(drc.get("schematic_parity", []))
    all_nets = set()
    for v in summary["violations"]:
        all_nets.update(v["nets"])
    summary["nets_involved"] = sorted(all_nets)
    return summary


def build_signal_plane_json(run_dir: Path) -> dict:
    erc = json.loads((run_dir / "erc.json").read_text())
    drc = json.loads((run_dir / "drc.json").read_text())
    return {
        "kicad_version": drc.get("kicad_version") or erc.get("kicad_version"),
        "source": drc.get("source") or erc.get("source"),
        "erc": extract_erc(erc),
        "drc": extract_drc(drc),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=REPO_ROOT / "evidence" / "reproducibility-checks" / "run-a",
        help="Directory containing erc.json and drc.json (default: run-a "
        "from the last reproducibility check)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path (default: <run-dir>/signal-plane.json)",
    )
    args = parser.parse_args()

    if not (args.run_dir / "erc.json").exists() or not (args.run_dir / "drc.json").exists():
        print(f"erc.json/drc.json not found under {args.run_dir}", file=sys.stderr)
        return 1

    result = build_signal_plane_json(args.run_dir)
    output_path = args.output or (args.run_dir / "signal-plane.json")
    output_path.write_text(json.dumps(result, indent=2) + "\n")

    print(f"ERC: {result['erc']['total']} violations across {len(result['erc']['sheets'])} sheet(s)")
    print(f"DRC: {result['drc']['total']} violations, {len(result['drc']['nets_involved'])} nets involved")
    print(f"Written: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

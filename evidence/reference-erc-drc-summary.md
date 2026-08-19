# Reference ERC/DRC Summary — Raw Counts

Human-readable companion to `evidence/reference-erc-drc-summary.json`. Raw
counts only, extracted from `automation/scripts/signal_plane_extract.py`'s
output — no severity/priority judgment applied.

- **Source run**: [CI run #8](https://github.com/kemaldemirag/kicad-gps-module-pcb-review-refactor/actions/runs/32300615204), commit `e23c3b6c06b0de62dbf36fbe7f39ea6a5eb8a5d3`
- **kicad-cli**: 10.0.5
- **D2 reproducibility**: PASSED
- **Reference project**: `septentrio-gnss/mosaicG5-HAT` @ `4936e8169b24b613ead996b778399cd3cce22721`

## ERC — 221 violations, 1 sheet

| type | count |
| --- | --- |
| lib_symbol_issues | 113 |
| footprint_link_issues | 63 |
| pin_not_connected | 23 |
| pin_to_pin | 15 |
| power_pin_not_driven | 5 |
| multiple_net_names | 1 |
| no_connect_dangling | 1 |

| severity | count |
| --- | --- |
| warning | 189 |
| error | 32 |

## DRC — 385 violations, 23 nets involved

| type | count |
| --- | --- |
| text_thickness | 68 |
| silk_over_copper | 58 |
| lib_footprint_issues | 55 |
| silk_overlap | 48 |
| clearance | 47 |
| isolated_copper | 20 |
| malformed_courtyard | 20 |
| solder_mask_bridge | 14 |
| annular_width | 12 |
| shorting_items | 9 |
| track_dangling | 8 |
| text_height | 6 |
| hole_clearance | 4 |
| drill_out_of_range | 4 |
| starved_thermal | 4 |
| copper_edge_clearance | 3 |
| courtyards_overlap | 3 |
| via_diameter | 2 |

| severity | count |
| --- | --- |
| warning | 263 |
| error | 122 |

Other: `unconnected_items: 0`, `schematic_parity_issues: 0`.

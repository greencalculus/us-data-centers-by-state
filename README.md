# US Data Centers by State: Every Published Count

There is no official count of US data centers. This dataset puts every published count we could verify side by side, by state, with what each source counts and the date it describes, plus the electricity, water and Virginia figures that go with them.

- **128 rows** from Data Center Map (via Pew Research), dcmap.us, Visual Capitalist (via the Washington Examiner), the US Census Bureau, EPRI, Lawrence Berkeley National Laboratory, JLARC and Google.
- **Values copied exactly as published.** The only derived values are Pew's US totals (sums of its four regions) and Google's Virginia water total (sum of four sites), both marked in `notes`.
- **Retrieved 22 October 2026.** Counts change monthly; we plan to refresh every quarter.

Read with context: https://greencalculus.com/data/data-centers-by-state/

## Headline (22 October 2026)

| | Operating | Incl. building and planned | Source, date |
|---|---|---|---|
| United States | 3,172 | 4,771 | dcmap.us, October 2026 |
| United States | 3,068 | 4,624 | Data Center Map via Pew, 19 February 2026 |
| Virginia | 320 to 398 | 591 to 685 | Visual Capitalist, Data Center Map, dcmap.us |
| Virginia (JLARC) | ~150 sites, ~340 buildings | | JLARC, 2024 |

## Columns

| Column | Meaning |
|---|---|
| `id` | Row id, stable within a version |
| `source` | Who published the figure (and through whom we read it) |
| `metric` | `data_centers`, `data_center_sites`, `data_center_buildings`, `establishments_naics_518210`, `electricity_share`, `electricity_use`, `power_demand`, `water_use`, `water_consumption`, `capacity_share`, `residential_bill_increase`, `economic_contribution` |
| `geography`, `state` | Area the figure describes; two-letter state code where it is one state |
| `value`, `unit` | As published; a range is written `low-high` |
| `status` | `operating`, `planned`, `under_construction`, `paused`, `total`, `current_total`, `tracked_total`, `estimate`, `projection` |
| `as_of` | Date or year the figure describes |
| `counts` | What the source counts as one data center |
| `source_title`, `source_url`, `source_date`, `retrieved` | Where and when the figure was read |
| `notes` | Quotes, definitions and caveats |

## Read before comparing

- **Trackers count different things.** A campus, a building or a hall can each be one entry. JLARC counted about 150 sites but around 340 buildings in Virginia.
- **Planned means different things.** Pew's "planned" includes under construction and land banked; dcmap.us splits under construction from planned.
- **The Census figure is not a count of data centers.** NAICS 518210 establishments are hosting, data processing and cloud businesses, many of them offices.

## Build

```
python3 build.py
```

## Licence and citation

CC BY 4.0 for this compilation. Cite this dataset (see `CITATION.cff`) and the original publisher of any figure you use.

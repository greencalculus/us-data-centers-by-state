#!/usr/bin/env python3
"""Build us-data-centers.csv / .json: every published count of US data centers, by state, side by side.

There is no official count of US data centers. Private trackers count different things
(buildings, campuses, projects; operating only or planned too), so each row records
what its source counts in `counts`. Values are copied exactly as published; the only
derived values are the regional and US sums of Pew's table, marked in `notes`.

    python3 build.py
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).parent
RETRIEVED = "2026-10-22"
VERSION = "2026.10.22"

FIELDS = ["id", "source", "metric", "geography", "state", "value", "unit", "status",
          "as_of", "counts", "source_title", "source_url", "source_date", "retrieved", "notes"]

PEW = ("Pew Research Center (Seets and Radde), Most new data centers in the US are coming to rural areas",
       "https://www.pewresearch.org/short-reads/2026/04/13/most-new-data-centers-in-the-us-are-coming-to-rural-areas/",
       "2026-04-13")
PEW_COUNTS = "Data Center Map listings; 'planned' = under construction, planned and land banked; canceled and uncertain removed"
DCMAP = ("dcmap.us, US data center map and statistics", "https://dcmap.us/", "2026-10")
DCMAP_COUNTS = "facilities and projects; a campus, building or hall can each be one entry"
VC = ("Washington Examiner (Hallas), What states are building the most data centers? Texas takes on Virginia, citing Visual Capitalist",
      "https://www.washingtonexaminer.com/policy/technology/4523051/what-states-building-most-data-centers/", "2026-04-09")
CBP = ("US Census Bureau, County Business Patterns 2023, NAICS 518210, state file cbp23st",
       "https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23st.zip", "2025")
CBP_COUNTS = ("business establishments in NAICS 518210 'Computing infrastructure providers, data processing, web hosting, "
              "and related services'; NOT a count of data center buildings")
EPRI = ("EPRI, Powering Intelligence 2026: Updated Scenarios of U.S. Data Center Electricity Use and Power Strategies",
        "https://powering-intelligence.epri.com/load-growth.html", "2026")
EPRI_BRIEF = ("EPRI, Back Pocket Insights: Powering Intelligence, Updated U.S. Data Center Scenarios",
              "https://restservice.epri.com/publicattachment/97025", "2026")
JLARC = ("JLARC, Data Centers in Virginia (Report 598), Summary",
         "https://jlarc.virginia.gov/pdfs/summary/Rpt598Sum.pdf", "2024-12-09")
JLARC_FULL = ("JLARC, Data Centers in Virginia (Report 598), full report",
              "https://jlarc.virginia.gov/pdfs/reports/Rpt598.pdf", "2024-12-09")
LBNL = ("Smith, Hubbard, Newkirk et al., United States Data Center Energy Usage Report: 2025 Update, LBNL",
        "https://escholarship.org/uc/item/33m6w3x0", "2026-06-18")
GOOGLE = ("Google 2026 Environmental Report, table 'Water use by data center location'",
          "https://sustainability.google/files/google-2026-environmental-report.pdf", "2026")

# Pew table: state -> (total, operating, planned), Data Center Map as of 19 Feb 2026
PEW_STATES = [("Virginia", "VA", 685, 398, 287), ("Texas", "TX", 466, 296, 170), ("California", "CA", 331, 277, 54),
              ("Illinois", "IL", 262, 139, 123), ("Georgia", "GA", 235, 94, 141), ("Ohio", "OH", 223, 166, 57),
              ("Arizona", "AZ", 184, 98, 86), ("New York", "NY", 154, 148, 6), ("Oregon", "OR", 142, 115, 27),
              ("Washington", "WA", 135, 124, 11), ("Pennsylvania", "PA", 129, 78, 51), ("Florida", "FL", 128, 120, 8),
              ("North Carolina", "NC", 113, 72, 41), ("Iowa", "IA", 105, 64, 41), ("Indiana", "IN", 92, 38, 54)]
PEW_REGIONS = [("South", 754, 1209), ("Midwest", 419, 655), ("West", 277, 807), ("Northeast", 106, 397)]


def rows():
    out = []

    def add(src, **kw):
        t, u, d = src
        r = dict.fromkeys(FIELDS, "")
        r.update(source_title=t, source_url=u, source_date=d, retrieved=RETRIEVED)
        r.update(kw)
        out.append(r)

    for name, st, total, op, pl in PEW_STATES:
        for status, v in (("operating", op), ("planned", pl), ("total", total)):
            add(PEW, source="Data Center Map via Pew Research Center", metric="data_centers", geography=name, state=st,
                value=v, unit="count", status=status, as_of="2026-02-19", counts=PEW_COUNTS)
    for reg, planned, existing in PEW_REGIONS:
        add(PEW, source="Data Center Map via Pew Research Center", metric="data_centers", geography=f"{reg} (Census region)",
            value=existing, unit="count", status="operating", as_of="2026-02-19", counts=PEW_COUNTS)
        add(PEW, source="Data Center Map via Pew Research Center", metric="data_centers", geography=f"{reg} (Census region)",
            value=planned, unit="count", status="planned", as_of="2026-02-19", counts=PEW_COUNTS)
    add(PEW, source="Data Center Map via Pew Research Center", metric="data_centers", geography="United States",
        value=sum(e for _, _, e in PEW_REGIONS), unit="count", status="operating", as_of="2026-02-19", counts=PEW_COUNTS,
        notes="Sum of Pew's four regional 'existing' figures (GreenCalculus calculation); Pew's text says 'more than 3,000 operational data centers'.")
    add(PEW, source="Data Center Map via Pew Research Center", metric="data_centers", geography="United States",
        value=sum(p for _, p, _ in PEW_REGIONS), unit="count", status="planned", as_of="2026-02-19", counts=PEW_COUNTS,
        notes="Sum of Pew's four regional 'planned' figures (GreenCalculus calculation); Pew's text says 'more than 1,500'. "
              "Pew: 67% of planned data centers are in rural areas, 87% of operating ones in urban areas; 39% of planned ones are in counties that have none today.")

    for status, v in (("operating", 3172), ("under_construction", 400), ("planned", 1199), ("paused", 79), ("current_total", 4771), ("tracked_total", 5098)):
        add(DCMAP, source="dcmap.us", metric="data_centers", geography="United States", value=v, unit="count", status=status,
            as_of="2026-10", counts=DCMAP_COUNTS,
            notes="current_total = operating + under construction + planned (3,172 + 400 + 1,199); tracked_total adds the 79 paused and 248 inactive or historical entries." if "total" in status else "")
    for name, st, v in (("Virginia", "VA", 591), ("Texas", "TX", 561)):
        add(DCMAP, source="dcmap.us", metric="data_centers", geography=name, state=st, value=v, unit="count", status="total",
            as_of="2026-10", counts=DCMAP_COUNTS, notes="'Counts include operating facilities and projects under construction or planned.'")

    add(VC, source="Visual Capitalist via Washington Examiner", metric="data_centers", geography="Virginia", state="VA", value=320,
        unit="count", status="operating", as_of="2026-04", counts="not stated in the article",
        notes="'Virginia still leads with 320 centers in operation.' Read in the Washington Examiner, not the original chart.")

    with open(HERE / "sources" / "census_cbp2023_naics518210_states.csv") as fh:
        for r in csv.DictReader(fh):
            add(CBP, source="US Census Bureau", metric="establishments_naics_518210", geography=r["state"], state=r["state"],
                value=int(r["establishments"]), unit="establishments", status="operating", as_of="2023-03", counts=CBP_COUNTS,
                notes=f"Employees (week of 12 March 2023): {int(r['employees']):,}; Census noise flag {r['emp_noise_flag']}.")

    add(EPRI_BRIEF, source="EPRI", metric="electricity_share", geography="United States", value="4-5", unit="percent of US electricity",
        status="estimate", as_of="2026", notes="'up from 4% to 5% today' (EPRI 2026 report); projected 9% to 17% by 2030.")
    add(EPRI_BRIEF, source="EPRI", metric="electricity_share", geography="United States", value="9-17", unit="percent of US electricity",
        status="projection", as_of="2030", notes="'about 60% higher than EPRI projected in 2024'; 56 to 132 GW nominal IT capacity in 2030, up from 35-44 GW in 2024.")
    add(EPRI, source="EPRI", metric="electricity_share", geography="Virginia", state="VA", value=">25", unit="percent of state electricity",
        status="estimate", as_of="2026", notes="Current estimate in EPRI's 2026 report: 'In several states, the share already exceeds 10%, with the highest concentration in Virginia, where the DC share exceeds 25%.'")
    add(EPRI_BRIEF, source="EPRI", metric="electricity_share", geography="Virginia", state="VA", value="39-57", unit="percent of state electricity",
        status="projection", as_of="2030", notes="'Virginia is the only state today where data centers consume over 20% of electricity, increasing to 39-57% by 2030. In the Medium scenario, eight states exceed 20% shares by 2030.'")

    add(LBNL, source="Lawrence Berkeley National Laboratory", metric="electricity_use", geography="United States", value=192, unit="TWh",
        status="estimate", as_of="2024", notes="4.7% of US electricity consumption; 521 to 843 TWh projected for 2030.")

    add(JLARC, source="JLARC (Virginia General Assembly)", metric="capacity_share", geography="Northern Virginia", state="VA", value=13,
        unit="percent of reported global operational capacity", status="estimate", as_of="2024",
        notes="'Northern Virginia is the largest data center market in the world, constituting 13 percent of all reported data center operational capacity globally and 25 percent of capacity in the Americas.'")
    add(JLARC, source="JLARC (Virginia General Assembly)", metric="residential_bill_increase", geography="Virginia (Dominion Energy)", state="VA",
        value="14-37", unit="USD per month, real", status="projection", as_of="2040",
        notes="'A typical residential customer of Dominion Energy could experience generation- and transmission-related costs increasing by an estimated $14 to $37 monthly in constant (or real) dollars by 2040.' Data centers 'are currently paying their full cost of service'.")
    add(JLARC, source="JLARC (Virginia General Assembly)", metric="economic_contribution", geography="Virginia", state="VA", value=74000,
        unit="jobs", status="estimate", as_of="2024", notes="'74,000 jobs, $5.5 billion in labor income, and $9.1 billion in GDP to Virginia's economy annually', mostly from construction.")

    jl = "JLARC staff analysis; a site can hold several buildings"
    add(JLARC_FULL, source="JLARC (Virginia General Assembly)", metric="data_center_sites", geography="Virginia", state="VA", value=150,
        unit="count", status="operating", as_of="2024", counts=jl, notes="'approximately 150 data center sites in Virginia, which collectively house around 340 data center buildings' (chapter 1).")
    add(JLARC_FULL, source="JLARC (Virginia General Assembly)", metric="data_center_buildings", geography="Virginia", state="VA", value=340,
        unit="count", status="operating", as_of="2024", counts=jl, notes="'around 340 data center buildings'; over 63 million square feet on 7,200 acres. 80% of the industry is in Loudoun, Prince William and Fairfax; Loudoun about half.")
    add(JLARC_FULL, source="JLARC (Virginia General Assembly)", metric="power_demand", geography="Virginia", state="VA", value=5050,
        unit="MW", status="estimate", as_of="2024", notes="'approximately 5,050 megawatts', from the 2024 peak load forecasts of Dominion Energy and three electric cooperatives (August 2023); 'roughly equivalent to the electricity needs of 2 million Virginia households'.")
    add(JLARC_FULL, source="JLARC (Virginia General Assembly)", metric="water_use", geography="Virginia", state="VA", value=2.1,
        unit="billion US gallons", status="estimate", as_of="2023", notes="'In 2023, the data center industry used an estimated 2.1 billion gallons of water, with just over a third coming from reclaimed water sources.' 11 buildings each used over 50 million gallons; one used 243 million (chapter 5).")

    # Google's Virginia sites, 2025 water consumption (million US gallons), as published
    va = [("Ashburn, VA", 53.2), ("Bristow, VA", 267.6), ("Leesburg, VA", 190.7), ("Sterling, VA", 199.8)]
    add(GOOGLE, source="Google", metric="water_consumption", geography="Virginia (Google's 4 sites)", state="VA",
        value=round(sum(v for _, v in va), 1), unit="million US gallons", status="operating", as_of="2025",
        notes="Sum of Google's published 2025 consumption for " + ", ".join(f"{s} {v}" for s, v in va) +
              " (GreenCalculus calculation; rows water-0001, 0003, 0017, 0036 of Data Center Water Benchmarks).")

    for n, r in enumerate(out, 1):
        r["id"] = f"usdc-{n:04d}"
    return out


def main():
    rs = rows()
    with open(HERE / "us-data-centers.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rs)
    (HERE / "us-data-centers.json").write_text(json.dumps(
        {"title": "US Data Centers by State: Every Published Count", "version": VERSION, "retrieved": RETRIEVED,
         "license": "CC-BY-4.0", "publisher": "GreenCalculus", "rows": rs}, indent=1, ensure_ascii=False) + "\n")
    print(len(rs), "rows")


if __name__ == "__main__":
    main()

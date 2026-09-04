# Clinical Data Platform

Analytics on synthetic electronic health records — building a reproducible
pipeline from raw clinical CSVs to answered business questions.

Built on [Synthea](https://synthetichealth.github.io/synthea/)'s 100-patient
synthetic sample: **108 patients, 5,473 encounters, 3,784 conditions,
75,343 observations.**

> **All data is synthetic.** Findings below demonstrate analytical method, not
> real epidemiology — the patterns reflect Synthea's generative models, not a
> real population. No real patient information appears anywhere in this repo.

---

## Selected findings

**Patients with social risk factors carry ~80% more disease.**
Patients flagged with social isolation, unemployment, or abuse average **9.5
distinct diagnoses** versus **5.2** for those without (n=76). Social
determinants are recorded in the same table as diagnoses — keeping them rather
than filtering them out is what made this visible.

**Disease burden is concentrated.** The top 10% of patients hold **23% of all
diagnoses** — the cohort a case-management programme would target.

**Care complexity scales with age.** Mean distinct diagnoses per patient:

| age group | diagnoses |
|---|---|
| young (0–17) | 4.3 |
| adult (18–39) | 7.2 |
| middleage (40–64) | 9.0 |
| elder (65+) | 13.0 |

**The naive answer to "most common condition" is wrong.** Ranking
`conditions.csv` by frequency returns *Medication review due* — an
administrative flag, 20.7% of all rows. Only **32%** of the table is actual
diagnoses; the rest are findings, situations, and social factors. Filtering by
SNOMED semantic tag changes the answer to **gingivitis, present in 75.9% of
patients.**

**No gender disparity in diagnosis count** — F 8.3, M 8.4. Reported as a null
result rather than dropped.

---

## What this demonstrates

- **Clinical data modelling** — SNOMED CT `SYSTEM`/`CODE`/`DESCRIPTION`
  triples, semantic tags, codes handled as identifiers rather than integers
- **Table grain** — separating record-level from patient-level counts, and
  choosing prevalence denominators deliberately
- **Joins with integrity checks** — foreign-key validation before merging,
  row-count assertions after
- **Meaningful vs missing nulls** — a null `STOP` on a condition means *still
  active*, not *absent data*
- **Reproducible transforms** — shared functions in `src/`, not copy-pasted
  notebook cells
- **Testing** — `pytest` covering the cleaning layer, including a leap-year
  case chosen so the test fails if the year length is wrong

## Stack

Python · pandas · matplotlib · pytest · Jupyter

---

## Repository layout

```
clinical-data-platform/
├── data/
│   ├── raw/         # Synthea CSVs (gitignored — download separately)
│   └── processed/   # derived outputs (gitignored, reproducible)
├── notebooks/
│   ├── 01_exploring_patients.ipynb      # profiling, age features, data quality
│   ├── 03_exploring_encounters.ipynb    # utilisation, length of stay, date ranges
│   ├── 04_exploring_conditions.ipynb    # diagnoses, coding, patient joins
│   └── 05_exploring_observations.ipynb  # vitals and labs (in progress)
├── src/
│   └── cleaning.py  # clean_patients(), clean_encounters()
├── tests/
│   └── test_cleaning.py
├── requirements.txt
└── README.md
```

## Design decisions

**Age is computed against an explicit `reference_date`.** `clean_patients()`
takes a date parameter defaulting to now. Without it, the same input produces
different ages on different days, patients silently cross age-group
boundaries, and no assertion can be written. Making the date explicit is what
made the cleaning layer testable.

**Every notebook derives its own data from `data/raw/`.** Notebooks call
`clean_patients()` rather than reading a cached CSV, so no notebook depends on
another having been run first, and categorical dtypes survive.

**Rows are classified, never deleted.** Condition types are labelled in a
`category` column instead of filtered at load. Filtering early would have
silently dropped 8 untagged rows that turned out to be real diagnoses —
including diabetic retinopathy and gout.

---

## Setup

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Getting the data

`data/` is gitignored, so fetch the dataset separately:

1. Download **"100 Sample Synthetic Patient Records, CSV"** from
   <https://synthea.mitre.org/downloads>
2. Unzip the CSVs into `data/raw/` (`data/raw/patients.csv`, etc.)
3. `mkdir -p data/processed`

### Running

```bash
pytest                      # from the repo root
jupyter lab notebooks/      # notebooks use ../data/raw paths
```

Notebooks are independent — each loads and cleans its own data, so they can be
run in any order.

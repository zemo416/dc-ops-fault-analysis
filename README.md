# dc-ops-fault-analysis

A small, reusable analysis toolkit for **data-center / mining-site operations fault logs**:
fault distribution, mean time to repair (MTTR), zone hot spots, weather correlation,
repeat-offender machines, and time-of-day patterns.

> **All data in this repo is synthetic.** It is randomly generated to demonstrate the method.
> No real company, client, machine, IP, or serial-number data is included.

## Why this exists

Operations teams usually react to alerts one at a time. Logging faults in a consistent format
makes it possible to answer questions like:

- Which fault types dominate, and how long does each take to fix?
- Are failures concentrated in particular zones (airflow, power, or cooling problems)?
- Do high-temperature faults track ambient weather?
- Which machines keep failing and should be repaired, replaced, or retired?

## Files

| File | Purpose |
|---|---|
| `gen_mock_data.py` | Generates a synthetic 90-day fault log and weather table |
| `analyze_faults.py` | Reads the CSVs, prints a summary, and saves charts |
| `fault_log.csv`, `weather.csv` | Example synthetic data |
| `charts/` | Example output charts |

## Quick start

```bash
pip install pandas numpy matplotlib
python3 gen_mock_data.py
python3 analyze_faults.py . charts
```

## Data format

`fault_log.csv`: `machine_id, model, zone, fault_type, detected_at, resolved_at, action`

`weather.csv`: `date, ambient_c, wind_mph, humidity_pct`

To use your own log, keep the same column names, use anonymized IDs, and record location only
at zone level.

## Example findings (synthetic data)

The generator deliberately embeds a few patterns so the analysis can be checked:
two hot-spot zones, a positive link between ambient temperature and high-temperature faults,
longer repair times for hashboard faults, and a small set of repeat-offender machines.
The script recovers all of them. These numbers describe the mock data, not any real site.

## Roadmap

- Add a Streamlit dashboard
- Add cost-of-downtime estimates
- Add alert-threshold backtesting

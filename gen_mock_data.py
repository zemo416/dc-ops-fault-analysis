"""Generate MOCK fault-log and weather data for a data-center ops analysis project.

All values are randomly generated. No real company, client, IP, or serial data.
Replace the CSVs with your own anonymized log later; the analysis script reads
the same column names.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# ---- daily weather (90 days) ----
days = pd.date_range("2026-07-01", periods=90, freq="D")
t = np.arange(len(days))
ambient = 30 + 6 * np.sin((t - 20) / 90 * np.pi) + rng.normal(0, 3, len(days))
wind = np.clip(rng.normal(4, 2, len(days)), 0, None)
humidity = np.clip(rng.normal(55, 15, len(days)), 15, 95)
weather = pd.DataFrame({
    "date": days.date,
    "ambient_c": ambient.round(1),
    "wind_mph": wind.round(1),
    "humidity_pct": humidity.round(0),
})

# ---- fault log ----
zones = ["A", "B", "C", "D", "E", "F"]
zone_w = np.array([0.10, 0.12, 0.14, 0.16, 0.22, 0.26])  # zone F is a built-in hot spot
models = ["Model-X1", "Model-X2", "Model-Y1"]
model_w = np.array([0.35, 0.45, 0.20])
types = ["offline", "zero_hashrate", "hashboard_fault", "fan_fault", "high_temp", "high_reject_rate"]
base_w = np.array([0.18, 0.30, 0.12, 0.15, 0.15, 0.10])
mean_hours = {"offline": 2, "zero_hashrate": 4, "hashboard_fault": 10,
              "fan_fault": 3, "high_temp": 1.5, "high_reject_rate": 5}
actions = {
    "offline": "check network / power cycle",
    "zero_hashrate": "check pool config / reboot",
    "hashboard_fault": "replace hashboard",
    "fan_fault": "replace fan",
    "high_temp": "clean intake / adjust cooling",
    "high_reject_rate": "check firmware / reboot",
}

machines = [f"M{i:04d}" for i in range(1, 801)]
repeat_offenders = rng.choice(machines, 25, replace=False)

rows = []
for i, d in enumerate(days):
    a = ambient[i]
    n = rng.poisson(14 + max(0.0, a - 32) * 1.5)
    for _ in range(n):
        w = base_w.copy()
        w[4] *= np.exp(max(0.0, a - 31) * 0.25)  # more high-temp faults on hot days
        w /= w.sum()
        ft = rng.choice(types, p=w)
        zone = rng.choice(zones, p=zone_w / zone_w.sum())
        model = rng.choice(models, p=model_w / model_w.sum())
        mid = rng.choice(repeat_offenders) if rng.random() < 0.12 else rng.choice(machines)
        if ft == "high_temp":
            hour = int(np.clip(rng.normal(14, 5), 0, 23))
        else:
            hour = int(rng.integers(0, 24))
        detected = pd.Timestamp(d) + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 60)))
        mh = mean_hours[ft] * (1.3 if zone == "F" else 1.0)
        repair_h = rng.gamma(2, mh / 2)
        resolved = detected + pd.Timedelta(hours=repair_h)
        rows.append({
            "machine_id": mid,
            "model": model,
            "zone": zone,
            "fault_type": ft,
            "detected_at": detected,
            "resolved_at": resolved,
            "action": actions[ft],
        })

faults = pd.DataFrame(rows).sort_values("detected_at").reset_index(drop=True)
faults.to_csv("fault_log.csv", index=False)
weather.to_csv("weather.csv", index=False)
print(f"fault_log.csv: {len(faults)} rows, weather.csv: {len(weather)} rows")

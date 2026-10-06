"""Analyze fault_log.csv + weather.csv. Works on mock data or your own anonymized log.

Required columns in fault_log.csv:
  machine_id, model, zone, fault_type, detected_at, resolved_at, action
Required columns in weather.csv:
  date, ambient_c, wind_mph, humidity_pct
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("charts")
out.mkdir(exist_ok=True)

f = pd.read_csv(src / "fault_log.csv", parse_dates=["detected_at", "resolved_at"])
w = pd.read_csv(src / "weather.csv", parse_dates=["date"])
f["repair_h"] = (f["resolved_at"] - f["detected_at"]).dt.total_seconds() / 3600
f["date"] = f["detected_at"].dt.normalize()
f["hour"] = f["detected_at"].dt.hour

lines = []

# 1. fault type distribution
c = f["fault_type"].value_counts()
lines.append("1) Fault type counts:\n" + c.to_string())
fig, ax = plt.subplots(figsize=(7, 4))
c.plot.barh(ax=ax, color="#3b6ea5")
ax.invert_yaxis(); ax.set_title("Faults by type"); ax.set_xlabel("count")
fig.tight_layout(); fig.savefig(out / "1_fault_types.png", dpi=150); plt.close(fig)

# 2. MTTR by type
m = f.groupby("fault_type")["repair_h"].agg(["count", "mean", "median"]).round(2)
lines.append("2) Repair time (hours) by type:\n" + m.to_string())
fig, ax = plt.subplots(figsize=(7, 4))
m["mean"].sort_values().plot.barh(ax=ax, color="#c9703a")
ax.set_title("Mean time to repair by fault type"); ax.set_xlabel("hours")
fig.tight_layout(); fig.savefig(out / "2_mttr.png", dpi=150); plt.close(fig)

# 3. zone hot spots (compare with even share)
z = f["zone"].value_counts().sort_index()
share = (z / z.sum() * 100).round(1)
lines.append("3) Fault share by zone (%):\n" + share.to_string())
fig, ax = plt.subplots(figsize=(7, 4))
share.plot.bar(ax=ax, color="#3b6ea5")
ax.axhline(100 / len(z), color="gray", ls="--", label="even share")
ax.set_title("Fault share by zone"); ax.set_ylabel("%"); ax.legend()
fig.tight_layout(); fig.savefig(out / "3_zones.png", dpi=150); plt.close(fig)

# 4. weather vs high_temp faults
daily = f[f["fault_type"] == "high_temp"].groupby("date").size().rename("high_temp_faults")
d = w.set_index("date").join(daily).fillna({"high_temp_faults": 0})
corr = d["ambient_c"].corr(d["high_temp_faults"])
lines.append(f"4) Correlation ambient temp vs daily high_temp faults: {corr:.2f}")
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(d["ambient_c"], d["high_temp_faults"], alpha=0.6)
ax.set_xlabel("ambient temp (C)"); ax.set_ylabel("high_temp faults per day")
ax.set_title(f"Ambient temp vs high-temp faults (r = {corr:.2f})")
fig.tight_layout(); fig.savefig(out / "4_weather.png", dpi=150); plt.close(fig)

# 5. repeat offenders
r = f["machine_id"].value_counts()
rep = r[r >= 3]
lines.append(f"5) Machines with >=3 faults: {len(rep)} of {r.size} machines "
             f"({rep.sum()/len(f)*100:.0f}% of all faults)\n" + rep.head(10).to_string())

# 6. time of day
h = f["hour"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(7, 4))
h.plot.bar(ax=ax, color="#3b6ea5")
ax.set_title("Faults by hour of day"); ax.set_xlabel("hour"); ax.set_ylabel("count")
fig.tight_layout(); fig.savefig(out / "6_hours.png", dpi=150); plt.close(fig)

summary = "\n\n".join(lines)
(out / "summary.txt").write_text(summary)
print(summary)

# dc-ops-fault-analysis

[English](#english) | [中文](#中文)

---

## English

A small, reusable toolkit for **data-center / mining-site operations fault logs**:
fault distribution, mean time to repair (MTTR), zone hot spots, weather correlation,
repeat-offender machines, and time-of-day patterns. Includes a daily logging template.

> **All data in this repo is synthetic.** It is randomly generated to demonstrate the method.
> No real company, client, machine, IP, or serial-number data is included.

### Why this exists

Operations teams usually react to alerts one at a time. Logging faults in a consistent format
makes it possible to answer questions like:

- Which fault types dominate, and how long does each take to fix?
- Are failures concentrated in particular zones (airflow, power, or cooling problems)?
- Do high-temperature faults track ambient weather?
- Which machines keep failing and should be repaired, replaced, or retired?

### Files

| File | Purpose |
|---|---|
| `ops_daily_log_template.xlsx` | Daily logging template (Fault Log, Daily Env, auto Summary). Bilingual instructions inside |
| `gen_mock_data.py` | Generates a synthetic 90-day fault log and weather table |
| `analyze_faults.py` | Reads the CSVs, prints a summary, and saves charts |
| `fault_log.csv`, `weather.csv` | Example synthetic data |
| `charts/` | Example output charts |

### Quick start

```bash
pip install pandas numpy matplotlib
python3 gen_mock_data.py
python3 analyze_faults.py . charts
```

### Using the template with your own log

1. Fill in the **Fault Log** and **Daily Env** sheets (blue cells are inputs; row 2 is an example).
2. Save each sheet as CSV: `fault_log.csv` and `weather.csv`.
3. Run `python3 analyze_faults.py <folder> charts`.

Privacy rules: use anonymized IDs (your own running numbers), record location only at zone level,
and never record client names, IPs, MACs, or serial numbers. Check your employer's policy first.

### Data format

`fault_log.csv`: `machine_id, model, zone, fault_type, detected_at, resolved_at, action`

`weather.csv`: `date, ambient_c, wind_mph, humidity_pct`

### Example findings (synthetic data)

The generator deliberately embeds a few patterns so the analysis can be checked:
two hot-spot zones, a positive link between ambient temperature and high-temperature faults,
longer repair times for hashboard faults, and a small set of repeat-offender machines.
The script recovers all of them. These numbers describe the mock data, not any real site.

### Roadmap

- Add a Streamlit dashboard
- Add cost-of-downtime estimates
- Add alert-threshold backtesting

---

## 中文

一个小型、可复用的**数据中心 / 矿场运维故障日志分析工具**:
故障类型分布、平均修复时长(MTTR)、区域热点、天气关联、反复故障机器、故障时段规律。
附带每日记录模板。

> **本仓库所有数据均为模拟数据**,由程序随机生成,仅用于演示分析方法。
> 不包含任何真实公司、客户、机器、IP 或序列号信息。

### 为什么做这个

运维团队通常是逐条响应告警。用统一格式记录故障后,就能回答这些问题:

- 哪类故障最多,各自要多久修好?
- 故障是否集中在某些区域(可能是风道、供电或散热问题)?
- 高温故障和外部气温是否相关?
- 哪些机器反复出故障,该修、该换还是该下架?

### 文件说明

| 文件 | 作用 |
|---|---|
| `ops_daily_log_template.xlsx` | 每日记录模板(故障记录、每日环境、自动汇总),内含中英文说明 |
| `gen_mock_data.py` | 生成 90 天的模拟故障日志和天气表 |
| `analyze_faults.py` | 读取 CSV,输出统计摘要并保存图表 |
| `fault_log.csv`、`weather.csv` | 模拟数据示例 |
| `charts/` | 示例输出图表 |

### 快速开始

```bash
pip install pandas numpy matplotlib
python3 gen_mock_data.py
python3 analyze_faults.py . charts
```

### 用模板记录自己的数据

1. 填写 **Fault Log** 和 **Daily Env** 两个表(蓝色格子是输入,第 2 行是示例)。
2. 每个表另存为 CSV:`fault_log.csv` 和 `weather.csv`。
3. 运行 `python3 analyze_faults.py <文件夹> charts`。

隐私规则:使用匿名编号(自己编的流水号),位置只记到区域级别,
绝不记录客户名、IP、MAC、序列号。使用前请先确认雇主的相关规定。

### 数据格式

`fault_log.csv`:`machine_id, model, zone, fault_type, detected_at, resolved_at, action`

`weather.csv`:`date, ambient_c, wind_mph, humidity_pct`

### 示例结论(模拟数据)

生成器故意埋入了几个规律,用来验证分析是否有效:
两个热点区域、气温与高温故障正相关、算力板故障修复时间更长、少数机器反复故障。
脚本都能把它们找出来。这些数字描述的是模拟数据,不代表任何真实站点。

### 后续计划

- 增加 Streamlit 看板
- 增加停机成本估算
- 增加告警阈值回测

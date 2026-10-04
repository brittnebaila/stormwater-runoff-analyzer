import pandas as pd
import matplotlib.pyplot as plt

print("ANALYZER STARTED")

df = pd.read_csv("data/mercer_creek_streamflow.csv")

df["Collect Date (local)"] = pd.to_datetime(
    df["Collect Date (local)"]
)

df = df.rename(columns={
    "Collect Date (local)": "date",
    "Stage (ft)": "stage_ft",
    "Discharge (cfs)": "streamflow_cfs"
})

print("Mercer Creek Streamflow Data")
print("----------------------------")

print("\nFirst 5 Rows:")
print(df.head())

print("\nSummary Statistics:")
print(df[["stage_ft", "streamflow_cfs"]].describe())

highest_flow = df.loc[df["streamflow_cfs"].idxmax()]
lowest_flow = df.loc[df["streamflow_cfs"].idxmin()]
average_flow = df["streamflow_cfs"].mean()

print("\nHighest Flow Day:")
print(highest_flow[["date", "streamflow_cfs"]])

print("\nLowest Flow Day:")
print(lowest_flow[["date", "streamflow_cfs"]])

print("\nAverage Streamflow:")
print(round(average_flow, 2), "cfs")

high_flow_threshold = df["streamflow_cfs"].quantile(0.90)

high_flow_events = df[
    df["streamflow_cfs"] >= high_flow_threshold
]

print("\nHigh Flow Threshold:")
print(round(high_flow_threshold, 2), "cfs")

print("\nHigh Flow Events:")
print(high_flow_events[["date", "streamflow_cfs"]])

rainfall = pd.read_csv(
    "data/bellevue_rainfall.csv",
    usecols=[0, 1, 2, 3]
)

rainfall["Collect Date (local)"] = pd.to_datetime(
    rainfall["Collect Date (local)"]
)

rainfall = rainfall.rename(columns={
    "Collect Date (local)": "date",
    "Precipitation (inches)": "precipitation_in"
})

combined = pd.merge(
    df,
    rainfall[["date", "precipitation_in"]],
    on="date"
)

print("\nCombined Rainfall and Streamflow Data:")
print(combined.head())

correlation = combined["precipitation_in"].corr(
    combined["streamflow_cfs"]
)

print("\nRainfall vs Streamflow Correlation:")
print(round(correlation, 3))

combined["rainfall_lag_1"] = combined["precipitation_in"].shift(1)
combined["rainfall_lag_2"] = combined["precipitation_in"].shift(2)

lag_1_correlation = combined["rainfall_lag_1"].corr(
    combined["streamflow_cfs"]
)

lag_2_correlation = combined["rainfall_lag_2"].corr(
    combined["streamflow_cfs"]
)

print("\n1-Day Lag Correlation:")
print(round(lag_1_correlation, 3))

print("\n2-Day Lag Correlation:")
print(round(lag_2_correlation, 3))

wettest_day = combined.loc[
    combined["precipitation_in"].idxmax()
]

wettest_date = wettest_day["date"]

next_day = combined[
    combined["date"] == wettest_date + pd.Timedelta(days=1)
]

print("\nWettest Day:")
print(
    wettest_day[
        ["date", "precipitation_in", "streamflow_cfs"]
    ]
)

print("\nStreamflow One Day Later:")
print(
    next_day[
        ["date", "streamflow_cfs"]
    ]
)

peak_flow_day = combined.loc[
    combined["streamflow_cfs"].idxmax()
]

peak_date = peak_flow_day["date"]

previous_day = combined[
    combined["date"] == peak_date - pd.Timedelta(days=1)
]

print("\nPeak Streamflow Day:")
print(
    peak_flow_day[
        ["date", "precipitation_in", "streamflow_cfs"]
    ]
)

print("\nRainfall One Day Before Peak Flow:")
print(
    previous_day[
        ["date", "precipitation_in", "streamflow_cfs"]
    ]
)

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(12, 8),
    sharex=True
)

ax1.bar(
    combined["date"],
    combined["precipitation_in"]
)

ax1.set_title("Bellevue Rainfall and Mercer Creek Streamflow")
ax1.set_ylabel("Precipitation (inches)")

ax2.plot(
    combined["date"],
    combined["streamflow_cfs"]
)

ax2.axhline(
    y=high_flow_threshold,
    linestyle="--",
    label="90th Percentile Threshold"
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Streamflow (cfs)")
ax2.legend()

plt.tight_layout()

plt.savefig(
    "output/rainfall_streamflow_combined.png",
    dpi=150
)

plt.show()

plt.figure(figsize=(12, 6))

plt.plot(
    df["date"],
    df["streamflow_cfs"],
    label="Streamflow"
)

plt.axhline(
    y=high_flow_threshold,
    linestyle="--",
    label="90th Percentile Threshold"
)

plt.title("Mercer Creek Daily Streamflow")
plt.xlabel("Date")
plt.ylabel("Streamflow (cfs)")
plt.legend()

plt.tight_layout()

plt.savefig("output/mercer_creek_streamflow.png")

plt.show()

plt.figure(figsize=(8, 6))

plt.scatter(
    combined["precipitation_in"],
    combined["streamflow_cfs"]
)

plt.title("Rainfall vs Mercer Creek Streamflow")
plt.xlabel("Daily Precipitation (inches)")
plt.ylabel("Streamflow (cfs)")

plt.tight_layout()

plt.savefig("output/rainfall_vs_streamflow.png")

plt.show()

correlation_labels = [
    "Same Day",
    "1-Day Lag",
    "2-Day Lag"
]

correlation_values = [
    correlation,
    lag_1_correlation,
    lag_2_correlation
]

plt.figure(figsize=(8, 5))

plt.bar(
    correlation_labels,
    correlation_values
)

plt.title("Rainfall vs Streamflow Correlation")
plt.xlabel("Rainfall Timing")
plt.ylabel("Correlation")

plt.tight_layout()

plt.savefig("output/correlation_comparison.png")

plt.show()


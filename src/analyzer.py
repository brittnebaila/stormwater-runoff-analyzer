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
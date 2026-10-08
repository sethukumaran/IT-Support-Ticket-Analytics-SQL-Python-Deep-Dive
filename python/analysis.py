import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("synthetic_it_support_tickets.csv")
OUT = Path("outputs")
FIG = Path("visualizations")
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

df = pd.read_csv(DATA)

# -----------------------------
# 1. EDA / Data Quality
# -----------------------------
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["resolution_time_hours"] = pd.to_numeric(df["resolution_time_hours"], errors="coerce")

print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("Duplicate ticket IDs:", df["ticket_id"].duplicated().sum())
print("\nNumeric summary:\n", df.describe())

# agent_first_reply is a message text field, not a timestamp.
print("\nSample agent_first_reply values:\n", df["agent_first_reply"].head())

# Derived KPI flags
df["is_resolved"] = df["status"].eq("resolved")
df["is_backlog"] = df["status"].isin(["open", "in_progress", "on_hold"])
df["negative_sentiment"] = df["customer_sentiment"].isin(["negative", "very_negative"])
df["year_month"] = df["created_at"].dt.to_period("M").astype(str)

# -----------------------------
# 2. Executive KPI table
# -----------------------------
kpis = pd.DataFrame([{
    "total_tickets": len(df),
    "unique_customers": df["customer_id"].nunique(),
    "resolved_rate_pct": df["is_resolved"].mean() * 100,
    "backlog_rate_pct": df["is_backlog"].mean() * 100,
    "reopen_rate_pct": df["reopened"].mean() * 100,
    "avg_csat": df["csat_score"].mean(),
    "negative_sentiment_pct": df["negative_sentiment"].mean() * 100,
    "avg_resolution_hours": df["resolution_time_hours"].mean(),
    "median_resolution_hours": df["resolution_time_hours"].median()
}])
kpis.to_csv(OUT / "executive_kpis.csv", index=False)

# -----------------------------
# 3. EDA summaries
# -----------------------------
def summarize(dim):
    out = df.groupby(dim, dropna=False).agg(
        tickets=("ticket_id","size"),
        resolved_rate=("is_resolved","mean"),
        backlog_rate=("is_backlog","mean"),
        avg_resolution_hours=("resolution_time_hours","mean"),
        median_resolution_hours=("resolution_time_hours","median"),
        reopen_rate=("reopened","mean"),
        avg_csat=("csat_score","mean"),
        negative_sentiment_rate=("negative_sentiment","mean")
    ).reset_index()
    out.to_csv(OUT / f"{dim}_kpis.csv", index=False)
    return out

for dim in ["issue_type","product_area","channel","priority",
            "customer_segment","sla_plan","platform","region"]:
    summarize(dim)

monthly = df.groupby("year_month").agg(
    tickets=("ticket_id","size"),
    resolved_rate=("is_resolved","mean"),
    backlog_rate=("is_backlog","mean"),
    avg_csat=("csat_score","mean"),
    negative_sentiment_rate=("negative_sentiment","mean"),
    avg_resolution_hours=("resolution_time_hours","mean")
).reset_index()
monthly.to_csv(OUT / "monthly_kpis.csv", index=False)

# -----------------------------
# 4. Visualizations
# -----------------------------
plt.figure(figsize=(12,5))
plt.plot(monthly["year_month"], monthly["tickets"], marker="o")
plt.xticks(rotation=60, fontsize=8)
plt.title("Monthly IT Support Ticket Volume")
plt.xlabel("Month"); plt.ylabel("Tickets")
plt.tight_layout()
plt.savefig(FIG / "01_monthly_ticket_volume.png", dpi=160)
plt.close()

status = df["status"].value_counts().sort_values()
plt.figure(figsize=(8,5))
status.plot(kind="barh")
plt.title("Ticket Status Distribution")
plt.xlabel("Tickets"); plt.ylabel("Status")
plt.tight_layout()
plt.savefig(FIG / "02_status_distribution.png", dpi=160)
plt.close()

issue_csat = df.groupby("issue_type")["csat_score"].mean().sort_values()
plt.figure(figsize=(9,5))
issue_csat.plot(kind="barh")
plt.title("Average CSAT by Issue Type")
plt.xlabel("Average CSAT"); plt.ylabel("Issue Type")
plt.tight_layout()
plt.savefig(FIG / "03_csat_by_issue_type.png", dpi=160)
plt.close()

priority_order = ["low","medium","high","urgent"]
priority_res = df.groupby("priority")["resolution_time_hours"].mean().reindex(priority_order)
plt.figure(figsize=(8,5))
priority_res.plot(kind="bar")
plt.title("Average Resolution Time by Priority")
plt.xlabel("Priority"); plt.ylabel("Hours")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG / "04_resolution_by_priority.png", dpi=160)
plt.close()

issue_neg = df.groupby("issue_type")["negative_sentiment"].mean().sort_values() * 100
plt.figure(figsize=(9,5))
issue_neg.plot(kind="barh")
plt.title("Negative Sentiment Rate by Issue Type")
plt.xlabel("Negative Sentiment (%)"); plt.ylabel("Issue Type")
plt.tight_layout()
plt.savefig(FIG / "05_negative_sentiment_by_issue.png", dpi=160)
plt.close()

channel_csat = df.groupby("channel")["csat_score"].mean().sort_values()
plt.figure(figsize=(9,5))
channel_csat.plot(kind="bar")
plt.title("Average CSAT by Support Channel")
plt.xlabel("Channel"); plt.ylabel("Average CSAT")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(FIG / "06_csat_by_channel.png", dpi=160)
plt.close()

resolved = df.loc[df["is_resolved"] & df["resolution_time_hours"].notna(),
                  "resolution_time_hours"]
plt.figure(figsize=(10,5))
plt.hist(resolved, bins=40)
plt.title("Resolution Time Distribution — Resolved Tickets")
plt.xlabel("Resolution Time (hours)"); plt.ylabel("Tickets")
plt.tight_layout()
plt.savefig(FIG / "07_resolution_distribution.png", dpi=160)
plt.close()

priority_vol = df["priority"].value_counts().reindex(priority_order)
plt.figure(figsize=(8,5))
priority_vol.plot(kind="bar")
plt.title("Ticket Volume by Priority")
plt.xlabel("Priority"); plt.ylabel("Tickets")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG / "08_priority_volume.png", dpi=160)
plt.close()

print("\nAnalysis complete. Outputs saved under outputs/ and visualizations/.")

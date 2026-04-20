"""
transport-microservice/src/services/analytics_service.py

Computes historical disruption rates from the joined weather-alert table.
Blends empirical rates derived from past T1 disruption events with
domain knowledge priors, producing per-severity disruption probabilities
used as input to the forecast service.
"""

import pandas as pd

from src.dependencies.db_client import joined_table
from src.marshallers.dataframe_marshaller import prepare_analysis_df
from src.repositories.db_repo import scan_all_items

SEVERITY_COLUMNS = [
    "tempSeverity",
    "rainSeverity",
    "windSeverity",
    "humiditySeverity",
    "sunSeverity",
]

DOMAIN_RATES = {
    "tempSeverity": {"Hot": 0.60, "Warm": 0.50, "Mild": 0.25, "Cold": 0.30},
    "rainSeverity": {
        "Heavy rain": 0.90,
        "Moderate rain": 0.70,
        "Light rain": 0.50,
        "No rain": 0.15,
    },
    "windSeverity": {
        "Gale": 0.70,
        "Windy": 0.50,
        "Breezy": 0.30,
        "Calm": 0.10,
    },
    "humiditySeverity": {
        "Extreme Humidity": 0.55,
        "High Humidity": 0.45,
        "Moderate Humidity": 0.25,
        "Low Humidity": 0.10,
    },
    "sunSeverity": {"Cloudy": 0.55, "Partly Cloudy": 0.35, "Sunny": 0.15},
}

HISTORICAL_BLEND = 0.3

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def load_joined_analysis_df(
    location: str | None = None, table=None
) -> pd.DataFrame:
    t = table or joined_table
    items = scan_all_items(t)
    df = pd.DataFrame(items)
    df = prepare_analysis_df(df)

    if location:
        df = df[df["location"] == location]

    return df


def compute_disruption_rates(df: pd.DataFrame) -> dict:
    """
    Blend empirical disruption rates from historical data with
    domain knowledge rates.
    """
    blended_rates = {}

    for col in SEVERITY_COLUMNS:
        empirical = df.groupby(col)["disruption"].mean().to_dict()
        blended_rates[col] = {}

        for category, domain_rate in DOMAIN_RATES[col].items():
            empirical_rate = empirical.get(category, domain_rate)
            blended_rates[col][category] = round(
                HISTORICAL_BLEND * empirical_rate
                + (1 - HISTORICAL_BLEND) * domain_rate,
                4,
            )

    return blended_rates


def _compute_rates_by_column(
    df: pd.DataFrame,
    group_col: str,
    label_key: str,
    ordered_labels: list[str],
) -> dict:
    rates = (
        df.groupby(group_col)["disruption"]
        .agg(["mean", "sum", "count"])
        .rename(
            columns={
                "mean": "disruption_rate",
                "sum": "disruption_days",
                "count": "sample_size",
            }
        )
        .reindex(ordered_labels)
        .dropna()
        .reset_index()
    )
    ranked = rates.sort_values("disruption_rate")

    return {
        label_key: [
            {
                "label": row[group_col],
                "disruption_rate": round(row["disruption_rate"], 4),
                "sample_size": int(row["sample_size"]),
                "disruption_days": int(row["disruption_days"]),
                "non_disruption_days": int(
                    row["sample_size"] - row["disruption_days"]
                ),
            }
            for _, row in rates.iterrows()
        ],
        "best": ranked.iloc[0][group_col],
        "worst": ranked.iloc[-1][group_col],
    }


def _compute_by_year(
    df: pd.DataFrame,
    group_col: str,
    label_key: str,
    ordered_labels: list[str],
) -> dict:
    """
    Generic helper to compute disruption rates for all time and per year.
    """
    years = sorted(df["date"].dt.year.unique().tolist())
    result = {
        "all_time": _compute_rates_by_column(
            df, group_col, label_key, ordered_labels
        )
    }
    for year in years:
        result[str(year)] = _compute_rates_by_column(
            df[df["date"].dt.year == year],
            group_col,
            label_key,
            ordered_labels,
        )
    return result


def disruption_rate_by_day_of_week(df: pd.DataFrame) -> dict:
    """
    Calculate historical disruption rate for each day of the week.
    Returns rates for all time and broken down by year.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()
    return _compute_by_year(df, "day_of_week", "by_day", DAYS_OF_WEEK)


def disruption_rate_by_month(df: pd.DataFrame) -> dict:
    """
    Calculate historical disruption rate for each month.
    Returns rates for all time and broken down by year.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    return _compute_by_year(df, "month", "by_month", MONTHS)


def disruption_by_weather_condition(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["tempMax_C"] = df["tempMax_C"].astype(float)
    df["maxWindSpeed_kmh"] = df["maxWindSpeed_kmh"].astype(float)
    df["rainfall_mm"] = df["rainfall_mm"].astype(float)

    def rate(subset):
        if len(subset) == 0:
            return None
        return {
            "disruption_rate": round(subset["disruption"].mean(), 4),
            "sample_size": len(subset),
            "disruption_days": int(subset["disruption"].sum()),
        }

    def threshold_above(df, col, thresholds, unit_key):
        return [
            {unit_key: t, **rate(df[df[col] >= t])}
            for t in thresholds
            if len(df[df[col] >= t]) > 0
        ]

    return {
        "temperature": threshold_above(
            df, "tempMax_C", [15, 18, 20, 22, 25, 28, 30, 35], "threshold_c"
        ),
        "wind": threshold_above(
            df, "maxWindSpeed_kmh", [10, 20, 30], "threshold_kmh"
        ),
        "rainfall": threshold_above(
            df, "rainfall_mm", [5, 10, 15, 20, 25, 30], "threshold_mm"
        ),
    }


def generate_summary(df: pd.DataFrame) -> dict:
    """
    High-level summary stats for dashboard header.
    """
    return {
        "total_days": len(df),
        "total_disruption_days": int(df["disruption"].sum()),
        "overall_disruption_rate": round(df["disruption"].mean(), 4),
        "data_from": df["date"].min(),
        "data_to": df["date"].max(),
    }


def generate_analytics_report(location: str, table=None) -> dict:
    df = load_joined_analysis_df(location=location, table=table)

    return {
        "location": location,
        "overall": generate_summary(df),
        "best_worst_day_of_week": disruption_rate_by_day_of_week(df),
        "best_worst_month": disruption_rate_by_month(df),
        "weather_threshold_analysis": disruption_by_weather_condition(df),
    }

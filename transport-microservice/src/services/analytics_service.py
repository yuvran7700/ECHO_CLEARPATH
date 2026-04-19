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


def load_joined_analysis_df() -> pd.DataFrame:
    items = scan_all_items(joined_table)
    df = pd.DataFrame(items)
    return prepare_analysis_df(df)


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

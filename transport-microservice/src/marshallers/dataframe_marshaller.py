# transport-microservice/src/marshallers/dataframe_marshaller.py
from decimal import Decimal

import pandas as pd


def prepare_analysis_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw DynamoDB items into a clean analysis DataFrame.
    - Converts Decimal → float
    - Normalises disruption column to bool
    - Coerces rainfall_mm to numeric
    - Drops rows with missing disruption or rainfall
    """
    cleaned = df.copy()

    # Convert all Decimal columns to float
    for col in cleaned.columns:
        cleaned[col] = cleaned[col].apply(
            lambda x: float(x) if isinstance(x, Decimal) else x
        )

    cleaned["disruption"] = (
        cleaned["disruption"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False})
    )

    cleaned["rainfall_mm"] = pd.to_numeric(
        cleaned["rainfall_mm"], errors="coerce"
    )
    cleaned = cleaned.dropna(subset=["disruption", "rainfall_mm"])
    cleaned["disruption"] = cleaned["disruption"].astype(bool)

    return cleaned

# tests/unit/test_dataframe_marshaller.py
from decimal import Decimal

import pandas as pd
from src.marshallers.dataframe_marshaller import prepare_analysis_df


class TestPrepareAnalysisDf:
    def test_converts_decimal_to_float(self, raw_dynamodb_df):
        result = prepare_analysis_df(raw_dynamodb_df)
        assert isinstance(result["rainfall_mm"].iloc[0], float)
        assert isinstance(result["tempMax_C"].iloc[0], float)

    def test_disruption_true_string_becomes_bool_true(self, raw_dynamodb_df):
        result = prepare_analysis_df(raw_dynamodb_df)
        assert result["disruption"].iloc[0] is True
        assert result["disruption"].dtype == bool

    def test_disruption_false_string_becomes_bool_false(self, raw_dynamodb_df):
        result = prepare_analysis_df(raw_dynamodb_df)
        assert result["disruption"].iloc[1] is False

    def test_rainfall_mm_is_numeric(self, raw_dynamodb_df):
        result = prepare_analysis_df(raw_dynamodb_df)
        assert pd.api.types.is_numeric_dtype(result["rainfall_mm"])

    def test_drops_rows_with_missing_rainfall(self, df_with_missing_data):
        result = prepare_analysis_df(df_with_missing_data)
        assert len(result) == 1
        assert result["date"].iloc[0] == "2025-08-03"

    def test_drops_rows_with_missing_disruption(self, df_with_missing_data):
        result = prepare_analysis_df(df_with_missing_data)
        assert all(result["disruption"].notna())

    def test_does_not_modify_original_dataframe(self, raw_dynamodb_df):
        original_dtypes = raw_dynamodb_df.dtypes.copy()
        prepare_analysis_df(raw_dynamodb_df)
        assert raw_dynamodb_df.dtypes.equals(original_dtypes)

    def test_returns_dataframe(self, raw_dynamodb_df):
        result = prepare_analysis_df(raw_dynamodb_df)
        assert isinstance(result, pd.DataFrame)

    def test_handles_whitespace_in_disruption(self):
        df = pd.DataFrame(
            [
                {
                    "date": "2025-09-01",
                    "rainfall_mm": Decimal("5.0"),
                    "disruption": "  True  ",
                }
            ]
        )
        result = prepare_analysis_df(df)
        assert result["disruption"].iloc[0] is True

    def test_handles_uppercase_disruption(self):
        df = pd.DataFrame(
            [
                {
                    "date": "2025-09-01",
                    "rainfall_mm": Decimal("5.0"),
                    "disruption": "TRUE",
                }
            ]
        )
        result = prepare_analysis_df(df)
        assert result["disruption"].iloc[0] is True

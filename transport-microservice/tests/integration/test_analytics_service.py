# tests/integration/test_analytics_service.py
import boto3
import pandas as pd
import pytest
from src.services.analytics_service import (
    DAYS_OF_WEEK,
    SEVERITY_COLUMNS,
    compute_disruption_rates,
    disruption_by_weather_condition,
    disruption_rate_by_day_of_week,
    disruption_rate_by_month,
    generate_analytics_report,
    generate_summary,
    load_joined_analysis_df,
)


@pytest.fixture(scope="module")
def live_table(joined_table_name):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    return dynamodb.Table(joined_table_name)


@pytest.fixture(scope="module")
def live_df(live_table):
    """Load real data from DynamoDB once for all tests in this module."""
    return load_joined_analysis_df(table=live_table)


class TestLoadJoinedAnalysisDf:
    def test_returns_dataframe(self, live_df):
        assert isinstance(live_df, pd.DataFrame)

    def test_has_rows(self, live_df):
        assert len(live_df) > 0

    def test_has_required_columns(self, live_df):
        required = ["date", "disruption", "rainfall_mm"] + SEVERITY_COLUMNS
        for col in required:
            assert col in live_df.columns, f"Missing column: {col}"

    def test_disruption_column_is_bool(self, live_df):
        assert live_df["disruption"].dtype == bool

    def test_rainfall_mm_is_numeric(self, live_df):
        assert pd.api.types.is_numeric_dtype(live_df["rainfall_mm"])

    def test_no_missing_disruption_values(self, live_df):
        assert live_df["disruption"].notna().all()

    def test_no_missing_rainfall_values(self, live_df):
        assert live_df["rainfall_mm"].notna().all()


class TestComputeDisruptionRatesIntegration:
    def test_returns_all_severity_columns(self, live_df):
        rates = compute_disruption_rates(live_df)
        for col in SEVERITY_COLUMNS:
            assert col in rates

    def test_all_rates_between_0_and_1(self, live_df):
        rates = compute_disruption_rates(live_df)
        for col, categories in rates.items():
            for category, rate in categories.items():
                assert 0 <= rate <= 1, f"{col}.{category} = {rate}"


class TestDisruptionRateByDayOfWeekIntegration:
    def test_returns_all_time_key(self, live_df):
        result = disruption_rate_by_day_of_week(live_df)
        assert "all_time" in result

    def test_all_7_days_present(self, live_df):
        result = disruption_rate_by_day_of_week(live_df)
        labels = [d["label"] for d in result["all_time"]["by_day"]]
        for day in DAYS_OF_WEEK:
            assert day in labels

    def test_best_and_worst_are_valid_days(self, live_df):
        result = disruption_rate_by_day_of_week(live_df)
        assert result["all_time"]["best"] in DAYS_OF_WEEK
        assert result["all_time"]["worst"] in DAYS_OF_WEEK


class TestDisruptionRateByMonthIntegration:
    def test_returns_all_time_key(self, live_df):
        result = disruption_rate_by_month(live_df)
        assert "all_time" in result

    def test_best_and_worst_present(self, live_df):
        result = disruption_rate_by_month(live_df)
        assert "best" in result["all_time"]
        assert "worst" in result["all_time"]


class TestDisruptionByWeatherConditionIntegration:
    def test_returns_temperature_wind_rainfall(self, live_df):
        result = disruption_by_weather_condition(live_df)
        assert "temperature" in result
        assert "wind" in result
        assert "rainfall" in result

    def test_all_sample_sizes_positive(self, live_df):
        result = disruption_by_weather_condition(live_df)
        for category in result.values():
            for entry in category:
                assert entry["sample_size"] > 0


class TestGenerateSummaryIntegration:
    def test_total_days_matches_df_length(self, live_df):
        result = generate_summary(live_df)
        assert result["total_days"] == len(live_df)

    def test_disruption_rate_between_0_and_1(self, live_df):
        result = generate_summary(live_df)
        assert 0 <= result["overall_disruption_rate"] <= 1


class TestGenerateAnalyticsReportIntegration:
    def test_returns_required_keys(self, live_table):
        result = generate_analytics_report("parramatta", table=live_table)
        assert "location" in result
        assert "overall" in result
        assert "best_worst_day_of_week" in result
        assert "best_worst_month" in result
        assert "weather_threshold_analysis" in result

    def test_location_matches_input(self, live_table):
        result = generate_analytics_report("parramatta", table=live_table)
        assert result["location"] == "parramatta"

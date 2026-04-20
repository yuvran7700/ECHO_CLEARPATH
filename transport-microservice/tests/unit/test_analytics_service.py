# tests/unit/test_analytics_service.py
import pandas as pd
from src.services.analytics_service import (
    DOMAIN_RATES,
    HISTORICAL_BLEND,
    compute_disruption_rates,
    disruption_by_weather_condition,
    disruption_rate_by_day_of_week,
    disruption_rate_by_month,
    generate_summary,
)


class TestComputeDisruptionRates:
    def test_returns_all_severity_columns(self, sample_analytics_df):
        rates = compute_disruption_rates(sample_analytics_df)
        assert "tempSeverity" in rates
        assert "rainSeverity" in rates
        assert "windSeverity" in rates
        assert "humiditySeverity" in rates
        assert "sunSeverity" in rates

    def test_blends_empirical_with_domain_rates(self, sample_analytics_df):
        rates = compute_disruption_rates(sample_analytics_df)
        # Hot has 2 disruptions out of 2 days = 1.0 empirical
        # blended = 0.3 * 1.0 + 0.7 * 0.60 = 0.72
        expected = round(
            HISTORICAL_BLEND * 1.0
            + (1 - HISTORICAL_BLEND) * DOMAIN_RATES["tempSeverity"]["Hot"],
            4,
        )
        assert rates["tempSeverity"]["Hot"] == expected

    def test_falls_back_to_domain_rate_when_no_empirical_data(
        self, sample_analytics_df
    ):
        rates = compute_disruption_rates(sample_analytics_df)
        # "Extreme Humidity" not in sample data so should use domain rate
        expected = round(
            HISTORICAL_BLEND
            * DOMAIN_RATES["humiditySeverity"]["Extreme Humidity"]
            + (1 - HISTORICAL_BLEND)
            * DOMAIN_RATES["humiditySeverity"]["Extreme Humidity"],
            4,
        )
        assert rates["humiditySeverity"]["Extreme Humidity"] == expected

    def test_all_rates_between_0_and_1(self, sample_analytics_df):
        rates = compute_disruption_rates(sample_analytics_df)
        for col, categories in rates.items():
            for category, rate in categories.items():
                assert (
                    0 <= rate <= 1
                ), f"{col}.{category} = {rate} is out of range"


class TestDisruptionRateByDayOfWeek:
    def test_returns_all_time_key(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        assert "all_time" in result

    def test_returns_year_keys(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        assert "2025" in result

    def test_all_time_has_by_day_key(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        assert "by_day" in result["all_time"]

    def test_all_time_has_best_and_worst(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        assert "best" in result["all_time"]
        assert "worst" in result["all_time"]

    def test_each_day_has_required_fields(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        for day in result["all_time"]["by_day"]:
            assert "label" in day
            assert "disruption_rate" in day
            assert "sample_size" in day
            assert "disruption_days" in day
            assert "non_disruption_days" in day

    def test_disruption_rate_between_0_and_1(self, sample_analytics_df):
        result = disruption_rate_by_day_of_week(sample_analytics_df)
        for day in result["all_time"]["by_day"]:
            assert 0 <= day["disruption_rate"] <= 1

    def test_does_not_modify_original_df(self, sample_analytics_df):
        original_cols = list(sample_analytics_df.columns)
        disruption_rate_by_day_of_week(sample_analytics_df)
        assert list(sample_analytics_df.columns) == original_cols


class TestDisruptionRateByMonth:
    def test_returns_all_time_key(self, sample_analytics_df):
        result = disruption_rate_by_month(sample_analytics_df)
        assert "all_time" in result

    def test_all_time_has_by_month_key(self, sample_analytics_df):
        result = disruption_rate_by_month(sample_analytics_df)
        assert "by_month" in result["all_time"]

    def test_all_time_has_best_and_worst(self, sample_analytics_df):
        result = disruption_rate_by_month(sample_analytics_df)
        assert "best" in result["all_time"]
        assert "worst" in result["all_time"]

    def test_only_includes_months_with_data(self, sample_analytics_df):
        result = disruption_rate_by_month(sample_analytics_df)
        months_returned = [m["label"] for m in result["all_time"]["by_month"]]
        assert "January" in months_returned
        assert "March" in months_returned
        assert "June" in months_returned
        assert "February" not in months_returned

    def test_january_has_100_percent_disruption_rate(
        self, sample_analytics_df
    ):
        result = disruption_rate_by_month(sample_analytics_df)
        january = next(
            m
            for m in result["all_time"]["by_month"]
            if m["label"] == "January"
        )
        assert january["disruption_rate"] == 1.0


class TestDisruptionByWeatherCondition:
    def test_returns_temperature_wind_rainfall_keys(self, sample_analytics_df):
        result = disruption_by_weather_condition(sample_analytics_df)
        assert "temperature" in result
        assert "wind" in result
        assert "rainfall" in result

    def test_each_threshold_has_required_fields(self, sample_analytics_df):
        result = disruption_by_weather_condition(sample_analytics_df)
        for entry in result["temperature"]:
            assert "threshold_c" in entry
            assert "disruption_rate" in entry
            assert "sample_size" in entry
            assert "disruption_days" in entry

    def test_higher_temp_threshold_has_smaller_sample(
        self, sample_analytics_df
    ):
        result = disruption_by_weather_condition(sample_analytics_df)
        temps = result["temperature"]
        sizes = [t["sample_size"] for t in temps]
        assert sizes == sorted(sizes, reverse=True)

    def test_excludes_thresholds_with_no_data(self, sample_analytics_df):
        result = disruption_by_weather_condition(sample_analytics_df)
        for entry in result["rainfall"]:
            assert entry["sample_size"] > 0

    def test_empty_threshold_returns_none(self):
        """When no rows meet a threshold, it is excluded from results."""
        df = pd.DataFrame(
            [
                {
                    "date": "2025-07-01",
                    "disruption": True,
                    "tempMax_C": 10.0,
                    "maxWindSpeed_kmh": 5.0,
                    "rainfall_mm": 0.0,
                }
            ]
        )
        result = disruption_by_weather_condition(df)
        # No rows have rainfall >= 5mm so rainfall thresholds should be empty
        assert result["rainfall"] == []


class TestGenerateSummary:
    def test_returns_required_fields(self, sample_analytics_df):
        result = generate_summary(sample_analytics_df)
        assert "total_days" in result
        assert "total_disruption_days" in result
        assert "overall_disruption_rate" in result
        assert "data_from" in result
        assert "data_to" in result

    def test_total_days_correct(self, sample_analytics_df):
        result = generate_summary(sample_analytics_df)
        assert result["total_days"] == 7

    def test_total_disruption_days_correct(self, sample_analytics_df):
        result = generate_summary(sample_analytics_df)
        assert result["total_disruption_days"] == 3

    def test_overall_disruption_rate_correct(self, sample_analytics_df):
        result = generate_summary(sample_analytics_df)
        assert result["overall_disruption_rate"] == round(3 / 7, 4)

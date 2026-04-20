# tests/unit/test_disruption_forecast_service.py
from src.services.disruption_forecast_service import (
    classify_risk,
    predict_disruption_risk_from_conditions,
)


class TestClassifyRisk:
    def test_low_when_below_0_3(self):
        assert classify_risk(0.20) == "Low"

    def test_moderate_when_between_0_3_and_0_4(self):
        assert classify_risk(0.35) == "Moderate"

    def test_high_when_between_0_4_and_0_45(self):
        assert classify_risk(0.42) == "High"

    def test_very_high_when_above_0_45(self):
        assert classify_risk(0.50) == "Very High"

    def test_boundary_exactly_0_3_is_moderate(self):
        assert classify_risk(0.30) == "Moderate"

    def test_boundary_exactly_0_4_is_high(self):
        assert classify_risk(0.40) == "High"

    def test_boundary_exactly_0_45_is_very_high(self):
        assert classify_risk(0.45) == "Very High"


class TestPredictDisruptionRiskFromConditions:
    def test_returns_risk_and_risk_level(self, sample_disruption_rates):
        conditions = {
            "tempSeverity": "Mild",
            "rainSeverity": "No rain",
            "windSeverity": "Breezy",
            "humiditySeverity": "Moderate Humidity",
            "sunSeverity": "Sunny",
        }
        result = predict_disruption_risk_from_conditions(
            conditions, sample_disruption_rates
        )
        assert "risk" in result
        assert "risk_level" in result

    def test_risk_is_between_0_and_1(self, sample_disruption_rates):
        conditions = {
            "tempSeverity": "Warm",
            "rainSeverity": "Light rain",
            "windSeverity": "Windy",
            "humiditySeverity": "High Humidity",
            "sunSeverity": "Cloudy",
        }
        result = predict_disruption_risk_from_conditions(
            conditions, sample_disruption_rates
        )
        assert 0 <= result["risk"] <= 1

    def test_high_risk_conditions_score_higher_than_low_risk(
        self, sample_disruption_rates
    ):
        high_risk = predict_disruption_risk_from_conditions(
            {
                "tempSeverity": "Hot",
                "rainSeverity": "Heavy rain",
                "windSeverity": "Gale",
                "humiditySeverity": "Extreme Humidity",
                "sunSeverity": "Cloudy",
            },
            sample_disruption_rates,
        )

        low_risk = predict_disruption_risk_from_conditions(
            {
                "tempSeverity": "Mild",
                "rainSeverity": "No rain",
                "windSeverity": "Calm",
                "humiditySeverity": "Low Humidity",
                "sunSeverity": "Sunny",
            },
            sample_disruption_rates,
        )

        assert high_risk["risk"] > low_risk["risk"]

    def test_returns_unknown_when_no_matching_rates(self):
        conditions = {
            "tempSeverity": "Unknown",
            "rainSeverity": "Unknown",
            "windSeverity": "Unknown",
            "humiditySeverity": "Unknown",
            "sunSeverity": "Unknown",
        }
        result = predict_disruption_risk_from_conditions(conditions, {})
        assert result["risk"] is None
        assert result["risk_level"] == "Unknown"

    def test_partial_conditions_normalises_weights(
        self, sample_disruption_rates
    ):
        # Only temp and rain provided — should still return valid risk
        conditions = {
            "tempSeverity": "Warm",
            "rainSeverity": "No rain",
        }
        result = predict_disruption_risk_from_conditions(
            conditions, sample_disruption_rates
        )
        assert result["risk"] is not None
        assert 0 <= result["risk"] <= 1

    def test_risk_is_rounded_to_4_decimal_places(
        self, sample_disruption_rates
    ):
        conditions = {
            "tempSeverity": "Warm",
            "rainSeverity": "Light rain",
            "windSeverity": "Breezy",
            "humiditySeverity": "High Humidity",
            "sunSeverity": "Partly Cloudy",
        }
        result = predict_disruption_risk_from_conditions(
            conditions, sample_disruption_rates
        )
        assert result["risk"] == round(result["risk"], 4)

# tests/unit/test_join_service.py
from src.services.join_service import build_joined_item


class TestBuildJoinedItem:
    def test_returns_disruption_true_when_alert_present(
        self, weather_item, alert_item
    ):
        result = build_joined_item(weather_item, alert_item)
        assert result["disruption"] is True

    def test_returns_disruption_false_when_no_alert(self, weather_item):
        result = build_joined_item(weather_item, None)
        assert result["disruption"] is False

    def test_sets_account_name_from_alert(self, weather_item, alert_item):
        result = build_joined_item(weather_item, alert_item)
        assert result["account_name"] == "T1 Sydney Trains"

    def test_sets_classification_from_alert(self, weather_item, alert_item):
        result = build_joined_item(weather_item, alert_item)
        assert result["classification"] == "unknown"

    def test_sets_account_name_unavailable_when_no_alert(self, weather_item):
        result = build_joined_item(weather_item, None)
        assert result["account_name"] == "Unavailable"

    def test_sets_classification_unavailable_when_no_alert(self, weather_item):
        result = build_joined_item(weather_item, None)
        assert result["classification"] == "Unavailable"

    def test_preserves_all_weather_fields(self, weather_item, alert_item):
        result = build_joined_item(weather_item, alert_item)
        for key, value in weather_item.items():
            assert result[key] == value

    def test_does_not_modify_original_weather_item(
        self, weather_item, alert_item
    ):
        original = weather_item.copy()
        build_joined_item(weather_item, alert_item)
        assert weather_item == original

    def test_handles_alert_with_missing_fields(self, weather_item):
        incomplete_alert = {"date": "2025-07-01"}
        result = build_joined_item(weather_item, incomplete_alert)
        assert result["disruption"] is True
        assert result["account_name"] is None
        assert result["classification"] is None

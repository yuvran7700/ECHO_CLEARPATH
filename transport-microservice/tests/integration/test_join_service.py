# tests/integration/test_join_service.py
import pytest
from src.repositories.db_repo import query_by_date, scan_all_items
from src.services.join_service import run_join_for_date


@pytest.fixture(scope="module")
def sample_date(live_weather_location_table):
    items = scan_all_items(live_weather_location_table)
    assert len(items) > 0, "Weather location table is empty"
    return items[0]["date"]


@pytest.fixture(scope="module")
def joined_items(live_joined_table):
    return scan_all_items(live_joined_table)


class TestJoinedTableData:
    def test_joined_table_has_rows(self, joined_items):
        assert len(joined_items) > 0

    def test_every_row_has_date(self, joined_items):
        for item in joined_items:
            assert "date" in item
            assert item["date"] is not None

    def test_every_row_has_location(self, joined_items):
        for item in joined_items:
            assert "location" in item
            assert item["location"] is not None

    def test_every_row_has_disruption_field(self, joined_items):
        for item in joined_items:
            assert "disruption" in item

    def test_disruption_is_boolean(self, joined_items):
        for item in joined_items:
            message = (
                f"Expected bool, got {type(item['disruption'])} "
                f"for {item['date']}"
            )
            assert isinstance(item["disruption"], bool), message

    def test_non_disrupted_rows_have_unavailable_account_name(
        self, joined_items
    ):
        non_disrupted = [i for i in joined_items if i["disruption"] is False]
        for item in non_disrupted:
            assert item["account_name"] == "Unavailable"

    def test_no_duplicate_date_location_combinations(self, joined_items):
        seen = set()
        for item in joined_items:
            key = (item["date"], item["location"])
            assert key not in seen, f"Duplicate found: {key}"
            seen.add(key)

    def test_both_locations_present(self, joined_items):
        locations = {item["location"] for item in joined_items}
        assert "parramatta" in locations or "sydney" in locations


class TestRunJoinForDate:
    def test_writes_rows_to_joined_table(
        self,
        sample_date,
        live_weather_location_table,
        live_alert_table,
        live_joined_table,
    ):
        run_join_for_date(
            sample_date,
            weather_table=live_weather_location_table,
            alerts_table=live_alert_table,
            target_joined_table=live_joined_table,
        )
        result = query_by_date(live_joined_table, sample_date)
        assert len(result) > 0

    def test_joined_rows_have_correct_date(
        self,
        sample_date,
        live_weather_location_table,
        live_alert_table,
        live_joined_table,
    ):
        run_join_for_date(
            sample_date,
            weather_table=live_weather_location_table,
            alerts_table=live_alert_table,
            target_joined_table=live_joined_table,
        )
        result = query_by_date(live_joined_table, sample_date)
        for item in result:
            assert item["date"] == sample_date

    def test_joined_rows_have_disruption_field(
        self,
        sample_date,
        live_weather_location_table,
        live_alert_table,
        live_joined_table,
    ):
        run_join_for_date(
            sample_date,
            weather_table=live_weather_location_table,
            alerts_table=live_alert_table,
            target_joined_table=live_joined_table,
        )
        result = query_by_date(live_joined_table, sample_date)
        for item in result:
            assert "disruption" in item
            assert isinstance(item["disruption"], bool)

    def test_skips_date_with_no_weather_records(
        self,
        live_weather_location_table,
        live_alert_table,
        live_joined_table,
    ):
        run_join_for_date(
            "1900-01-01",
            weather_table=live_weather_location_table,
            alerts_table=live_alert_table,
            target_joined_table=live_joined_table,
        )
        result = query_by_date(live_joined_table, "1900-01-01")
        assert len(result) == 0

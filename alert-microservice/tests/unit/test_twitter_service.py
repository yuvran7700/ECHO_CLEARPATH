from datetime import datetime

from src.services.twitter_service import generate_weekly_queries


def test_weekly_queries_generation():
    start = datetime.strptime("2026-02-01", "%Y-%m-%d")
    end = datetime.strptime("2026-02-20", "%Y-%m-%d")

    queries = generate_weekly_queries(start, end)

    assert len(queries) == 3
    assert "since:2026-02-01 until:2026-02-08" in queries[0]
    assert "since:2026-02-08 until:2026-02-15" in queries[1]
    assert "since:2026-02-15 until:2026-02-20" in queries[2]

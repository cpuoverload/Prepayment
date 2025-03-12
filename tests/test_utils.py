from utils import get_last_day_of_month


def test_get_last_day_of_month():
    assert get_last_day_of_month("Apr 2024") == "30/04/2024"

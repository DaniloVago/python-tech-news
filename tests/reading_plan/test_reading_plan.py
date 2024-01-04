from tech_news.analyzer.reading_plan import ReadingPlanService  # noqa: F401, E261, E501
import pytest
from unittest.mock import patch, Mock


def test_reading_plan_group_news():
    data = [
        {"title": "Notícia 1", "reading_time": 4},
        {"title": "Notícia 2", "reading_time": 3},
        {"title": "Notícia 3", "reading_time": 10},
        {"title": "Notícia 4", "reading_time": 20},
    ]

    mock_data = Mock(return_value=data)

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        mock_data,
    ):
        reading_plan_service = ReadingPlanService()

        first_result = reading_plan_service.group_news_for_available_time(10)
        first_expected = {
            "readable": [
                {
                    "unfilled_time": 3,
                    "chosen_news": [
                        ("Notícia 1", 4),
                        ("Notícia 2", 3),
                    ],
                },
                {
                    "unfilled_time": 0,
                    "chosen_news": [
                        ("Notícia 3", 10),
                    ],
                },
            ],
            "unreadable": [
                ("Notícia 4", 20),
            ],
        }
        assert first_result == first_expected

        second_result = reading_plan_service.group_news_for_available_time(3)
        second_expected = {
            "readable": [
                {
                    "unfilled_time": 0,
                    "chosen_news": [
                        ("Notícia 2", 3),
                    ],
                },
            ],
            "unreadable": [
                ("Notícia 1", 4),
                ("Notícia 3", 10),
                ("Notícia 4", 20),
            ],
        }
        assert second_result == second_expected

        with pytest.raises(ValueError):
            reading_plan_service.group_news_for_available_time(0)

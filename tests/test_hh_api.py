from unittest.mock import Mock, patch

import pytest
import requests

from src.hh_api import HhRu

from .conftest import hh_ru


def test_init(hh_ru):
    assert hh_ru.session.headers["Authorization"] == "Bearer test_access_token"


def test_init_without_access_token():
    with pytest.raises(ValueError, match="ACCESS_TOKEN is required"):
        HhRu("")


def test_connect_to_api(hh_ru):
    expected_data = {"items": [{"id": "123", "name": "Python Developer"}]}
    mock_response = Mock()
    mock_response.json.return_value = expected_data

    with patch.object(hh_ru.session, "get", return_value=mock_response) as mock_get:
        result = hh_ru._connect_to_api(
            "https://api.hh.ru/vacancies",
            {"text": "Python", "page": 0, "per_page": 1},
        )

    assert result == expected_data
    mock_response.raise_for_status.assert_called_once_with()
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        params={"text": "Python", "page": 0, "per_page": 1},
    )


def test_connect_to_api_http_error(hh_ru):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Bad Request")

    with patch.object(hh_ru.session, "get", return_value=mock_response):
        with pytest.raises(requests.HTTPError, match="Bad Request"):
            hh_ru._connect_to_api(
                "https://api.hh.ru/vacancies",
                {"text": "Python"},
            )


def test_get_vacancies(hh_ru):
    expected_vacancies = [
        {"id": "123", "name": "Python Developer"},
        {"id": "456", "name": "Junior Python Developer"},
    ]

    with patch.object(
        hh_ru,
        "_connect_to_api",
        return_value={
            "items": expected_vacancies,
            "pages": 1,
        },
    ) as mock_connect:
        result = hh_ru.get_vacancies("Python", 2)

    assert result == expected_vacancies
    mock_connect.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        {
            "text": "Python",
            "search_field": "name",
            "per_page": 2,
            "page": 0,
        },
    )


def test_get_vacancies_multiple_pages(hh_ru):
    first_page = [{"id": "123", "name": "Python Developer"}]
    second_page = [{"id": "456", "name": "Junior Python Developer"}]

    with patch.object(
        hh_ru,
        "_connect_to_api",
        side_effect=[
            {"items": first_page, "pages": 2},
            {"items": second_page, "pages": 2},
        ],
    ) as mock_connect:
        result = hh_ru.get_vacancies("Python", 2)

    assert result == first_page + second_page
    assert mock_connect.call_count == 2


def test_get_vacancies_zero(hh_ru):
    with patch.object(hh_ru, "_connect_to_api") as mock_connect:
        result = hh_ru.get_vacancies("Python", 0)

    assert result == []
    mock_connect.assert_not_called()


def test_get_vacancies_negative_top_n(hh_ru):
    with pytest.raises(ValueError, match="top_n is required"):
        hh_ru.get_vacancies("Python", -1)


def test_get_vacancies_no_results(hh_ru, capsys):
    with patch.object(
        hh_ru,
        "_connect_to_api",
        return_value={"items": [], "pages": 0},
    ) as mock_connect:
        result = hh_ru.get_vacancies("Python", 10)

    assert result == []
    assert mock_connect.call_count == 1
    assert "only 0 were found" in capsys.readouterr().out


def test_get_vacancies_fewer_results_than_requested(hh_ru, capsys):
    vacancies = [{"id": "123", "name": "Python Developer"}]

    with patch.object(
        hh_ru,
        "_connect_to_api",
        return_value={"items": vacancies, "pages": 1},
    ):
        result = hh_ru.get_vacancies("Python", 10)

    assert result == vacancies
    assert "only 1 were found" in capsys.readouterr().out


def test_get_vacancies_does_not_exceed_top_n(hh_ru):
    first_page = [
        {"id": "1", "name": "Python Developer"},
        {"id": "2", "name": "Junior Python Developer"},
    ]

    with patch.object(
        hh_ru,
        "_connect_to_api",
        return_value={"items": first_page, "pages": 10},
    ):
        result = hh_ru.get_vacancies("Python", 1)

    assert len(result) == 1
    assert result == first_page[:1]

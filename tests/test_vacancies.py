import pytest

from src.vacancies import Vacancy


@pytest.mark.parametrize(
    ("salary_data", "expected_salary"),
    [
        (None, 0),
        ({"from": 2500, "to": 3600, "currency": "USD"}, 298800),
        ({"from": 500000, "to": 1000000, "currency": "KZT"}, 150000),
        ({"from": 80000, "to": 130000, "currency": "RUR"}, 130000),
        ({"from": 70000, "to": None, "currency": "RUR"}, 70000),
        ({"from": 2300, "to": None, "currency": "BYR"}, 57500),
        ({"from": 30000, "to": 45000, "currency": "KGS"}, 41400),
        ({"from": 15000000, "to": 20000000, "currency": "UZS"}, 132000),
        ({"from": 50000, "to": None, "currency": "UNKNOWN"}, 50000),
    ],
)
def test_cast_to_object_salary(salary_data, expected_salary):
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": salary_data,
        "snippet": {"requirement": "Python"},
    }

    vacancy = Vacancy.cast_to_object(vacancy_data)

    assert vacancy.salary == expected_salary
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://api.hh.ru/vacancies/123"
    assert vacancy.requirement == "Python"


def test_cast_to_object_without_snippet():
    """Отсутствующий snippet не должен приводить к ошибке."""
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": None,
    }

    vacancy = Vacancy.cast_to_object(vacancy_data)

    assert vacancy.requirement is None
    assert vacancy.salary == 0


def test_cast_to_object_with_none_requirement():
    """Проверка преобразования requirement=None."""
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": {"from": 90000, "to": None, "currency": "RUR"},
        "snippet": {"requirement": None},
    }

    vacancy = Vacancy.cast_to_object(vacancy_data)

    assert vacancy.requirement is None
    assert vacancy.salary == 90000


def test_cast_to_object_without_requirement_key():
    """Отсутствующий ключ requirement должен давать None."""
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": None,
        "snippet": {},
    }

    vacancy = Vacancy.cast_to_object(vacancy_data)

    assert vacancy.requirement is None


def test_vacancy_init(vacancy_1):
    assert vacancy_1.name == "Стажер / Junior BI engenineer"
    assert vacancy_1.url == "https://api.hh.ru/vacancies/125828331?host=hh.ru"
    assert vacancy_1.salary == 0
    assert vacancy_1.requirement is not None


def test_validate_salary_none():
    vacancy = Vacancy("Python Developer", "https://example.com", None, None)

    assert vacancy.salary == 0


def test_lt_correct(vacancy_1, vacancy_2):
    assert vacancy_1 < vacancy_2


def test_lt_false(vacancy_1, vacancy_2):
    assert not vacancy_2 < vacancy_1


def test_gt_correct(vacancy_1, vacancy_2):
    assert vacancy_2 > vacancy_1


def test_gt_false(vacancy_1, vacancy_2):
    assert not vacancy_1 > vacancy_2


def test_to_json(vacancy_1):
    assert vacancy_1.to_json() == {
        "name": "Стажер / Junior BI engenineer",
        "url": "https://api.hh.ru/vacancies/125828331?host=hh.ru",
        "salary": 0,
        "requirement": vacancy_1.requirement,
    }


def test_to_json_with_none_requirement(vacancy_without_requirement):
    result = vacancy_without_requirement.to_json()

    assert result["requirement"] is None
    assert result["salary"] == 90000

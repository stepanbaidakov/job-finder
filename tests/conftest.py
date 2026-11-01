import pytest

from src.hh_api import HhRu
from src.vacancies import Vacancy


@pytest.fixture
def hh_ru():
    return HhRu("test_access_token")


@pytest.fixture
def vacancy_1():
    return Vacancy(
        "Стажер / Junior BI engenineer",
        "https://api.hh.ru/vacancies/125828331?host=hh.ru",
        0,
        "Знание инструментов визуализации данных (например, Power BI, Qlik) будет преимуществом. "
        "- Владение языками программирования (например, <highlighttext>Python</highlighttext>, R) приветствуется. "
        "- Стремление учиться, адаптироваться...",
    )


@pytest.fixture
def vacancy_2():
    return Vacancy(
        "QA Engineer",
        "https://api.hh.ru/vacancies/125789503?host=hh.ru",
        110000,
        "Умение писать запросы и работать с базами данных (SQL).  Базовое владение "
        "<highlighttext>Python</highlighttext> для анализа информации.  Понимание основ статистики и вероятности.  ",
    )


@pytest.fixture
def vacancy_without_requirement():
    return Vacancy(
        "Python Developer",
        "https://api.hh.ru/vacancies/123456?host=hh.ru",
        90000,
        None,
    )

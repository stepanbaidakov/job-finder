from src.user_communication import filter_vacancies, sort_vacancies


def test_sort_vacancies(vacancy_1, vacancy_2):
    """Проверка сортировки вакансий по убыванию зарплаты."""
    vacancies = [vacancy_1, vacancy_2]

    result = sort_vacancies(vacancies)

    assert result == [vacancy_2, vacancy_1]


def test_sort_vacancies_empty_list():
    """Проверка сортировки пустого списка."""
    assert sort_vacancies([]) == []


def test_filter_vacancies_by_keyword(vacancy_1, vacancy_2):
    """Проверка фильтрации по ключевому слову."""
    vacancies = [vacancy_1, vacancy_2]

    result = filter_vacancies(vacancies, ["Python"])

    assert result == [vacancy_1, vacancy_2]


def test_filter_vacancies_case_insensitive(vacancy_1, vacancy_2):
    """Проверка фильтрации без учёта регистра."""
    vacancies = [vacancy_1, vacancy_2]

    result = filter_vacancies(vacancies, ["pYtHoN"])

    assert result == [vacancy_1, vacancy_2]


def test_filter_vacancies_multiple_keywords(vacancy_1, vacancy_2):
    """Проверка фильтрации по нескольким ключевым словам."""
    vacancies = [vacancy_1, vacancy_2]

    result = filter_vacancies(vacancies, ["Power BI", "SQL"])

    assert result == [vacancy_1, vacancy_2]


def test_filter_vacancies_no_matches(vacancy_1, vacancy_2):
    """Если совпадений нет, возвращается пустой список."""
    vacancies = [vacancy_1, vacancy_2]

    result = filter_vacancies(vacancies, ["JavaScript"])

    assert result == []


def test_filter_vacancies_empty_keywords(vacancy_1, vacancy_2):
    """Пустой список ключевых слов не находит вакансии."""
    vacancies = [vacancy_1, vacancy_2]

    result = filter_vacancies(vacancies, [])

    assert result == []


def test_filter_vacancies_skips_none_requirement(
    vacancy_1,
    vacancy_without_requirement,
):
    """Вакансия с requirement=None пропускается при фильтрации."""
    vacancies = [vacancy_1, vacancy_without_requirement]

    result = filter_vacancies(vacancies, ["Python"])

    assert result == [vacancy_1]
    assert vacancy_without_requirement not in result


def test_filter_vacancies_returns_empty_when_only_requirement_is_none(
    vacancy_without_requirement,
):
    """Если у вакансии нет требований, совпадений не будет."""
    result = filter_vacancies(
        [vacancy_without_requirement],
        ["Python"],
    )

    assert result == []


def test_filter_vacancies_with_none_requirement_and_empty_keywords(
    vacancy_without_requirement,
):
    """Пустой список ключевых слов не вызывает ошибку."""
    result = filter_vacancies(
        [vacancy_without_requirement],
        [],
    )

    assert result == []

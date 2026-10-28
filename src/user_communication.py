from src.vacancies import Vacancy


def sort_vacancies(vacancies_list: list[Vacancy]) -> list[Vacancy]:
    """Sort vacancies by salary in descending order."""
    return sorted(vacancies_list, key=lambda vacancy: vacancy.salary, reverse=True)


def filter_vacancies(vacancies_list: list[Vacancy], filter_words: list) -> list[Vacancy]:
    """Filter vacancies by keywords in their requirements."""
    filtered_list = []
    normalized_words = [word.casefold() for word in filter_words]

    for vacancy in vacancies_list:
        requirement = vacancy.requirement
        if requirement is None:
            continue
        requirement = requirement.casefold()

        if any(word in requirement for word in normalized_words):
            filtered_list.append(vacancy)

    return filtered_list

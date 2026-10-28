import os
from src.hh_api import HhRu
from src.vacancies import Vacancy
from src.user_communication import filter_vacancies
from src.file_worker import JSONSaver


def main():
    """Interact with the user."""
    search_query = input("Enter a job title to search for: ")
    top_n = int(input("Enter the number of top vacancies to display: "))
    all_filter_words = input("Enter keywords to filter vacancies: ").split(",")

    access_token = os.getenv("ACCESS_TOKEN")

    if not access_token:
        raise ValueError("ACCESS_TOKEN is not set.")

    hh_api = HhRu(access_token)
    hh_vacancies = hh_api.get_vacancies(search_query, top_n)
    vacancies_list = [Vacancy.cast_to_object(vacancy) for vacancy in hh_vacancies]
    filtered_list = filter_vacancies(vacancies_list, all_filter_words)

    final_list = [vacancy.to_json() for vacancy in filtered_list]

    file_saver = JSONSaver()
    file_saver.add_vacancies_to_file(final_list)

    get_vacancies_input = input("Would you like to retrieve vacancies from the file? Yes/No: ").lower()

    if get_vacancies_input == "yes":
        urls_input = input("Enter the URL(s) of the vacancy/vacancies you are looking for: ").split(", ")
        got_vacancies = file_saver.get_vacancies_from_file(urls_input)
        print(got_vacancies)
    else:
        pass


if __name__ == "__main__":
    main()

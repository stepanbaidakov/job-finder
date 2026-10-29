from abc import ABC, abstractmethod

import requests
from dotenv import load_dotenv

load_dotenv()


class HhAPI(ABC):
    """Base class for interacting with the API."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _connect_to_api(self, url, params):
        pass

    @abstractmethod
    def get_vacancies(self, key_word, top_n):
        pass


class HhRu(HhAPI):
    """Class for interacting with the API."""

    def __init__(self, access_token: str):
        if not access_token:
            raise ValueError("ACCESS_TOKEN is required.")

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def _connect_to_api(self, url: str, params: dict):
        """Connect to the API."""
        return self.__connect_to_api(url, params)

    def __connect_to_api(self, url: str, params: dict) -> dict:
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, key_word: str, top_n: int) -> list[dict]:
        """Retrieve vacancies as a list of dictionaries."""

        if top_n < 0:
            raise ValueError("top_n is required.")
        if top_n == 0:
            return []
        max_results = min(top_n, 2000)
        per_page = min(100, max_results)
        params = {"text": key_word, "search_field": "name", "per_page": per_page, "page": 0}

        vacancies = []
        url = "https://api.hh.ru/vacancies"

        while len(vacancies) < max_results:
            data = self._connect_to_api(url, params)
            items = data.get("items", [])
            if not items:
                print(f"Requested {max_results} vacancies, " f"but only {len(vacancies)} were found.")
                break
            remaining = max_results - len(vacancies)
            vacancies.extend(items[:remaining])
            if len(vacancies) >= max_results:
                break
            if params["page"] + 1 >= data.get("pages", 0):
                print(f"Requested {max_results} vacancies, " f"but only {len(vacancies)} were found.")
                break
            params["page"] += 1

        return vacancies

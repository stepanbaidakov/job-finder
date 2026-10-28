import json
import os.path
from abc import ABC, abstractmethod
from typing import Any

from config import DATA_DIR


class BaseJSONSaver(ABC):
    """Base class for working with the API."""

    @abstractmethod
    def add_vacancies_to_file(self, vacancies: list[dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def get_vacancies_from_file(self, urls: list[str]) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancies(self) -> None:
        pass


class JSONSaver(BaseJSONSaver):
    """Class for working with a file."""

    file_name: str

    def __init__(self, file_name: str ="vacancies.json"):
        self.__file_path = os.path.join(DATA_DIR, file_name)

    def _read_data(self) -> list[dict[str, Any]]:
        """Read vacancies from the file."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []


    def _write_data(self, data: list[dict[str, Any]]) -> None:
        """Write vacancies to the file."""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def add_vacancies_to_file(self, vacancies: list[dict[str, Any]]) -> None:
        """Add vacancies to the file."""

        data = self._read_data()
        existing_urls = {vacancy["url"] for vacancy in data}
        new_vacancies_found = False
        for vacancy in vacancies:
            if vacancy["url"] not in existing_urls:
                data.append(vacancy)
                existing_urls.add(vacancy["url"])
                new_vacancies_found = True
        if new_vacancies_found:
            self._write_data(data)


    def get_vacancies_from_file(self, urls: list) -> list:
        """Return vacancies matching the provided URLs."""

        data = self._read_data()
        url_set = set(urls)
        return [vacancy for vacancy in data if vacancy["url"] in url_set]

    def delete_vacancies(self):
        """Clear all vacancies from the file."""
        self._write_data([])

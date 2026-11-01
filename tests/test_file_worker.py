import json
import os

from config import DATA_DIR
from src.file_worker import JSONSaver


def test_jsonsaver_init():
    file_worker = JSONSaver("new_vacancies.json")

    assert file_worker._JSONSaver__file_path == os.path.join(DATA_DIR, "new_vacancies.json")


def test_add_vacancies():
    file_worker = JSONSaver()
    vacancies = [
        {
            "name": "Инженер по тестированию",
            "url": "https://api.hh.ru/vacancies/126274858?host=hh.ru",
            "salary": 0,
            "requirements": "Опыт работы с автотестами, базовые знания Python.",
        }
    ]

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file(vacancies)

    report_path = os.path.join(DATA_DIR, "vacancies.json")

    with open(report_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0] == vacancies[0]


def test_add_duplicate_vacancies():
    file_worker = JSONSaver()
    vacancy = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": 100000,
        "requirements": "Python",
    }

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file([vacancy])
    file_worker.add_vacancies_to_file([vacancy])

    report_path = os.path.join(DATA_DIR, "vacancies.json")

    with open(report_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0] == vacancy


def test_add_vacancies_with_existing_url():
    file_worker = JSONSaver()
    original_vacancy = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": 100000,
        "requirements": "Python",
    }
    updated_vacancy = {
        "name": "Senior Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": 150000,
        "requirements": "Python, Django",
    }

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file([original_vacancy])
    file_worker.add_vacancies_to_file([updated_vacancy])

    report_path = os.path.join(DATA_DIR, "vacancies.json")

    with open(report_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0] == original_vacancy


def test_add_vacancies_new_file(tmp_path):
    file_name = "new_vacancies.json"
    file_worker = JSONSaver(file_name)
    file_path = os.path.join(DATA_DIR, file_name)

    # Ensure the file does not exist before the test.
    if os.path.exists(file_path):
        os.remove(file_path)

    vacancy = {
        "name": "Инженер по тестированию",
        "url": "https://api.hh.ru/vacancies/126274858?host=hh.ru",
        "salary": 0,
        "requirements": "Python",
    }

    file_worker.add_vacancies_to_file([vacancy])

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [vacancy]

    os.remove(file_path)


def test_get_vacancies_from_file():
    file_worker = JSONSaver()
    vacancies = [
        {
            "name": "Python Developer",
            "url": "https://api.hh.ru/vacancies/123",
            "salary": 100000,
            "requirements": "Python",
        },
        {
            "name": "Tester",
            "url": "https://api.hh.ru/vacancies/456",
            "salary": 80000,
            "requirements": "Testing",
        },
    ]

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file(vacancies)

    result = file_worker.get_vacancies_from_file(["https://api.hh.ru/vacancies/456"])

    assert len(result) == 1
    assert result[0] == vacancies[1]


def test_get_multiple_vacancies_from_file():
    file_worker = JSONSaver()
    vacancies = [
        {
            "name": "Python Developer",
            "url": "https://api.hh.ru/vacancies/123",
            "salary": 100000,
            "requirements": "Python",
        },
        {
            "name": "Tester",
            "url": "https://api.hh.ru/vacancies/456",
            "salary": 80000,
            "requirements": "Testing",
        },
    ]

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file(vacancies)

    result = file_worker.get_vacancies_from_file(
        [
            "https://api.hh.ru/vacancies/123",
            "https://api.hh.ru/vacancies/456",
        ]
    )

    assert len(result) == 2
    assert result == vacancies


def test_get_vacancies_not_found():
    file_worker = JSONSaver()
    vacancy = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": 100000,
        "requirements": "Python",
    }

    file_worker.delete_vacancies()
    file_worker.add_vacancies_to_file([vacancy])

    result = file_worker.get_vacancies_from_file(["https://api.hh.ru/vacancies/999"])

    assert result == []


def test_delete_vacancies():
    file_worker = JSONSaver()
    vacancy = {
        "name": "Python Developer",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": 100000,
        "requirements": "Python",
    }

    file_worker.add_vacancies_to_file([vacancy])
    file_worker.delete_vacancies()

    report_path = os.path.join(DATA_DIR, "vacancies.json")

    with open(report_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == []


def test_read_data_when_file_does_not_exist(tmp_path):
    file_worker = JSONSaver("missing_vacancies.json")
    file_path = os.path.join(DATA_DIR, "missing_vacancies.json")

    if os.path.exists(file_path):
        os.remove(file_path)

    assert file_worker._read_data() == []

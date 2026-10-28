class Vacancy:
    """Class for working with vacancies."""

    name: str
    url: str
    salary: int | float
    requirement: str | None

    __slots__ = ("name", "url", "salary", "requirement")

    def __init__(self, name, url, salary, requirement):
        validated_salary = self.__validate_salary(salary)

        self.name = name
        self.url = url
        self.salary = validated_salary
        self.requirement = requirement


    def __validate_salary(self, salary):
        return salary if salary is not None else 0


    @classmethod
    def cast_to_object(cls, vacancy_dict: dict) -> "Vacancy":
        """Convert a dictionary into a Vacancy object."""

        salary_data = vacancy_dict.get("salary") or {}
        snippet = vacancy_dict.get("snippet") or {}

        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")
        currency = salary_data.get("currency")

        currency_rates = {
            "BYR": 25,
            "USD": 83,
            "KZT": 0.15,
            "UZS": 0.0066,
            "KGS": 0.92,
        }

        if currency == "RUR":
            salary = salary_from if salary_to is None else salary_to
        elif currency in currency_rates:
            salary = salary_from if salary_to is None else salary_to
            if salary is not None:
                salary = currency_rates[currency] * salary
        else:
            salary = salary_from if salary_to is None else salary_to

        return cls(
            name=vacancy_dict.get("name"),
            url=vacancy_dict.get("url"),
            salary=salary,
            requirement=snippet.get("requirement"),
        )

    def __lt__(self, other) -> bool:
        """Return True if this vacancy has a lower salary than the other."""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __gt__(self, other) -> bool:
        """Return True if this vacancy has a higher salary than the other."""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def to_json(self) -> dict:
        """Convert the Vacancy object into a dictionary."""
        return {"name": self.name, "url": self.url, "salary": self.salary, "requirements": self.requirement}

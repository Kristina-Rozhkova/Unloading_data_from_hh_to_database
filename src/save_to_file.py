import json
from abc import ABC, abstractmethod


class SaveInFile(ABC):
    """Абстрактный класс для сохранения данных в файл"""

    @abstractmethod
    def write_down(self, information: dict[int, list]) -> None:
        pass

    @abstractmethod
    def read_file(self) -> dict[str, list] | str:
        pass

    @abstractmethod
    def clean_file(self) -> str | None:
        pass


class Json(SaveInFile):
    """Класс для сохранения данных в JSON-файл"""

    file: str

    def __init__(self, file: str = "data/save.json"):
        self.__file = file

    def write_down(self, information: dict[int, list] | list) -> None:
        """Запись вакансий в файл"""
        with open(self.__file, "w", encoding="utf-8") as file:
            json.dump(information, file, ensure_ascii=False, indent=4)

    def read_file(self) -> dict[str, list] | str:
        """Чтение данных файла"""
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return "Файл не найден."

    def clean_file(self) -> str | None:
        """Очистка файла"""
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                reading_data = json.load(f)
            if reading_data == []:
                return "Файл уже очищен."
            elif reading_data:
                self.write_down([])
        except FileNotFoundError:
            return "Файл не найден."


# if __name__ == '__main__':
#     empl_in_json = Json('../data/employers.json')
#     empl_in_json.read_file()
    # empl_in_json.clean_file()
    # empl_in_json.write_down(employer_inf)
    # vac_in_json = Json('../data/vacancies.json')
    # vac_in_json.clean_file()
    # vac_in_json.write_down(vacancy_inf)
    # empl_in_json.write_down(e2)
    # vac_in_json.write_down(v2)

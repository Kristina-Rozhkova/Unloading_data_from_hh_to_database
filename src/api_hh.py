from abc import ABC, abstractmethod

import requests


class Parser(ABC):

    @abstractmethod
    def _connection(self, url: str):
        pass

    @abstractmethod
    def get_vacancies(self) -> list:
        pass


class HeadHunterEmployers(Parser):
    """Класс получения информации о работодателе и его вакансиях"""
    vacancies_list: list = []
    employers_list: list = []
    vacancies_url: str

    def __init__(self, employer_id: int) -> None:
        self.url = f'https://api.hh.ru/employers/{employer_id}'

    def _connection(self, url: str):
        """Метод проверки подключения"""
        response = requests.get(url)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    def __connection(self, url: str):
        return self._connection(url)

    def get_employers(self) -> list:
        """Метод получения информации о работодателе"""
        employer_info = self.__connection(self.url).json()
        self.vacancies_url = employer_info['vacancies_url']
        self.employers_list.append(employer_info)
        return self.employers_list

    def get_vacancies(self) -> list:
        """Метод получения информации о вакансиях работодателя"""
        vacancies_info = self.__connection(self.vacancies_url).json()['items']
        return vacancies_info


#
# if __name__ == '__main__':
#     list_employers = []
#     dict_employers = {}
#     dict_vacancies = {}
#     for _ in range(1):
#         list_employers.append(int(input(f'Введите id {_ + 1}-го работодателя: ')))
#     for employer in list_employers:
#         empl = HeadHunterEmployers(employer)
#         dict_employers[employer] = empl.get_employers()
#         dict_vacancies[employer] = empl.get_vacancies()
#
#     print(dict_employers)
#     # print(dict_vacancies)

import requests
from abc import ABC, abstractmethod


class HeadHunterAPI(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class HHEmployers(HeadHunterAPI):
    """
    Класс для работы с API HeadHunterEmployers
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/employers'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 1, 'area': 113}

    def get_data(self, keyword):
        """
        Возвращает компанию по ключевому слову
        """

        self.__params['text'] = keyword

        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()['items']
            for item in vacancies:
                if item['open_vacancies'] != 0:
                    return item
                continue
            self.__params['page'] += 1


class HHVacancies(HeadHunterAPI):
    """
    Класс для работы с API HeadHunterVacancies
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'area': 113}
        self.vacancies = []

    def get_data(self, company_id):
        """
        Создает и возвращает вакансии в компании, id которой передан в аргументе
        """

        self.__params['employer_id'] = company_id
        while self.__params.get('page') != 10:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.__params['page'] += 1
        return self.vacancies

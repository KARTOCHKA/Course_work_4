import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        """Возвращает результат поиска на сайте"""


class HH(Engine):
    def __init__(self, job_title: str, page=15):
        """Получение вакансий с hh.ru по API"""
        self.job_title = job_title
        self.vacancy_list = []
        for item in range(page):
            self.data = requests.get(f"https://api.hh.ru/vacancies?text={self.job_title}",
                                     params={'page': item, 'per_page': 1}).json()
            self.vacancy_list.append(self.data)

    def get_request(self) -> list:
        """Возвращает список вакансий с hh.ru"""
        return self.vacancy_list


class SuperJob(Engine):
    def __init__(self, job_title: str, page=15):
        """Получение вакансий с superjob по API"""
        self.job_title = job_title
        load_dotenv()
        api_key: str = os.getenv('SUPERJOB_API')  # ключ находится в файле .env
        my_auth_data = {'X-Api-App-Id': api_key}
        self.vacancy_list = []
        for item in range(page):
            self.data = requests.get('https://api.superjob.ru/2.0/vacancies', headers=my_auth_data,
                                     params={'keywords': self.job_title, 'page': item, 'count': 1}).json()
            self.vacancy_list.append(self.data)

    def get_request(self) -> list:
        """Возвращает список вакансий с superjob"""
        return self.vacancy_list

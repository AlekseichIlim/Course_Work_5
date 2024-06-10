import psycopg2
from config import config

params = config()


class DBManager:
    """
    Класс для работы с данными в БД
    """

    def __init__(self, params):

        conn = psycopg2.connect(**params)
        self.conn = conn

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        with self.conn.cursor() as cur:
            cur.execute('SELECT name, count_vacancies FROM company')
            rows = cur.fetchall()
            self.conn.close()
            return rows

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        with self.conn.cursor() as cur:
            cur.execute("""SELECT vacancies.name, company.name, salary, vacancies.url FROM vacancies
                            INNER JOIN company ON vacancies.id_company = company.id""")
            rows = cur.fetchall()
            self.conn.close()
            return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""

        with self.conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary) as AVG_salary FROM vacancies""")
            rows = cur.fetchall()
            self.conn.close()
            return rows

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)""")
            rows = cur.fetchall()
            self.conn.close()
            return rows

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""

        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT * FROM vacancies
                WHERE name LIKE '%{keyword}%'""")
            rows = cur.fetchall()
            self.conn.close()
            return rows

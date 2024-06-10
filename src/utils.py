import psycopg2
from src.hh_api import HHEmployers, HHVacancies


def return_company(names):
    """Создает и возвращает список компаний."""
    employers = []
    for company in names:
        com = HHEmployers()
        employers.append(com.get_data(company))
    return employers


def return_vacancies(companies):
    """Создает и возвращает список вакансий компании."""

    vacancies = []
    for item in companies:
        vac = HHVacancies()
        for i in (vac.get_data(item['id'])):
            vacancies.append(i)
    return vacancies


def create_tables(params: dict):
    """Создание таблиц для хранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(**params)
    conn.autocommit = True

    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS company')
        cur.execute("""CREATE TABLE company
                    (id int PRIMARY KEY,
                    name varchar(100) NOT NULL,
                    url varchar(100) NOT NULL,
                    count_vacancies int)""")

        cur.execute('DROP TABLE IF EXISTS vacancies')
        cur.execute("""CREATE TABLE vacancies
                    (id int NOT NULL,
                    name varchar(200) NOT NULL,
                    salary int DEFAULT 0,
                    url varchar(100) NOT NULL,
                    id_company int NOT NULL)""")

    conn.commit()
    conn.close()


def save_data_company(data_company, params: dict):

    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        for item in data_company:
            cur.execute(
                """INSERT INTO company 
                VALUES (%s, %s, %s, %s)""",
                (item['id'], item['name'], item['url'], item['open_vacancies']))

    conn.commit()
    conn.close()


def save_data_vacancies(data_vacancies, params: dict):
    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:

        for item in data_vacancies:
            if item['salary'] is not None:
                if item['salary']['from'] is None:
                    salary = item['salary']['to']
                elif item['salary']['to'] is None:
                    salary = 0
                else:
                    salary = item['salary']['from']
            else:
                salary = 0

            cur.execute(
                """INSERT INTO vacancies 
                VALUES (%s, %s, %s, %s, %s)""",
                (item['id'], item['name'], salary, item['url'], item['employer']['id']))

        cur.execute('SELECT name, salary FROM vacancies')

    conn.commit()
    conn.close()

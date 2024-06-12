from config import config, names_company
from src.utils import create_tables, return_company, return_vacancies, save_data_company, save_data_vacancies
from src.db_manager import DBManager

import psycopg2
params = config()

create_tables(params)
company_list = return_company(names_company)
vacancies_list = return_vacancies(company_list)

save_data_company(company_list, params)
save_data_vacancies(vacancies_list, params)

try:
    with psycopg2.connect(**params) as conn:
        exemp1 = DBManager()

        a = exemp1.get_companies_and_vacancies_count(conn)
        b = exemp1.get_all_vacancies(conn)
        c = exemp1.get_avg_salary(conn)
        d = exemp1.get_vacancies_with_higher_salary(conn)
        e = exemp1.get_vacancies_with_keyword(conn, 'python')

finally:
    conn.close()

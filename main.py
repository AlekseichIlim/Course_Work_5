from config import config, names_company
from src.utils import create_tables, return_company, return_vacancies, save_data_company, save_data_vacancies
from src.db_manager import DBManager

params = config()

create_tables(params)
company_list = return_company(names_company)
vacancies_list = return_vacancies(company_list)

save_data_company(company_list, params)
save_data_vacancies(vacancies_list, params)

a = DBManager(params)
print(a.get_avg_salary())
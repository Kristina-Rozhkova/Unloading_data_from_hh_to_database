from src.api_hh import HeadHunterEmployers
from src.database import DBManager, Insert, create_database, create_tables
from src.save_to_file import Json


def staging_database() -> str:
    """Подготовка базы данных для ее дальнейшего использования"""
    # Получение информации о работодателях и их вакансиях через api hh.ru
    list_employers = [10997442, 8923296, 10911658, 11599905, 1627290, 11736287, 9183982, 3207989, 5410307, 842621]
    dict_employers = {}
    dict_vacancies = {}
    for employer in list_employers:
        empl = HeadHunterEmployers(employer)
        dict_employers[employer] = empl.get_employers()
        dict_vacancies[employer] = empl.get_vacancies()

    # Запись полученных данных в json-файл
    employers_in_json = Json('data/employers.json')
    employers_in_json.clean_file()
    employers_in_json.write_down(dict_employers)
    vacancies_in_json = Json('data/vacancies.json')
    vacancies_in_json.clean_file()
    vacancies_in_json.write_down(dict_vacancies)

    # Создание базы данных и таблиц, если они не существуют
    create_database()
    create_tables()

    # Заполнение базы данных данными о работодателях и их вакансиях
    insertion_empl = Insert()
    insertion_vac = Insert()
    employers_information = employers_in_json.read_file()
    vacancies_information = vacancies_in_json.read_file()
    if isinstance(employers_information, str):
        print(f'Возникла ошибка: {employers_information}')
    else:
        insertion_empl.insert_employers(employers_information)
    if isinstance(vacancies_information, str):
        print(f'Возникла ошибка: {vacancies_information}')
    else:
        insertion_vac.insert_vacancies(vacancies_information)

    return 'База данных подготовлена'


def get_information() -> str | list[dict] | float:
    """Главная функция"""
    print('''
    Здравствуйте!
    Для Вас подобран список вакансий. Выберите меню номер пункта, чтобы получить определенную информацию:
    1. Получение списка всех компаний и количества вакансий у каждой компании
    2. Получение списка всех вакансий
    3. Получение средней зарплаты по вакансиям
    4. Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
    5. Получение списка вакансий по переданному слову
    ''')
    user_choice = input()

    manager = DBManager()

    if user_choice == '1':
        all_companies = manager.get_companies_and_vacancies_count()
        return all_companies

    elif user_choice == '2':
        all_vacancies = manager.get_all_vacancies()
        return all_vacancies

    elif user_choice == '3':
        avg_salary = manager.get_avg_salary()
        return avg_salary

    elif user_choice == '4':
        vacancies_with_high_salary = manager.get_vacancies_with_higher_salary()
        return vacancies_with_high_salary

    elif user_choice == '5':
        user_keyword = input('Введите должность для поиска вакансий: ')
        vacancies_with_keyword = manager.get_vacancies_with_keyword(user_keyword)
        return vacancies_with_keyword

    else:
        return 'Введен неверный пункт меню. Попробуйте снова'

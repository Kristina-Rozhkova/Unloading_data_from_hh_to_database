from unittest.mock import Mock, patch

from src.database import DBManager, Insert, create_database, create_tables


def test_create_database() -> None:
    """Тестирование создания базы данных"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchone.return_value = None

        create_database()

        mock_cur.execute.call_count = 2

        sql_queries = [call.args[0] for call in mock_cur.execute.call_args_list]
        assert "SELECT 1 FROM pg_database WHERE datname = 'hh_ru';" in sql_queries[0]
        assert "CREATE DATABASE hh_ru" in sql_queries[1]


def test_create_tables() -> None:
    """Тестирование создания таблиц"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchone.side_effect = [(False,), (False,)]

        create_tables()

        mock_cur.execute.call_count = 4

        sql_queries = [call.args[0].strip() for call in mock_cur.execute.call_args_list]
        assert "SELECT EXISTS (SELECT * FROM pg_tables WHERE tablename = 'employers' AND schemaname = 'public');" in \
               sql_queries[0]

        assert "SELECT EXISTS (SELECT * FROM pg_tables WHERE tablename = 'vacancies' AND schemaname = 'public');" in \
               sql_queries[1]

        assert "CREATE TABLE employers" in sql_queries[2]
        assert "name VARCHAR(50)" in sql_queries[2]
        assert "CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)" in sql_queries[2]

        assert "CREATE TABLE vacancies" in sql_queries[3]
        assert "salary_from INT" in sql_queries[3]
        assert "CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id)" in sql_queries[3]
        assert "FOREIGN KEY(employer_id) REFERENCES employers(employer_id)" in sql_queries[3]


def test_insert_into_employers(employer_info: dict[int | str, list]) -> None:
    """Тестирование заполнения таблицы employers"""
    with (patch('psycopg2.connect') as mock_connect):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        insertion = Insert()
        result = insertion.insert_employers(employer_info)

        assert result == 'Таблица заполнена.'

        sql_queries = [call.args[0] for call in mock_cur.execute.call_args_list]

        actual_sql_query = ' '.join(sql_queries[0].split())
        assert "INSERT INTO employers VALUES (561525, 'ABCP', 'company', 'Москва', 'https://hh.ru/employer/561525')" \
               in actual_sql_query


def test_insert_into_vacancies(vacancies_info: dict) -> None:
    """Тестирование заполнения таблицы vacancies"""
    with (patch('psycopg2.connect') as mock_connect):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        insertion = Insert()
        insertion.insert_vacancies(vacancies_info)

        assert mock_cur.execute.call_count == 5

        sql_queries = [call.args[0] for call in mock_cur.execute.call_args_list]

        actual_query = ' '.join(sql_queries[0].split())
        assert "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)" in actual_query

        # проверка параметров первого вызова
        call = mock_cur.execute.call_args_list
        assert call[0].args[1] == (
            115409516, 'Инженер сопровождения it-продукта', 155000, None, 561525, 'https://hh.ru/vacancy/115409516')


def test_dbmanager_get_companies_and_vacancies_count() -> None:
    """Тестирование получения списка всех компаний и количества вакансий у каждой компании"""
    manager = DBManager()
    all_companies_and_vacancies = manager.get_companies_and_vacancies_count()
    assert all_companies_and_vacancies == [{'name': 'Хайталент', 'vacancies_count': 1},
                                           {'name': 'Самоделкина Вероника Сергеевна', 'vacancies_count': 1},
                                           {'name': 'SW Development', 'vacancies_count': 2},
                                           {'name': 'enKod', 'vacancies_count': 6},
                                           {'name': 'ics-it', 'vacancies_count': 7},
                                           {'name': 'Тендерлайв', 'vacancies_count': 7},
                                           {'name': 'ДОМА', 'vacancies_count': 8},
                                           {'name': 'Tech Horizon', 'vacancies_count': 9},
                                           {'name': 'JavaCode', 'vacancies_count': 11},
                                           {'name': 'АИКЦ Эксперт-аудитор', 'vacancies_count': 15}]


def test_dbmanager_get_all_vacancies(all_vacancies_and_companies: list) -> None:
    """Тестирование получения списка всех вакансий"""
    manager = DBManager()
    result = manager.get_all_vacancies()
    assert result == all_vacancies_and_companies


def test_dbmanager_get_avg_salary() -> None:
    """Тестирование получения среднего значения зарплаты"""
    manager = DBManager()
    avg_salary = manager.get_avg_salary()
    assert avg_salary == 73960.0000


def test_dbmanager_get_vacancies_with_higher_salary(higher_salary: list) -> None:
    """Тестирование получения вакансий со значением зарплаты выше среднего"""
    manager = DBManager()
    result = manager.get_vacancies_with_higher_salary()
    assert result == higher_salary


def test_dbmanager_get_vacancies_with_keyword(vacancies_with_keyword: list) -> None:
    """Тестирование получения вакансий по ключевому слову"""
    manager = DBManager()
    result = manager.get_vacancies_with_keyword('разработчик')
    assert result == vacancies_with_keyword

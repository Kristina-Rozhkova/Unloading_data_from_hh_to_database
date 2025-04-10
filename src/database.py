import psycopg2


def create_database() -> None:
    """Создание базы данных"""
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        password="9605"
    )
    conn.autocommit = True

    cur = conn.cursor()

    try:
        # проверка существования базы данных hh_ru
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'hh_ru';")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE hh_ru;")
    finally:
        cur.close()
        conn.close()


def create_tables() -> None:
    """Создание таблиц базы данных"""
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        password="9605",
        dbname="hh_ru"
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        # проверка существования таблиц employers и vacancies в базе данных
        cur.execute('''
        SELECT EXISTS (SELECT * FROM pg_tables WHERE tablename = 'employers' AND schemaname = 'public');
        ''')
        employers_exists = cur.fetchone()[0]
        cur.execute('''
                SELECT EXISTS (SELECT * FROM pg_tables WHERE tablename = 'vacancies' AND schemaname = 'public');
                ''')
        vacancies_exists = cur.fetchone()[0]

        # создание таблиц, если они не существуют
        if not employers_exists:
            cur.execute('''CREATE TABLE employers(
                        employer_id INT,
                        name VARCHAR(50),
                        type VARCHAR(50),
                        city VARCHAR(50),
                        employer_url VARCHAR(50),

                        CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
                        );''')

        if not vacancies_exists:
            cur.execute('''CREATE TABLE vacancies(
                                vacancy_id INT,
                                name VARCHAR,
                                salary_from INT,
                                salary_to INT,
                                employer_id INT,
                                vacancy_url VARCHAR(50),

                                CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
                                FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
                                );''')
    finally:
        cur.close()
        conn.close()


class Insert:
    """Заполнение таблиц базы данных"""
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host='localhost',
            user="postgres",
            port="5432",
            password="9605",
            dbname="hh_ru"
        )

    def _connect(self) -> None:
        """Подключение объектов для выполнения запросов"""
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def _close_connection(self) -> None:
        """Закрытие подключения к базе данных"""
        self.cur.close()
        self.conn.close()

    def insert_employers(self, information: dict[int | str, list]) -> str:
        """Заполнение таблицы employers"""
        try:
            self._connect()
            for value in information.values():
                for employer in value:
                    employer_id = employer['id']
                    name = employer['name']
                    organization_type = employer['type']
                    city = employer['area']['name']
                    employer_url = employer['alternate_url']

                    self.cur.execute(f'''
                        INSERT INTO employers
                        VALUES ({employer_id}, '{name}', '{organization_type}', '{city}', '{employer_url}')
                    ''')
        finally:
            self._close_connection()
            return 'Таблица заполнена.'

    def insert_vacancies(self, information: dict[str, list]) -> None:
        """Заполнение таблицы vacancies"""
        try:
            self._connect()
            for value in information.values():
                for vacancy in value:
                    try:
                        vacancy_id = int(vacancy['id'])
                        name = vacancy['name']
                        salary = vacancy.get('salary')
                        salary_from = salary.get('from') if salary else None
                        salary_to = salary.get('to') if salary else None
                        employer_id = int(vacancy['employer']['id'])
                        vacancy_url = vacancy['alternate_url']

                        self.cur.execute('''
                            INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)
                            ''', (vacancy_id, name, salary_from, salary_to, employer_id, vacancy_url))
                    except Exception as e:
                        print(f"Ошибка при обработке вакансии {vacancy.get('id')}: {e}")
        finally:
            self._close_connection()


class DBManager:
    """Класс для работы с базой данных"""
    answer_for_query: list = []

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            port="5432",
            password="9605",
            dbname='hh_ru'
        )

    def _connect(self) -> None:
        """Подключение объектов для выполнения запросов"""
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def _close_connection(self) -> None:
        """Закрытие подключения к базе данных"""
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> list:
        """Получение списка всех компаний и количества вакансий у каждой компании"""
        self.answer_for_query = []
        self._connect()
        try:
            self.cur.execute('''
                SELECT employers.name, COUNT(vacancies.vacancy_id) AS vacancies_count
                FROM employers
                JOIN vacancies USING(employer_id)
                GROUP BY employers.name
                ORDER BY vacancies_count;
                ''')
            self._get_answer()
        finally:
            self._close_connection()
            return self.answer_for_query

    def get_all_vacancies(self) -> list:
        """Получение списка всех вакансий"""
        self.answer_for_query = []
        self._connect()
        try:
            self.cur.execute('SELECT * FROM vacancies;')
            self._get_answer()
        finally:
            self._close_connection()
            return self.answer_for_query

    def get_avg_salary(self) -> float:
        """Получение средней зарплаты по вакансиям"""
        self.answer_for_query = []
        self._connect()
        try:
            self.cur.execute('SELECT AVG(salary_from) FROM vacancies;')
            self._get_answer()
        finally:
            self._close_connection()
            avg = self.answer_for_query[0]['avg']
            return round(avg, 4)

    def get_vacancies_with_higher_salary(self) -> list:
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.answer_for_query = []
        self._connect()
        try:
            self.cur.execute('''
                SELECT * FROM vacancies
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies);
            ''')
            self._get_answer()
        finally:
            self._close_connection()
            return self.answer_for_query

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Получение списка вакансий по переданному слову"""
        self.answer_for_query = []
        self._connect()
        try:
            self.cur.execute(f'''
                SELECT * FROM vacancies
                WHERE name LIKE '%{keyword.lower()}%' OR name LIKE '%{keyword.title()}%';
            ''')
            self._get_answer()
        finally:
            self._close_connection()
            return self.answer_for_query

    def _get_answer(self) -> None:
        """Подготовка ответа на запрос"""
        # получение названий столбцов
        columns = [column[0] for column in self.cur.description]

        for row in self.cur.fetchall():
            vacancy = dict(zip(columns, row))
            self.answer_for_query.append(vacancy)


# if __name__ == '__main__':
    # create_database()
    # create_tables()
    # insertion = Insert()
    #
    # read_file_v = Json('../data/test.json')
    # vacancy_inf = read_file_v.read_file()
    # # print(vacancy_inf)
    # read_file_e = Json('../data/employers.json')
    # employer_inf = read_file_e.read_file()
    # # insertion.insert_employers(employer_inf)
    # insertion.insert_vacancies(vacancy_inf)

    # manager = DBManager()
    # all_vac = manager.get_vacancies_with_keyword('разработчик')
    # print(all_vac)

    # save_vacancy = Json('../data/all_vacancies.json')
    # save_vacancy.write_down(manager.get_all_vacancies())
    # save_vacancy.read_file()

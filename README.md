# Unloading_data_from_hh_to_database

***Всем привет! Меня зовут Кристина Рожкова. Я учусь в online школе [sky.pro](https://sky.pro/#giftpopup) на phyton-разработчика. Данный проект является выполнением курсового задания.

**Задание:** В рамках проекта необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

## Установка

1. Клонирование репозитория по [HTTPS](https://github.com/Kristina-Rozhkova/Integration_with_external_service.git)
2. Все зависимости описаны в файле pyproject.toml, все исключения добавлены в .gitignore

---

## Использование

**Пакет src содержит следующие модули:**

1. [api_hh.py](src/api_hh.py)
2. [save_to_file.py](src/save_to_file.py)
3. [database.py](src/database.py)
4. [main.py](src/main.py)

**Пакет data будет содержать следующие файлы:**

- employers.json - для сохранения данных о работодателе. 

- vacancies.json - для сохранения данных о вакансиях работодателей.

**Пакет tests содержит следующие файлы:**
- [conftest.py](tests/conftest.py)
- [test_api_hh.py](tests/test_api_hh.py)
- [test_database.py](tests/test_database.py)
- [test_save_to_file.py](tests/test_save_to_file.py)

---

## Содержание модулей пакета src

1. [api_hh.py](src/api_hh.py)
   
    - `Parser` - *Абстрактный класс, содержащий абстрактные методы подключения к api и получения вакансий*

    - `HeadHunterEmployers` - *Класс для получения информации о вакансиях с помощью API hh.ru*
        
        Методы класса:
        1) Инициализация: каждый новый экземпляр класса содержит в себе минимальные необходимые данные для последующей отправки запроса на сайт
        2) _connection - Получение данных с сайта
        3) __connection - Приватный метод, который вызывает защищенный метод _connection
        4) get_employers - Возвращает полученный список работодателей
        5) get_vacancies - Возвращает полученный список вакансий в формате json, используя при этом ссылку на все текущие вакансии организации, которая содержится в информации о работодателе


2. [save_to_file.py](src/save_to_file.py)

    Модуль содержит абстрактный класс для сохранения данных в файл и Класс для сохранения данных в JSON-файл.

    - `Инициализация` - *создает экземпляр класса с путем к файлу*
    - `write_down` - *Добавление вакансий в файл*
    - `read_file` - *Чтение данных файла*
    - `clean_file` - *Очистка файла*


3. [database.py](src/database.py)

    Модуль содержит функции и классы для работы с базой данных.

    - `create_database` - *Создание базы данных hh_ru*
    - `create_tables` - *Создание таблиц базы данных: employers и vacancies*
    - `Insert` - *Класс осуществляет заполнение таблиц базы данных*
      - `Инициализация`: подготовка данных для подключения к базе данных
      - `_connect`: подключение объектов для выполнения запросов
      - `_close_connection`: Закрытие подключения к базе данных
      - `insert_employers`: Заполнение таблицы employers
      - `insert_vacancies`: Заполнение таблицы vacancies
    - `DBManager` - *Класс для работы с базой данных*
      - `Инициализация`: подготовка данных для подключения к базе данных
      - `_connect`: подключение объектов для выполнения запросов
      - `_close_connection`: Закрытие подключения к базе данных
      - `_get_answer`: Подготовка ответа на запрос
      - `get_companies_and_vacancies_count`: Получение списка всех компаний и количества вакансий у каждой компании
      - `get_all_vacancies`: Получение списка всех вакансий
      - `get_avg_salary`: Получение средней зарплаты по вакансиям
      - `get_vacancies_with_higher_salary`: Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
      - `get_vacancies_with_keyword`: Получение списка вакансий по переданному слову

4. [main.py](src/main.py) 

    Модуль содержит функцию взаимодействия с пользователем - get_information, а также функцию для создания базы данных - staging_database.
---

## Содержание модулей пакета tests

1. [conftest.py](tests/conftest.py)

   - `head_hunter_vacancies_data` - данные, получаемые с помощью api, для последующего мокирования тестов
   - `vacancy_information` - данные о вакансиях для записи в файл
   - `employer_info` - данные о работодателе
   - `vacancies_info` - данные о вакансиях работодателя
   - `all_vacancies_and_companies` - данные, получаемые с помощью метода *get_all_vacancies*
   - `higher_salary` - данные о вакансиях выше средней цены по текцщей выборке
   - `vacancies_with_keyword` - данные о вакансиях, содержащие в названии должности слово "разработчик"

2. [test_api_hh.py](tests/test_api_hh.py)

    - `test_get_vacancies` - Тестирование успешного получения вакансий
    - `test_status_code_error` - Тестирование безуспешного подключения

3. [test_database.py](tests/test_database.py)

    - `test_create_database` - Тестирование создания базы данных
    - `test_create_tables` - Тестирование создания таблиц
    - `test_insert_into_employers` - Тестирование заполнения таблицы employers
    - `test_insert_into_vacancies` - Тестирование заполнения таблицы vacancies
    - `test_dbmanager_get_companies_and_vacancies_count` - Тестирование получения списка всех компаний и количества вакансий у каждой компании
    - `test_dbmanager_get_all_vacancies` - Тестирование получения списка всех вакансий
    - `test_dbmanager_get_avg_salary` - Тестирование получения среднего значения зарплаты
    - `test_dbmanager_get_vacancies_with_higher_salary` - Тестирование получения вакансий со значением зарплаты выше среднего
    - `test_dbmanager_get_vacancies_with_keyword` - Тестирование получения вакансий по ключевому слову

4. [test_save_to_file.py](tests/test_save_to_file.py)

    - `test_json_write_down` - Тестирование добавления данных
    - `test_json_read_file` - Тестирование чтения информации из файла
    - `test_json_read_file_error` - Тестирование выброса ошибки FileNotFoundError при попытке прочитать файл
    - `test_json_clean_file` - Тестирование очистки файла
    - `test_json_clean_file_error` - Тестирование выброса ошибки FileNotFoundError при попытке очистить файл
    - `test_json_clean_file_already_cleaned` - Тестирование повторной попытки очистить файл

---

import json

from src.save_to_file import Json


def test_json_write_down(vacancy_information: list[dict[str, str | int]]) -> None:
    """Тестирование добавления данных"""
    path_to_file = 'test.json'

    data = Json(path_to_file)
    data.write_down(vacancy_information)

    with open(path_to_file, 'r', encoding='utf-8') as test_file:
        result = json.load(test_file)

    assert result == vacancy_information


def test_json_read_file(vacancy_information: list[dict[str, str | int]]) -> None:
    """Тестирование чтения информации из файла"""
    path_to_file = 'test.json'

    data = Json(path_to_file)
    result = data.read_file()

    assert result == vacancy_information


def test_json_read_file_error() -> None:
    """Тестирование выброса ошибки FileNotFoundError при попытке прочитать файл"""
    path_to_file = 'fake_file.json'

    data = Json(path_to_file)
    result = data.read_file()

    assert result == 'Файл не найден.'


def test_json_clean_file(vacancy_information: list[dict[str, str | int]]) -> None:
    """Тестирование очистки файла"""
    path_to_file = 'test.json'

    data = Json(path_to_file)
    # проверяем, что перед очисткой файл содержал данные
    data.write_down(vacancy_information)
    with open(path_to_file, 'r', encoding='utf-8') as file:
        reading_data = json.load(file)
    assert reading_data == vacancy_information

    # теперь очищаем файл
    data.clean_file()

    with open(path_to_file, 'r', encoding='utf-8') as clear_file:
        clean_data = json.load(clear_file)
    assert clean_data == []


def test_json_clean_file_error() -> None:
    """Тестирование выброса ошибки FileNotFoundError при попытке очистить файл"""
    path_to_file = 'fake_file.json'

    file_init = Json(path_to_file)

    result = file_init.clean_file()

    assert result == "Файл не найден."


def test_json_clean_file_already_cleaned(vacancy_information: list[dict[str, str | int]]) -> None:
    """Тестирование повторной попытки очистить файл"""
    path_to_file = 'test.json'

    json_data = Json(path_to_file)
    # заранее заполняем, а потом очищаем файл
    json_data.write_down(vacancy_information)
    with open(path_to_file, 'r', encoding='utf-8') as file:
        reading_data = json.load(file)
    assert reading_data == vacancy_information

    json_data.clean_file()
    with open(path_to_file, 'r', encoding='utf-8') as file:
        reading_data = json.load(file)
    assert reading_data == []

    result = json_data.clean_file()
    assert result == "Файл уже очищен."

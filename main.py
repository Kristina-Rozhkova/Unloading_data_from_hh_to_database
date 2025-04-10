from src.main import get_information, staging_database


def main() -> str | list[dict] | float:
    """Вызов главной функции"""
    return get_information()


if __name__ == '__main__':
    # staging_database()
    print(main())

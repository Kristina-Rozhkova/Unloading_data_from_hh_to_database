from unittest.mock import Mock, patch
import pytest
from requests.exceptions import HTTPError

from src.api_hh import HeadHunterEmployers


def test_get_vacancies(head_hunter_vacancies_data: dict) -> None:
    """Тестирование успешного получения вакансий"""
    mock_employer = {'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=6'}
    with patch('requests.get') as mock_get:
        mock_response_employer = Mock()
        mock_response_employer.status_code = 200
        mock_response_employer.json.return_value = mock_employer

        mock_response_vacancies = Mock()
        mock_response_vacancies.status_code = 200
        mock_response_vacancies.json.return_value = {'items': head_hunter_vacancies_data}

        mock_get.side_effect = [mock_response_employer, mock_response_vacancies]

        parser = HeadHunterEmployers(6)
        employers = parser.get_employers()
        assert len(employers) == 1

        result = parser.get_vacancies()
        assert len(result) == len(head_hunter_vacancies_data)

        assert mock_get.call_count == 2
        mock_get.assert_any_call('https://api.hh.ru/vacancies?employer_id=6')
        mock_get.assert_any_call(mock_employer['vacancies_url'])


def test_status_code_error() -> None:
    """Тестирование безуспешного подключения"""
    with patch('requests.get') as mock_get:
        mock_response_employer = Mock()
        mock_response_employer.status_code = 404
        mock_response_employer.raise_for_status.side_effect = HTTPError("Employer not found")
        mock_get.return_value = mock_response_employer

        parser = HeadHunterEmployers(00)

        with pytest.raises(HTTPError, match='Employer not found'):
            parser.get_employers()

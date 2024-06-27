import json
from datetime import datetime

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.mark.parametrize(
    "category, date, expected_result",
    [
        (
            "Еда",
            None,
            [
                {"Категория": "Еда", "Сумма": 700},
                {"Категория": "Еда", "Сумма": 500},
                {"Категория": "Еда", "Сумма": 1000},
            ],
        ),
        (
            "Еда",
            "2024.06.15",
            [
                {"Категория": "Еда", "Сумма": 700},
                {"Категория": "Еда", "Сумма": 500},
                {"Категория": "Еда", "Сумма": 1000},
            ],
        ),
    ],
)
def test_spending_by_category(category: str, date: str, expected_result: list) -> None:
    data = {
        "Дата операции": [
            "01.06.2024 12:00:00",
            "15.05.2024 08:30:00",
            "10.05.2024 15:45:00",
            "25.04.2024 18:20:00",
            "15.04.2024 09:10:00",
        ],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда", "Транспорт"],
        "Сумма": [1000, 500, 300, 700, 400],
    }
    transactions = pd.DataFrame(data)
    result = spending_by_category(transactions, category, date)
    assert result == expected_result


def test_spending_by_weekday() -> None:
    data = {
        "Дата операции": [
            "01.06.2024 12:00:00",
            "02.06.2024 12:00:00",
            "15.05.2024 08:30:00",
            "10.05.2024 15:45:00",
            "25.04.2024 18:20:00",
            "15.04.2024 09:10:00",
            "16.04.2024 09:10:00",
        ],
        "Сумма операции": [1000, 500, 300, 700, 400, 100, 500],
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"].apply(lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").strftime("%A")).unique()
    result_current_date = spending_by_weekday(transactions)
    expected_result_current_date = {
        "Понедельник": 100.0,
        "Вторник": 500.0,
        "Среда": 300.0,
        "Четверг": 400.0,
        "Пятница": 700.0,
        "Суббота": 1000.0,
        "Воскресенье": 500.0,
    }
    assert json.loads(result_current_date) == expected_result_current_date
    result_given_date = spending_by_weekday(transactions, "2024.06.15")
    expected_result_given_date = {
        "Понедельник": 100.0,
        "Вторник": 500.0,
        "Среда": 300.0,
        "Четверг": 400.0,
        "Пятница": 700.0,
        "Суббота": 1000.0,
        "Воскресенье": 500.0,
    }
    assert json.loads(result_given_date) == expected_result_given_date


def test_spending_by_workday() -> None:
    data = {
        "Дата операции": [
            "01.06.2024 12:00:00",
            "02.06.2024 12:00:00",
            "15.05.2024 08:30:00",
            "10.05.2024 15:45:00",
            "25.04.2024 18:20:00",
            "15.04.2024 09:10:00",
            "16.04.2024 09:10:00",
        ],
        "Сумма операции": [1000, 500, 300, 700, 400, 100, 500],
    }
    transactions = pd.DataFrame(data)
    result_current_date = spending_by_workday(transactions)
    expected_result_current_date = {
        "Рабочий": 400.0,  # Средняя сумма операций по рабочим дням
        "Выходной": 750.0,  # Средняя сумма операций по выходным дням
    }
    assert json.loads(result_current_date) == expected_result_current_date

    result_given_date = spending_by_workday(transactions, "2024.06.15")  # без даты
    expected_result_given_date = {
        "Рабочий": 400.0,  # Средняя сумма операций по рабочим дням
        "Выходной": 750.0,  # Средняя сумма операций по выходным дням
    }
    assert json.loads(result_given_date) == expected_result_given_date

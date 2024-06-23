# Курсовая работа
## Описание:
Приложение для анализа транзакций, которые находятся в Excel-файле.
## Установка:
1. Клонируйте репозиторий:
```
git@github.com:Kostiik8/HomeWorkProject.git
```
2. Установите зависимости:
```
pip install poetry
poetry install
poetry add openpyxl
poetry add pandas
poetry add requests
poetry add python-dotenv 
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort
poetry add --group lint flake8 
```
## Тестирование
С помощью линтеров mypy, black, flake8, isort можете проверить код на соответствие PEP8
Пример команды:
```
flake8 module_name
flake8 . (все модули)
```

## Test Coverage
При необходимости можете проверить с помощью команд:
```
poetry add --group dev pytest
pytest --cov 
```

## Логирование
В проекте реализована система логирования с использованием стандартного модуля `logging` из библиотеки Python.

## Модули
```
main - Запускает проект
views - Веб сервис
utils - функции веб сервиса
services - функции сервиса
reports - функции отчётов

```
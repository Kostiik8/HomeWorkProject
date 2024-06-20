import os

import pandas as pd
import json
from datetime import datetime

import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv(os.path.join("..", ".env"))
API_KEY = os.getenv("API_KEY")


def get_currency_rates(base_currency: str, target_currencies: list) -> dict:
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = {currency: data['rates'][currency] for currency in target_currencies}
        return rates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currency rates: {e}")
        return {}


def get_sp500_stocks_prices(stocks: list) -> dict:
    symbols = ",".join(stocks)
    url = f"https://api.marketstack.com/v1/eod/latest?access_key={API_KEY}&symbols={symbols}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices = {quote['symbol']: quote['close'] for quote in data['data']}
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching S&P 500 stocks prices: {e}")
        return {}


def get_greeting(current_time: datetime) -> str:
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_transactions(file_path: str, start_date: datetime, end_date: datetime) -> DataFrame:
    df = pd.read_excel(file_path)
    df['date'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df


def process_transactions(transactions):
    card_info = {}
    transactions_list = []

    for _, row in transactions.iterrows():
        card_number = str(row['Номер карты'])
        amount = row['Сумма операции']
        category = row['Категория']
        description = row['Описание']
        if pd.isna(card_number):
            last_four = "нет номера"
        else:
            last_four = card_number[-4:]

        if last_four not in card_info:
            card_info[last_four] = {'Сумма платежа': 0, 'Кэшбэк': 0}

        card_info[last_four]['Сумма платежа'] += amount

        if card_info[last_four]['Сумма платежа'] > 0:
            card_info[last_four]['Кэшбэк'] = round(card_info[last_four]['Сумма платежа'] // 100, 2)
        else:
            card_info[last_four]['Кэшбэк'] = 0

        transactions_list.append({
            "card_number": last_four,
            "amount": amount,
            "date": row['date'],
            "category": category,
            "description": description
        })

    top_transactions = sorted(transactions_list, key=lambda x: x['amount'], reverse=True)[:5]

    return card_info, top_transactions


def main(input_datetime: str, file_path: str) -> str:
    current_time = datetime.strptime(input_datetime, "%d.%m.%Y %H:%M:%S")
    greeting = get_greeting(current_time)

    start_date = current_time.replace(day=1)
    end_date = current_time

    transactions = read_transactions(file_path, start_date, end_date)
    card_info, top_transactions = process_transactions(transactions)

    currencies = ["USD", "EUR"]
    currency_rates = get_currency_rates("RUB", currencies)

    currency_rates_formatted = {currency: {"currency": currency, "rate": rate} for currency, rate in
                                currency_rates.items()}

    sp500_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]  # Пример некоторых акций
    sp500_prices = get_sp500_stocks_prices(sp500_stocks)

    cards = [
        {
            "last_digits": last_four,
            "total_spent": round(info['Сумма платежа'], 2),
            "cashback": round(info['Кэшбэк'], 2)

        }
        for last_four, info in card_info.items()
    ]

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": [
            {
                "date": transaction['date'].strftime("%Y-%m-%d"),
                "amount": round(transaction['amount'], 2),
                "category": transaction['category'],
                "description": transaction['description']
            }
            for transaction in top_transactions
        ],
        "currency_rates": currency_rates_formatted,
        "stock_prices": sp500_prices
    }

    with open('../user_settings.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    return json.dumps(response, ensure_ascii=False, indent=4)


file_path = "../data/operations.xlsx"
input_datetime = "18.12.2021 00:40:20"
print(main(input_datetime, file_path))

import json
import os
from dotenv import load_dotenv

from src.utils import (
    filter_transactions_by_date,
    get_cards_data,
    read_excel_to_dict_lict,
    get_exchange_rates,
    get_stocks_cost,
    get_top_5_transactions,
    greeting,
)

with open("../user_settings.json", "r") as file:
    user_choice = json.load(file)
load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
input_date_str = "20.03.2020"


def main(input_date, user_settings, api_key_currency, api_key_stocks):
    """Основная функция для генерации JSON-ответа."""
    path = r"../data/operations.xls"
    transactions = read_excel_to_dict_lict(path)
    filtered_transactions = filter_transactions_by_date(transactions, input_date)
    cards_data = get_cards_data(filtered_transactions)
    exchange_rates = get_exchange_rates(user_settings["user_currencies"], api_key_currency)
    stocks_cost = get_stocks_cost(user_settings["user_stocks"], api_key_stocks)
    top_transactions = get_top_5_transactions(filtered_transactions)
    greetings = greeting()
    user_data = {
        "greeting": greetings,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stocks_cost,
    }
    return json.dumps(user_data, ensure_ascii=False, indent=4)
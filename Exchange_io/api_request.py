import requests
from api_priv import api_exchange

url = "https://exchangeratespro.p.rapidapi.com/latest"

headers = {
    "X-RapidAPI-Key": f"{api_exchange()}",
    "X-RapidAPI-Host": "exchangeratespro.p.rapidapi.com"
}


def get_user_request(currency_dt, exchange_to):
    querystring = {"base": f"{currency_dt}", "currencies": f"{exchange_to}"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text

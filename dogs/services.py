
import requests

def convert_currencies(curr, amount):
    # response = requests.get(
    #     "https://api.currencyapi.com/v3/latest?apikey=cur_live_Fb66gE7yx4Ok95zbOsIvAzDhgM713yGWb6lGb8Sn&currencies=RUB,EUR",
    # )
    # if curr == "USD":
    #     return amount / float(response.json()["data"]["RUB"]["value"])
    # elif curr == "EUR":
    #     return float(response.json()["data"]["EUR"]["value"]) * amount / float(response.json()["data"]["RUB"]["value"])
    if curr == "USD":
        return amount / 90
    elif curr == "EUR":
        return amount / 100

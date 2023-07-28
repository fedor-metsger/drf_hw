
import requests

def convert_currencies(curr, amount):

    if curr == "USD":
        return amount / 90
    elif curr == "EUR":
        return amount / 100

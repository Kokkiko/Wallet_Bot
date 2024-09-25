import requests

fiat = ["EUR", "USD"]
url = f"https://api.coingate.com/v2/rates/merchant"

def rub_to_fiat(currency_from, currency_to):
    url2 = f"https://v6.exchangerate-api.com/v6/23e8b4a328229a0fb4ed24d5/latest/RUB"
    response = requests.get(url2)
    data = response.json()
    fiat_exchange_rate = data["conversion_rates"]["USD"]
    if currency_from == "RUB":
        response = requests.get(url)
        data = response.json()
        exchange_rate = float(data[currency_to]["USD"])
        exchange_rate = (1 / exchange_rate) * fiat_exchange_rate
        return exchange_rate
    else:
        response = requests.get(url)
        data = response.json()
        exchange_rate = float(data[currency_from]["USD"])
        exchange_rate = exchange_rate / fiat_exchange_rate
        return exchange_rate

# показ курса одной валюты по отношению к другой
def get_exchange_rate(currency_from, currency_to):
    if currency_from == "RUB" or currency_to == "RUB":
        return rub_to_fiat(currency_from, currency_to)

    if currency_from in fiat:
        response = requests.get(url)
        data = response.json()
        exchange_rate = float(data[currency_to][currency_from])
        exchange_rate = 1 / exchange_rate
        return exchange_rate

    else:
        response = requests.get(url)
        data = response.json()
        exchange_rate = data[currency_from][currency_to]
        return float(exchange_rate)

# показ стоимости n-го количества одной валюты в другой валюте
def exchange_currency(From, to, amount=1):
    exchange_rate = get_exchange_rate(From, to)
    to_amount = amount * exchange_rate
    return to_amount
print(exchange_currency("ETH", "RUB", 1))



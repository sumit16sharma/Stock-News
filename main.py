import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "bead060fa09e495893203243921cfa83"

stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": "JHZZDPMFOCXKTOB5"
}

news_parameters = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME
}

response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]

yesterday_closing_price = float(data_list[0]["4. close"])
day_before_yesterday_closing_price = float(data_list[1]["4. close"])

diff = yesterday_closing_price-day_before_yesterday_closing_price
percentage = (abs(diff)/day_before_yesterday_closing_price)*100

if diff<0:
    symbol="🔻"
    how_much=round(percentage)
else:
    symbol="🔺"
    how_much=round(percentage)

if percentage > 5:
    response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    news_list = news_data["articles"][:3]
    new_description = [item["description"] for item in news_list]
    news_title = [item["title"] for item in news_list]

    account_sid = "ACddf2c84a94953789913539681022b6be"
    auth_token = "b84bf5d6f6cd32236a24f97297f36701"
    client = Client(account_sid, auth_token)

    for i in range(0,len(news_title)):
        message = client.messages \
            .create(
            body=f"\n\nTSLA: {symbol}{how_much}%\n\nHeadline: {news_title[i]}\n\nBrief: {new_description[i]}",
            from_="+19472824893",
            to="+918826159592"
        )

        print(message.status)


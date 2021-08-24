import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"  # Company name to get information about the stocks.
COMPANY_NAME = "Tesla Inc"   # Company name to get the news out it.
AV_API_KEY = os.environ["AV_API_KEY"]
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
NEWSAPI_API_KEY = os.environ["NEWSAPI_API_KEY"]
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": AV_API_KEY
}
parameters_2 = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWSAPI_API_KEY
}
# GETTING THE LAST 2 DAYS OF TESLA STOCK PRICES
request_1 = requests.get(STOCK_ENDPOINT, params=parameters)
request_1.raise_for_status()
data = request_1.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_close = (data_list[0]["4. close"])
before_yesterday_close = (data_list[1]["4. close"])

# GETTING THE DIFFERENCE BETWEEN THE LAST 2 DAYS
diff = abs(float(yesterday_close) - float(before_yesterday_close))
diff_percentage = round((diff * 100) / float(yesterday_close), 2)

if yesterday_close > before_yesterday_close:
    up_down = "🔺"
else:
    up_down = "🔻"
# IF THE DIFFERENCE IS GREATER THAN 5%. SEND A SMS TO THE LAST NEWS ABOUT TESLA.
if diff_percentage > 1:
    request_2 = requests.get(NEWS_ENDPOINT, params=parameters_2)
    request_2.raise_for_status()
    data_2 = request_2.json()
    first_3_news = data_2["articles"][:3]
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in first_3_news]
    for article in formatted_articles:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"{STOCK_NAME}{up_down}{diff_percentage}%\n{article}",
                from_='YOUR TWILIO NUMBER',  #####################################
                to='YOUR PERSONAL NUMBER'  ####################################
            )
        print(message.sid)

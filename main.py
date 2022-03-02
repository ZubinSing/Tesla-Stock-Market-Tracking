import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_KEY = "0a9be1fed35846aa81453b0d855ae208"
STOCKS_KEY = "A9OTH0SJ2229HZW8"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "AC226e4f22254651038f3a8195f818df5e"
TWILIO_TOKEN = "2693b2644f8b6cfd103dda71c4d24098"
TWILIO_NUMBER = "+19032897800"

news_params = {
    "apiKey": NEWS_KEY,
    "qInTitle":"tesla",
}

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCKS_KEY,
}

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#Getting the closing price of Tesla yesterday
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list=[value for key, value in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

#The day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = float(day_before_yesterday_data['4. close'])

#Finding the positive difference between 1 and 2
difference = yesterday_closing_price - day_before_yesterday_data_closing_price

#Percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference/yesterday_closing_price) * 100)
print(diff_percent)

#If percentage is greater than 5 then get the news.
if abs(diff_percent)>3:
    print(news_response.json())
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    # A new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"Headline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    # Sending each article as a separate message via Twilio.

    for every_article in formatted_articles:
        message = client.messages \
            .create(
            body=every_article,
            from_=TWILIO_NUMBER,
            to='+919667008279'
        )






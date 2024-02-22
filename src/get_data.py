import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup


def get_news():
    url = "https://seeking-alpha.p.rapidapi.com/news/v2/list-by-symbol"
    headers = {
        "X-RapidAPI-Key": "70f39bfb51mshbcc1159f7ffb2ddp144fe1jsnc494bbf0cefb",
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }
    total_items_needed = 400
    items_per_request = 40
    all_news = []

    # Loop through multiple requests to fetch a total of 400 items
    for number in range(1, total_items_needed // items_per_request + 1):
        querystring = {"id": "TSLA", "size": str(items_per_request), "number": str(number)}
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            all_news.extend(data['data']) 
        else:
            print(f"Error: {response.status_code}")
            break  # Or continue based on how we want to handle errors

        # Handling rate limits, just in case
        time.sleep(1)  # Sleep for 1 second between requests

    return all_news


def get_stock_timeseries():
    url = "https://real-time-finance-data.p.rapidapi.com/stock-time-series"

    querystring = {"symbol":"TSLA","period":"1Y","language":"en"}

    headers = {
        "X-RapidAPI-Key": "70f39bfb51mshbcc1159f7ffb2ddp144fe1jsnc494bbf0cefb",
        "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data

def get_TSLA_info():
    # URL
    url = 'https://en.wikipedia.org/wiki/Tesla,_Inc.#Finances'

    # Send a request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    res = []
    # Replace 'wikitable' with the actual class name of your table
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('th')
        if len(cols) == 6:
            res.append([cols[0].get_text(strip = True),cols[1].get_text(strip = True),cols[2].get_text(strip = True)
                    ,cols[3].get_text(strip = True),cols[4].get_text(strip = True)])

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 6:
            res.append([cols[0].get_text(strip = True),cols[1].get_text(strip = True),cols[2].get_text(strip = True)
                    ,cols[3].get_text(strip = True),cols[4].get_text(strip = True)])
    return res

news_data = get_news()
stock_timeseries = get_stock_timeseries()
TSLA_info = get_TSLA_info()

# Specify the file path for news_data and save it as JSON
news_data_file_path = '../data/raw/raw_news_data.json'
with open(news_data_file_path, "w") as news_data_file:
    json.dump(news_data, news_data_file, indent=4) 


# Specify the file path for stock_timeseries and save it as JSON
stock_timeseries_file_path = '../data/raw/raw_stock_timeseries.json'
with open(stock_timeseries_file_path, "w") as stock_timeseries_file:
    json.dump(stock_timeseries, stock_timeseries_file, indent=4)  

# Specify the file path for TSLA_info and save it as CSV
df = pd.DataFrame(TSLA_info)
TSLA_file_path = '../data/raw/TSLA_wiki.csv'
df.to_csv(TSLA_file_path, index=False)

print('-----------------------------------------------------------------Data Acquired-----------------------------------------------------------------')



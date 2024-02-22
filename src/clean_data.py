import pandas as pd
import numpy as np
import json

news_data_file_path = '../data/raw/raw_news_data.json'
stock_timeseries_file_path = '../data/raw/raw_stock_timeseries.json'
TSLA_file_path = '../data/raw/TSLA_wiki.csv'

# Read the JSON file for news_data
with open(news_data_file_path, "r") as news_data_file:
    raw_news_data = json.load(news_data_file)

# Read the JSON file for stock_timeseries
with open(stock_timeseries_file_path, "r") as stock_timeseries_file:
    raw_stock_data = json.load(stock_timeseries_file)

# Read the CSV file for TSLA info
TSLA_info = pd.read_csv(TSLA_file_path)


processed_news_data = []
for item in raw_news_data:
    processed_item = {
        'id': item['id'],
        'title': item['attributes']['title'],
        'date_time': item['attributes']['publishOn'],
    }
    processed_news_data.append(processed_item)

news_data = pd.DataFrame(processed_news_data)

processed_stock_data = []
for key, value in raw_stock_data['data']['time_series'].items():
    processed_item = {
        'date_time': key,
        'price': value['price'],
        'volume': value.get('volume', None),
    }
    processed_stock_data.append(processed_item)

stock_data = pd.DataFrame(processed_stock_data)


# Convert 'date_time' to datetime
stock_data['date_time'] = pd.to_datetime(stock_data['date_time'])
# Sort the dataframe by date
stock_data.sort_values('date_time', inplace=True)

# Align the format for date and time
news_data['date_time'] = pd.to_datetime(news_data['date_time'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce')
news_data['date_time'] = pd.to_datetime(news_data['date_time'], format='%Y-%m-%d %H:%M:%S%z', errors='coerce')

# Extract date and time as new columns
news_data['Date'] = news_data['date_time'].dt.date
news_data['Time'] = news_data['date_time'].dt.time

# Drop duplicates based on 'title'
news_data = news_data.drop_duplicates(subset='title')

# Clean TSLA info extracted from wiki
columns = TSLA_info.iloc[0]
TSLA_info.columns = columns
TSLA_info.drop([0,1,20,21], inplace=True)
TSLA_info.replace("0", np.nan, inplace=True)
TSLA_info.dropna(inplace=True)
TSLA_info.reset_index(drop=True, inplace=True)
for column in TSLA_info.columns:
    if TSLA_info[column].dtype == 'object':
        TSLA_info[column] = TSLA_info[column].str.replace(',', '')
        TSLA_info[column] = TSLA_info[column].str.replace('−', '-')
        TSLA_info[column] = pd.to_numeric(TSLA_info[column], errors='coerce')

# Save processed data as CSV files in the proper directions
news_data_file_path = '../data/processed/processed_news_data.csv'
stock_timeseries_file_path = '../data/processed/processed_stock_timeseries.csv'
TSLA_info_path = '../data/processed/processed_TSLA_info.csv'

news_data.to_csv(news_data_file_path, index=False)
stock_data.to_csv(stock_timeseries_file_path, index=False)
TSLA_info.to_csv(TSLA_info_path, index=False)
print('-----------------------------------------------------------------Data Cleaning Done-----------------------------------------------------------------')
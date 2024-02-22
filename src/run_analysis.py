import pandas as pd
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import grangercausalitytests

# Import data
news_data = pd.read_csv('../data/processed/processed_news_data.csv')
stock_data = pd.read_csv('../data/processed/processed_stock_timeseries.csv')


# Analysis PART1: Sentiment Analysis
# NLTK VADER for sentiment analysis
# New words and values
new_words = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}
# Instantiate the sentiment intensity analyzer with the existing lexicon
vader = SentimentIntensityAnalyzer()
# Update the lexicon
vader.lexicon.update(new_words)

# Iterate through the headlines and get the polarity scores
scores = [vader.polarity_scores(headline) for headline in news_data.title]
# Convert the list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)
# Join the DataFrames
scored_news = news_data.join(scores_df)

# Analysis PART2: Statistical Analysis - Granger Causality Test
# Preprocess and align your datasets
# Group by date from scored_news and calculate the mean
mean_c = scored_news.loc[:, ['compound','Date']].groupby('Date').mean()
# Get the cross-section of compound in the 'columns' axis
mean_c = mean_c.xs('compound', axis=1)
score_by_date = pd.DataFrame(mean_c)
score_by_date.index = pd.to_datetime(score_by_date.index)
# Parameters for filtering in a date range
start_date = '2023-11-06'
end_date = score_by_date.index.max()

sentiment_analysis = score_by_date.resample('D').asfreq().fillna(0)
sentiment_analysis['date'] = sentiment_analysis.index

stock_data['date_time'] = pd.to_datetime(stock_data['date_time'])
stock_data['Date'] = stock_data['date_time'].dt.date
stock_data_new = stock_data.drop('date_time', axis=1, inplace=False)
stock_data_new.index = pd.to_datetime(stock_data_new.Date)
stock_data_new = stock_data_new.resample('D').fillna(method='ffill')
stock_data_new['Date'] = stock_data_new.index
filtered_stock_data = stock_data_new[(stock_data_new.index >= start_date) 
                                     & (stock_data_new.index <= end_date)]
filtered_sentiment_analysis = sentiment_analysis[(sentiment_analysis.index >= start_date) 
                                     & (sentiment_analysis.index <= end_date)]

filtered_stock_data['Date'] = pd.to_datetime(filtered_stock_data['Date'])
filtered_sentiment_analysis['date'] = pd.to_datetime(filtered_sentiment_analysis['date'])

merged_df = pd.merge(filtered_sentiment_analysis, filtered_stock_data, left_index=True, right_index=True, how='inner')

# Statistical Analysis: Granger Causality Test
gc_test = grangercausalitytests(merged_df[['price', 'compound']], maxlag=[1])

# Output result data
path1 = '../results/filtered_stock_data.csv'
path2 = '../results/filtered_sentiment_analysis.csv'
path3 = '../results/scored_news.csv'
filtered_stock_data.to_csv(path1, index=False)
filtered_sentiment_analysis.to_csv(path2, index=False)
scored_news.to_csv(path3, index=False)
print('-----------------------------------------------------------------Analysis Finished-----------------------------------------------------------------')
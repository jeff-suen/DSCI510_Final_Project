import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Import data
stock_data = pd.read_csv('../data/processed/processed_stock_timeseries.csv')
filtered_stock_data = pd.read_csv('../results/filtered_stock_data.csv')
filtered_sentiment_analysis = pd.read_csv('../results/filtered_sentiment_analysis.csv')
scored_news = pd.read_csv('../results/scored_news.csv')
df= pd.read_csv('../data/processed/processed_TSLA_info.csv')

#1 Create a line plot - TSLA Stock Price
stock_data['date_time'] = pd.to_datetime(stock_data['date_time'])
stock_data.sort_values('date_time', inplace=True)
plt.figure(figsize=(10, 6))
sns.lineplot(x='date_time', y='price', data=stock_data)
plt.xticks(rotation=30)
plt.grid(True)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.title('TSLA Stock Price Over Time', fontsize=14)
ax = sns.scatterplot(x='date_time', y='price', data = stock_data, color='red', s=30, legend=False)
plt.tight_layout()
plt.show()

#2 Plot Mean Sentiment Scores by Dates
mean_c = scored_news.loc[:, ['compound','Date']].groupby('Date').mean()
mean_c = mean_c.xs('compound', axis=1)
mean_c.plot(kind='bar',
            figsize=(10, 6),
            title = 'Tesla: Mean Compound Sentiment Score by Date')
plt.xlabel('Date')
plt.ylabel('Mean Compound Sentiment Score')
plt.show()

#3 Plot a stacked bar chart: Mean Sentiment Scores by Dates
stacked_plot = scored_news.loc[:, ['neg', 'neu', 'pos', 'Date', 'Time']].groupby(['Date', 'Time']).mean()
stacked_plot.columns = ['negative', 'neutral', 'positive']
stacked_plot.plot(kind = 'bar', 
              stacked = True, 
              figsize = (14, 7), 
              title = "Negative, neutral, and positive sentiment for TSLA", 
              color = ["red","orange", "green"]).legend(bbox_to_anchor=(1.0, 0.5))
plt.xlabel('Date & Time')
plt.ylabel('Sentiment Score')
plt.legend(title='Sentiment', loc='upper right', labels=['Negative', 'Neutral', 'Positive'])
plt.tight_layout()
plt.show()

#4 Dual-axis Plot
# Preprocess
filtered_stock_data['Date'] = pd.to_datetime(filtered_stock_data['Date'])
filtered_sentiment_analysis['date'] = pd.to_datetime(filtered_sentiment_analysis['date'])
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 5))
# Plot the 'price' vs 'date' as a line plot
ax1.set_xlabel('Date')
ax1.set_ylabel('Price', color='tab:blue')
ax1.plot(filtered_stock_data['Date'], filtered_stock_data['price'], color='tab:blue', label='Price')
ax1.tick_params(axis='y', labelcolor='tab:blue')
# Create a second y-axis for 'compound' vs 'date' as scatter points
ax2 = ax1.twinx() 
ax2.set_ylabel('Compound', color='tab:orange')
ax2.scatter(filtered_sentiment_analysis['date'], filtered_sentiment_analysis['compound'], color='tab:orange', label='Compound Sentiment Scores')
ax2.tick_params(axis='y', labelcolor='tab:orange')
# Add labels and legend
plt.title('TSLA: Stock Price vs Compound Sentiment Scores Over a Month')
plt.xlabel('Date')
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()
plt.show()

#5 Combined Graph for TSLA company overall info over years
# Create a combined plot with shared x-axis
fig, ax1 = plt.subplots(figsize=(14, 8))
# Line plot for Revenue and Net Income on the first y-axis
sns.lineplot(data=df, x='Year', y='Revenue(US$ m)', marker='o', label='Revenue(US$ m)', ax=ax1, color='blue')
sns.lineplot(data=df, x='Year', y='Net income(US$ m)', marker='o', label='Net income(US$ m)', ax=ax1, color='green')
# Setting the labels and title for the first y-axis
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Revenue & Net Income (US$ m)', fontsize=14)
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')
# Create a second y-axis for Total Assets with shared x-axis
ax2 = ax1.twinx()
sns.lineplot(data=df, x='Year', y='Total assets(US$ m)', marker='o', label='Total assets(US$ m)', ax=ax2, color='red')
# Setting the labels and title for the second y-axis
ax2.set_ylabel('Total assets(US$ m)', fontsize=14)
ax2.tick_params(axis='y', labelcolor='red')
ax2.legend(loc='upper right')
# Create a bar chart for Employees on the first y-axis with shared x-axis
# Note: We use the bar plot from matplotlib to ensure it shares the same x-axis
ax1.bar(df['Year'], df['Employees'], color='lightgrey', label='Employees', alpha=0.5)
# Additional legend for the bar plot due to different plot type
handles, labels = ax1.get_legend_handles_labels()
labels.append('Employees')
ax1.legend(handles, labels, loc='center left')
# Show the combined plot
plt.title('Company Financial and Employee Data Over Time')
plt.show()

print('-----------------------------------------------------------------Data Visualization Finished-----------------------------------------------------------------')
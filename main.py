import datetime, requests, yfinance as yf
import config
from transformers import pipeline
import streamlit as st 

# Initialize the negative_count variable
negative_count = 0
negative_sum = 0
positive_count = 0
positive_sum = 0


option = st.sidebar.selectbox("Which Dashboard?", ('Home','Twitter Sentiment', 'News Sentiment'),0)

classifier = pipeline('sentiment-analysis')



if option == 'Home':
  st.title('home')
  st.write('This webpage will help you to tell what the current sentiment of a given ticker is. The closer the number is to 1 the more positive or negative the sentiment is.')
  st.write('Thank you for visiting and good luck investing')

if option == 'News Sentiment':

  symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)
  ticker = yf.Ticker(symbol)
  news = ticker.news

  positive_count = 0
  negative_count = 0
  positive_sum = 0
  negative_sum = 0

  for item in news:
      title = item['title']
      result = classifier(title)
      label = result[0]['label']
      score = result[0]['score']
      
      if label == 'POSITIVE':
          positive_count += 1
          positive_sum += score
      elif label == 'NEGATIVE':
          negative_count += 1
          negative_sum += score

  positive_average = positive_sum / positive_count if positive_count > 0 else 0
  negative_average = negative_sum / negative_count if negative_count > 0 else 0

  # Display the metrics at the top of the screen
  st.write("Positive Count:", positive_count)
  st.write("Negative Count:", negative_count)
  st.write("Positive Average:", positive_average)
  st.write("Negative Average:", negative_average)

  for item in news:
    st.write(item['title'])



if option == 'Twitter Sentiment':

  symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)

  r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

  data = r.json()

  # Initialize the variables for counting and averaging
  positive_count = 0
  positive_sum = 0
  negative_count = 0
  negative_sum = 0

  for message in data['messages']:
      result = classifier(message['body'])
      label = result[0]['label']
      score = result[0]['score']

      if label == 'POSITIVE':
          positive_count += 1
          positive_sum += score
      elif label == 'NEGATIVE':
          negative_count += 1
          negative_sum += score

  # Calculate the averages
  positive_average = positive_sum / positive_count if positive_count > 0 else 0
  negative_average = negative_sum / negative_count if negative_count > 0 else 0

  # Display the metrics at the top of the screen
  st.write("Positive Count:", positive_count)
  st.write("Negative Count:", negative_count)
  st.write("Positive Average:", positive_average)
  st.write("Negative Average:", negative_average)

  # Display the tweets
  for message in data['messages']:
      st.image(message['user']['avatar_url'])
      st.write(message['user']['username'])
      st.write(message['created_at'])
      st.write(message['body'])
      result = classifier(message['body'])
      label = result[0]['label']
      score = result[0]['score']

from api_clients import newsapi, co

def fetch_news(ticker):
    """Fetch news articles."""
    try:
        articles = newsapi.get_everything(
            q=ticker,
            language="en",
            sort_by="relevancy",
            page_size=5
        )
        return [(article["title"], article["description"]) 
                for article in articles["articles"]
                if article["title"] and article["description"]]
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []

def analyze_sentiment(news_articles):
    """Analyze sentiment of news articles using Cohere."""
    sentiments = []
    for title, summary in news_articles:
        try:
            prompt = f"Analyze the sentiment of this financial news:\nHeadline: {title}\nSummary: {summary}\nRespond with exactly one word - either 'positive', 'neutral', or 'negative':"
            response = co.generate(
                model="command",
                prompt=prompt,
                max_tokens=5,
                temperature=0.3,
                stop_sequences=["\n", "."],
            )
            
            sentiment = (
                response.generations[0].text
                .lower()
                .replace('.', '')
                .replace('\n', '')
                .strip()
            )
            
            valid_sentiments = {'positive', 'neutral', 'negative'}
            if sentiment not in valid_sentiments:
                print(f"Invalid sentiment received: '{sentiment}', defaulting to neutral")
                sentiment = 'neutral'
            sentiments.append(sentiment)
            
        except Exception as e:
            print(f"Error in sentiment analysis for news: {title[:50]}... Error: {str(e)}")
            sentiments.append('neutral')
    
    if not sentiments:
        print("No sentiments could be analyzed, returning balanced default")
        return ['neutral'] * len(news_articles)
    
    return sentiments
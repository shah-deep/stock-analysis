from newsapi import NewsApiClient
import cohere
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigError(Exception):
    pass

def get_required_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ConfigError(f"Missing required environment variable: {var_name}")
    return value

def initialize_apis():
    try:
        news_api_key = get_required_env_var("NEWS_API_KEY")
        cohere_api_key = get_required_env_var("COHERE_API_KEY")
        
        return (
            NewsApiClient(api_key=news_api_key),
            cohere.Client(api_key=cohere_api_key)
        )
    except ConfigError as e:
        print(f"Configuration error: {e}")
        raise


newsapi, co = initialize_apis()
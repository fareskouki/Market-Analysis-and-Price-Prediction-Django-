# sentiment_analysis.py

from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

AZURE_TEXT_ANALYTICS_KEY = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
AZURE_TEXT_ANALYTICS_ENDPOINT = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')

def authenticate_client():
    """
    Authenticates the Text Analytics client using environment variables.
    """
    if not AZURE_TEXT_ANALYTICS_KEY or not AZURE_TEXT_ANALYTICS_ENDPOINT:
        logger.error("Azure Text Analytics key or endpoint not set in environment variables.")
        raise ValueError("Azure Text Analytics key or endpoint not set.")
    
    credential = AzureKeyCredential(AZURE_TEXT_ANALYTICS_KEY)
    client = TextAnalyticsClient(endpoint=AZURE_TEXT_ANALYTICS_ENDPOINT, credential=credential)
    logger.debug("Azure Text Analytics client authenticated successfully.")
    return client

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text and returns detailed sentiment scores.

    Parameters:
    - text (str): The text to analyze.

    Returns:
    - dict: A dictionary containing sentiment label and confidence scores.
    """
    client = authenticate_client()
    documents = [text]
    try:
        response = client.analyze_sentiment(documents=documents)[0]
        sentiment = response.sentiment  # 'positive', 'neutral', 'negative'
        confidence_scores = response.confidence_scores  # {'positive': 0.0-1.0, 'neutral': 0.0-1.0, 'negative': 0.0-1.0}
        
        # Log the full sentiment response for debugging
        logger.debug(f"Sentiment: {sentiment}")
        logger.debug(f"Confidence Scores: {confidence_scores}")
        
        return {
            'sentiment': sentiment,
            'positive': confidence_scores.positive,
            'neutral': confidence_scores.neutral,
            'negative': confidence_scores.negative
        }
    except Exception as err:
        logger.exception(f"Encountered exception during sentiment analysis: {err}")
        return None

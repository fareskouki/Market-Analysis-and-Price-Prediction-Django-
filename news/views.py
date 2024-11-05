import matplotlib
import os
matplotlib.use('Agg')
from django.shortcuts import render, redirect, get_object_or_404
from .models import News, NewsArticle, InflationData
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from django.core.files.storage import default_storage
from .forms import UploadFileForm, NewsArticleForm,CommentForm
from sklearn.linear_model import LinearRegression
from .sentiment_analysis import analyze_sentiment
import seaborn as sns
import mplcursors
import json
import numpy as np
import logging
from django.conf import settings
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from .forms import PDFUploadForm
import PyPDF2
from .models import News, NewsArticle, Comment

logger = logging.getLogger(__name__)

# List all news articles
def news_list(request):
    articles = NewsArticle.objects.all()
    return render(request, 'news/news_list.html', {'news_items': articles})

# Create a new article
def create_article(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsArticleForm()
    return render(request, 'news/create_article.html', {'form': form})

# Update an article
def update_article(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsArticleForm(instance=article)
    return render(request, 'news/update_article.html', {'form': form})

# Delete an article
def delete_article(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('news_list')
    return render(request, 'news/delete_article.html', {'article': article})

# Add a comment to an article
def add_comment(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article  # Link comment to the article
            comment.save()
            return redirect('news_list')
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form, 'article': article})

def train_model_from_csv(file_path):
    data = pd.read_csv(file_path, skiprows=3)
    tunisia_data = data[data['Country Name'] == 'Tunisia'].loc[:, '1960':'2023'].T
    tunisia_data.columns = ['Inflation Rate']
    tunisia_data.dropna(inplace=True)
    tunisia_data.index = tunisia_data.index.astype(int)
    
    # Prepare data for supervised learning
    tunisia_data['Next Year Inflation Rate'] = tunisia_data['Inflation Rate'].shift(-1)
    tunisia_data.dropna(inplace=True)
    X = tunisia_data[['Inflation Rate']]
    y = tunisia_data['Next Year Inflation Rate']
    
    # Train the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, 'tunisia_inflation_model.pkl')

    # Plotting
    plt.figure(figsize=(14, 9))
    plt.plot(tunisia_data.index, tunisia_data['Inflation Rate'], color='#1f77b4', marker='o', label='Actual Inflation Rate')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return chart_base64

def upload_and_train(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            path = default_storage.save(f'uploads/{csv_file.name}', csv_file)
            chart_base64 = train_model_from_csv(path)
            return render(request, 'news/result.html', {'chart_base64': chart_base64})
    else:
        form = UploadFileForm()
    return render(request, 'news/upload.html', {'form': form})

from .sentiment_analysis import analyze_sentiment


def result_chart_with_forecast(request):
    """
    View to display the forecasted provisioned price based on the latest news sentiment.
    It visualizes historical inflation rates, oil prices, and the provisioned price for the next year.
    """
    base_dir = settings.BASE_DIR
    model_path = os.path.join(base_dir, 'news', 'tunisia_inflation_model.pkl')

    # Load the trained model
    try:
        model = joblib.load(model_path)
        logger.debug(f"Model loaded successfully from {model_path}")
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        return render(request, 'news/error.html', {'message': 'Model not found. Please train the model first.'})
    except Exception as e:
        logger.exception(f"Error loading model: {e}")
        return render(request, 'news/error.html', {'message': 'Error loading the model.'})

    # Get the latest news article's sentiment score
    try:
        latest_article = NewsArticle.objects.latest('date_published')
        sentiment_result = analyze_sentiment(latest_article.content)
        if sentiment_result:
            sentiment_label = sentiment_result['sentiment']
            positive_score = sentiment_result['positive']
            neutral_score = sentiment_result['neutral']
            negative_score = sentiment_result['negative']
        else:
            # Fallback if sentiment_result is None
            sentiment_label = latest_article.sentiment_label
            positive_score = latest_article.positive_score
            neutral_score = latest_article.neutral_score
            negative_score = latest_article.negative_score

        logger.debug(f"Latest sentiment label: {sentiment_label}")
        logger.debug(f"Scores - Positive: {positive_score}, Neutral: {neutral_score}, Negative: {negative_score}")
    except NewsArticle.DoesNotExist:
        logger.error("No news articles found.")
        return render(request, 'news/error.html', {'message': 'No news articles found. Please upload an article first.'})
    except Exception as e:
        logger.exception(f"Error fetching latest article: {e}")
        return render(request, 'news/error.html', {'message': 'Error fetching the latest article.'})

    # Real price of olive oil in USD per liter (example value)
    real_price = 9.59  
    MAX_REDUCTION = 0.5  # 50%

    # Calculate adjustment factor based on sentiment label
    if sentiment_label == 'positive':
        adjustment_factor = -positive_score  # Positive sentiment leads to price decrease
    elif sentiment_label == 'negative':
        adjustment_factor = negative_score  # Negative sentiment leads to price increase
    else:
        adjustment_factor = 0  # Neutral sentiment leads to no change

    # Cap the adjustment factor to prevent excessive reduction
    if adjustment_factor < -MAX_REDUCTION:
        adjustment_factor = -MAX_REDUCTION
        logger.debug(f"Adjustment factor capped to {adjustment_factor} to prevent excessive reduction.")

    logger.debug(f"Adjustment factor: {adjustment_factor}")

    # Calculate provisioned price
    provisioned_price = real_price * (1 + adjustment_factor)
    logger.debug(f"Provisioned price before adjustment: {provisioned_price}")

    # Ensure provisioned price is not negative
    if provisioned_price < 0:
        provisioned_price = 0
        logger.debug("Provisioned price adjusted to 0 to prevent negative value.")

    # Load historical inflation data
    inflation_file_path = os.path.join(base_dir, 'uploads', 'inflation_data.csv')
    if not os.path.exists(inflation_file_path):
        logger.error(f"Inflation data file not found at {inflation_file_path}")
        return render(request, 'news/error.html', {'message': 'Inflation data file not found.'})

    try:
        inflation_data = pd.read_csv(inflation_file_path, skiprows=3)
        tunisia_data = inflation_data[inflation_data['Country Name'] == 'Tunisia'].loc[:, '1960':'2023'].T
        tunisia_data.columns = ['Inflation Rate']
        tunisia_data.index = tunisia_data.index.astype(int)
        tunisia_data = tunisia_data.dropna()
        logger.debug(f"Inflation data loaded successfully with {tunisia_data.shape[0]} records.")
    except Exception as e:
        logger.exception(f"Error processing inflation data: {e}")
        return render(request, 'news/error.html', {'message': 'Error processing inflation data.'})

    # Load historical oil price data
    oil_price_file_path = os.path.join(base_dir, 'uploads', 'oil_prices.csv')
    if not os.path.exists(oil_price_file_path):
        logger.error(f"Oil price data file not found at {oil_price_file_path}")
        return render(request, 'news/error.html', {'message': 'Oil price data file not found.'})

    try:
        oil_price_data = pd.read_csv(oil_price_file_path)
        oil_price_data.set_index('Year', inplace=True)
        oil_price_data = oil_price_data.dropna()
        logger.debug(f"Oil price data loaded successfully with {oil_price_data.shape[0]} records.")
    except Exception as e:
        logger.exception(f"Error processing oil price data: {e}")
        return render(request, 'news/error.html', {'message': 'Error processing oil price data.'})

    # Prepare data for Plotly charts
    inflation_years = tunisia_data.index.tolist()
    inflation_rates = tunisia_data['Inflation Rate'].tolist()

    oil_years = oil_price_data.index.tolist()
    oil_prices = oil_price_data['Price (USD/L)'].tolist()

    # Determine the latest year in the data
    latest_inflation_year = max(inflation_years) if inflation_years else datetime.now().year
    latest_oil_year = max(oil_years) if oil_years else datetime.now().year
    latest_year = max(latest_inflation_year, latest_oil_year)

    # Calculate next year
    next_year = latest_year + 1

    # Add provisioned price as a point for the next year
    provisioned_year = next_year
    provisioned_price_value = provisioned_price

    # Prepare Plotly data
    inflation_data_json = json.dumps({
        'x': inflation_years,
        'y': inflation_rates,
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Inflation Rate'
    })

    oil_data_json = json.dumps({
        'x': oil_years,
        'y': oil_prices,
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Oil Prices'
    })

    provisioned_price_data_json = json.dumps({
        'x': [provisioned_year],
        'y': [provisioned_price_value],
        'type': 'scatter',
        'mode': 'markers',
        'name': 'Provisioned Price',
        'marker': {
            'color': 'red',
            'size': 12,
            'symbol': 'diamond'
        },
        'text': ['Forecasted Price'],
        'hoverinfo': 'text+y'
    })

    context = {
        'inflation_data': inflation_data_json,
        'oil_data': oil_data_json,
        'provisioned_price_data': provisioned_price_data_json,  # Added provisioned price data
        'real_price': round(real_price, 2),
        'provisioned_price': round(provisioned_price, 2),
        'sentiment_label': sentiment_label,
        'sentiment_score': {
            'positive': round(positive_score, 2),
            'neutral': round(neutral_score, 2),
            'negative': round(negative_score, 2)
        },
        'next_year': provisioned_year,  # Pass next year to the template if needed
    }

    logger.debug("Rendering result_with_forecast.html with context.")

    return render(request, 'news/result_with_forecast.html', context)

def upload_and_analyze_news(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            sentiment_score = analyze_sentiment(article.content)
            if sentiment_score is not None:
                article.sentiment_score = sentiment_score
                article.save()
                return redirect('result_chart_with_forecast')
            else:
                # Handle the case where sentiment analysis failed
                return render(request, 'error.html', {'message': 'Sentiment analysis failed. Please try again.'})
    else:
        form = NewsArticleForm()
    return render(request, 'news/upload_news.html', {'form': form})


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
 

def authenticate_azure_client():
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def analyze_economic_content_from_pdf(pdf_file):
    # Read the full text from the PDF
    text_content = extract_text_from_pdf(pdf_file)
    
    # Set up Azure Text Analytics client
    client = authenticate_azure_client()
    sentiment_scores = {'positive': 0, 'neutral': 0, 'negative': 0}
    
    # Analyze sentiment of the entire document
    response = client.analyze_sentiment(documents=[text_content])[0]
    
    if not response.is_error:
        print("Full Document Sentiment:", response.sentiment)
        print("Confidence Scores:", response.confidence_scores)
        sentiment_scores['positive'] = response.confidence_scores.positive
        sentiment_scores['neutral'] = response.confidence_scores.neutral
        sentiment_scores['negative'] = response.confidence_scores.negative

    return text_content, sentiment_scores


def upload_and_analyze_news_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            full_content, sentiment_scores = analyze_economic_content_from_pdf(pdf_file)
            
            if full_content:
                article = NewsArticle.objects.create(
                    title="Extracted Full Content",
                    content=full_content
                )
                # Store sentiment scores if desired
                article.sentiment_score = sentiment_scores
                article.save()
                
                return redirect('result_chart_with_forecast')
            else:
                return render(request, 'news/error.html', {'message': 'No content found in the PDF.'})
    else:
        form = PDFUploadForm()
    return render(request, 'news/upload_pdf.html', {'form': form})


def news_list(request):
    news_items = NewsArticle.objects.all().order_by('-date_published')  # Assuming date_published exists in the model
    return render(request, 'news/news_list.html', {'news_items': news_items})



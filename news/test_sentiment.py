# test_sentiment.py

from sentiment_analysis import analyze_sentiment

def test_analyze_sentiment():
    # Sample texts with known sentiments
    test_cases = {
        "Positive News": "The economy is thriving with unprecedented growth and low unemployment rates.",
        "Negative News": "The economy has plummeted, leading to widespread unemployment and financial instability.",
        "Neutral News": "The council met to discuss upcoming infrastructure projects and budget allocations.",
        "Positive Example 1": "The company's profits have increased by 20% this quarter.",
        "Negative Example 1": "The project failed to meet its objectives, resulting in significant losses.",
        "Neutral Example 1": "The meeting is scheduled for next Monday at 10 AM.",
        "Simple Positive 1": "I am extremely happy with the results.",
        "Simple Positive 2": "This is the best day ever!",
        "Simple Positive 3": "I love sunny days.",
        "Simple Negative 1": "I am very sad today.",
        "Simple Neutral 1": "It is raining outside."
    }

    for label, text in test_cases.items():
        result = analyze_sentiment(text)
        if result:
            sentiment = result['sentiment']
            positive = result['positive']
            neutral = result['neutral']
            negative = result['negative']
            print(f"{label}:\nText: {text}\nSentiment: {sentiment}\nPositive Score: {positive}\nNeutral Score: {neutral}\nNegative Score: {negative}\n{'-'*60}")
        else:
            print(f"{label}:\nText: {text}\nSentiment Analysis Failed.\n{'-'*60}")

if __name__ == "__main__":
    test_analyze_sentiment()

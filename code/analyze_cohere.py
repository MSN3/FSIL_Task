# Import the necessary libraries
import os
import re
import cohere
import json
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from textblob import TextBlob

# Set up the Cohere API
cohere_api_key = 'YOUR_API_KEY_HERE'
co = cohere.Client(cohere_api_key)

# Define the preprocessing function
def preprocess_text(file_path):
    with open(file_path, 'r') as file:
        raw_10k = file.read()

    # Extract the relevant sections from the 10-K filing
    doc_start_pattern = re.compile(r'<DOCUMENT>')
    doc_end_pattern = re.compile(r'</DOCUMENT>')
    type_pattern = re.compile(r'<TYPE>[^\n]+')

    doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
    doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]
    doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

    document = {}

    for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
        if doc_type == '10-K':
            document[doc_type] = raw_10k[doc_start:doc_end]

    # Extract the start and end positions of the relevant sections
    regex = re.compile(r'((>Item|Item)(\s+|&#160;|&nbsp;)(6|7|8|9)\.{0,1})|(ITEM\s+(6|7|8|9))')
    matches = regex.finditer(document['10-K'])
    test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])
    test_df.columns = ['item', 'start', 'end']
    test_df['item'] = test_df.item.str.lower()

    # Get rid of unnecessary characters from the dataframe
    test_df.replace('&#160;',' ',regex=True,inplace=True)
    test_df.replace('&nbsp;',' ',regex=True,inplace=True)
    test_df.replace(' ','',regex=True,inplace=True)
    test_df.replace('\.','',regex=True,inplace=True)
    test_df.replace('>','',regex=True,inplace=True)

    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
    pos_dat.set_index('item', inplace=True)

    # Extract the content of the relevant sections
    item_6_raw = document['10-K'][pos_dat['start'].loc['item6']:pos_dat['start'].loc['item7']]
    item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item8']]
    item_8_raw = document['10-K'][pos_dat['start'].loc['item8']:pos_dat['start'].loc['item9']]

    # Limit the content to 5000 characters
    item_6_content = BeautifulSoup(item_6_raw, 'lxml').get_text(" ")[0:5000]
    item_7_content = BeautifulSoup(item_7_raw, 'lxml').get_text(" ")[0:5000]
    item_8_content = BeautifulSoup(item_8_raw, 'lxml').get_text(" ")[0:5000]

    return {
        "Selected Finance": item_6_content,
        "MD&A": item_7_content,
        "Financial Statement": item_8_content
    }

# Define the function to extract text from the filings
def extract_text_from_filings(directory):
    filings_data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "full-submission.txt":
                company = os.path.basename(os.path.dirname(root))
                year = os.path.basename(root).split('-')[1]
                file_path = os.path.join(root, file)
                sections = preprocess_text(file_path)
                text = f"{sections['Selected Finance']}\n{sections['MD&A']}\n{sections['Financial Statement']}"
                filings_data.append({
                    "company_name": company,
                    "filing_year": '\'' + year,
                    "text": text
                })
    return filings_data

# Define the function to generate insights from the texts
def generate_insights_from_texts(texts):
    insights = []
    for text in texts:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Analyze the following 10-K filing and provide key insights:\n{text}",
            max_tokens=100
        )
        insights.append({
            "company_name": text['company_name'],
            "filing_year": text['filing_year'],
            "insight": response.generations[0].text.strip()
        })
    return insights

# Define the function to analyze the sentiment of an insight
def analyze_sentiment(insight):
    blob = TextBlob(insight)
    if blob.sentiment.polarity > 0:
        return "positive"
    elif blob.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

# Define the function to visualize insights and sentiments
def visualize_insights_and_sentiments(insights):
    sentiments = [analyze_sentiment(insight['insight']) for insight in insights]
    companies = [f"{insight['company_name']} ({insight['filing_year']})" for insight in insights]

    df = pd.DataFrame({"Company": companies, "Sentiment": sentiments})
    sentiment_counts = df['Sentiment'].value_counts()

    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', ax=ax)
    ax.set_title('Sentiment Analysis of Insights')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')

    plt.tight_layout()
    plt.show()

# Define the function to save insights to a CSV file
def save_insights_to_csv(insights, filename):
    data = []
    for insight in insights:
        sentiment = analyze_sentiment(insight['insight'])
        data.append({
            "company_name": insight['company_name'],
            "filing_year": insight['filing_year'],
            "insight": insight['insight'],
            "sentiment": sentiment
        })
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Main function to extract text from filings, generate insights, and visualize them
if __name__ == "__main__":
    directory = "sec-edgar-filings"  # directory where the filings are stored
    texts = extract_text_from_filings(directory)
    insights = generate_insights_from_texts(texts)
    
    save_insights_to_csv(insights, "insights_cohere.csv") # save insights to a CSV file

    visualize_insights_and_sentiments(insights)

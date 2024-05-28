# import streamlit as st
# import pandas as pd

# def load_insights():
#     # Load your pre-saved insights
#     insights = pd.read_csv("D:/Georgia_Tech/Courses/Fintech_Lab/insights.csv")
#     return insights

# def display_insights(insights, ticker):
#     company_insights = insights[insights['Company'] == ticker]
#     st.write(company_insights[['Year', 'Insight']])
#     st.line_chart(company_insights.set_index('Year')['Insight Score'])

# if __name__ == "__main__":
#     st.title("Financial Insights from 10-K Filings")
#     st.write("Select a company ticker to view insights.")
#     ticker = st.selectbox("Company Ticker", options=['AAPL', 'GOOGL', 'MSFT'])
#     insights = load_insights()
#     display_insights(insights, ticker)

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

# Load insights from CSV file
def load_insights_from_csv(filename):
    return pd.read_csv(filename)

# Visualize insights and sentiments
# def visualize_insights_and_sentiments(insights):
#     sentiment_counts = insights['sentiment'].value_counts()

#     fig, ax = plt.subplots()
#     sentiment_counts.plot(kind='bar', ax=ax)
#     ax.set_title('Sentiment Analysis of Insights')
#     ax.set_xlabel('Sentiment')
#     ax.set_ylabel('Count')

#     st.pyplot(fig)

# Visualize insights and sentiments over the years
def visualize_sentiments_over_years(insights):
    insights['filing_year'] = insights['filing_year'].apply(lambda x: int(x.replace("'", '20')) if int(x.strip("'")) <= 23 else int(x.replace("'", '19')))
    
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    insights['sentiment_score'] = insights['sentiment'].map(sentiment_map)
    
    line_chart = alt.Chart(insights).mark_line(point=True).encode(
        x='filing_year:O',
        y='mean(sentiment_score):Q',
        color='company_name:N',
        tooltip=['company_name', 'filing_year', 'mean(sentiment_score)']
    ).properties(
        width=800,
        height=400,
        title='Average Sentiment Score Over the Years'
    ).interactive()

    st.altair_chart(line_chart)

# Display insights for a specific ticker
def display_insights_for_ticker(insights, ticker):
    filtered_insights = insights[insights['company_name'].str.contains(ticker, case=False)]
    if filtered_insights.empty:
        st.write(f"No insights found for ticker: {ticker}")
    else:
        for _, row in filtered_insights.iterrows():
            st.write(f"Company: {row['company_name']} ({row['filing_year']})")
            st.write(f"Insight: {row['insight']}")
            st.write(f"Sentiment: {row['sentiment']}")
            st.write("---")

def display_table(insights, ticker):
    company_insights = insights[insights['company_name'] == ticker]
    st.dataframe(company_insights[['company_name', 'filing_year', 'insight', 'sentiment']])

# Streamlit app
st.title("10-K Filings Analysis")
st.write("This app allows you to visualize insights and sentiments from 10-K filings.")

st.write("Select a company ticker to view insights.")
ticker_table = st.selectbox("Company Ticker", options=['AAPL', 'GOOGL', 'MSFT'])

# Load insights from CSV
insights_csv = "insights_cohere.csv"
insights = load_insights_from_csv(insights_csv)

st.write("Insights from 10-K Filings:")
display_table(insights, ticker_table)

# Visualize sentiments
st.write("Sentiment Analysis:")
visualize_sentiments_over_years(insights)

# Ticker input
ticker = st.text_input("Enter company ticker to view insights:")
if ticker:
    display_insights_for_ticker(insights, ticker)


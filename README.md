# FSIL_Task

# 10-K Filings Analysis App

This project analyzes SEC 10-K filings using the Cohere API to generate insights and sentiment analysis. The insights and sentiment data are then visualized using Streamlit.
You can find the deployed app on [WebLink](https://fsiltask-24.streamlit.app/)

## Tech Stack
- **Web App:** Streamlit - Chosen for its simplicity, ease of setup and seamless deployed without worrying about front-end and backend development 
- **LLM API:** Cohere - Provides powerful text analysis capabilities with a free tier for initial usage.
- **Visualization:** Matplotlib - For generating simple visualizations of the insights.

## Features

- **Preprocessing**: Extracts relevant sections (Selected Finance, MD&A, and Financial Statement) from 10-K filings.
- **Insight Generation**: Utilizes the Cohere API to generate key insights from the extracted text.
- **Sentiment Analysis**: Analyzes the sentiment of the generated insights using the Cohere API.
- **Visualization**: Displays sentiment trends over the years for different companies using Streamlit and Altair.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7+
- Required Python packages (listed in `requirements.txt`)

## Configuration

1. **Cohere API Key**:
   
   Add your Cohere API key to the script by setting the `cohere_api_key` variable in `analyze_cohere.py`.

2. **Directory Structure**:

   Ensure your SEC 10-K filings are organized in the following directory structure:

    ```
    sec-edgar-filings/
    ├── <company-ticker>/
    │   ├── <year>/
    │   │   ├── full-submission.txt
    ```

## Usage

1. **Generate Insights**:

   Run the script to preprocess filings, generate insights, analyze sentiments, and save the results to a CSV file:

    ```bash
    python analyze_cohere.py
    ```

2. **Run the Streamlit App Locally**:

   Launch the Streamlit app to visualize the data:

    ```bash
    streamlit run app.py
    ```

## Example Insights CSV

The generated CSV file (`insights_cohere.csv`) will contain the following columns:

- `company_name`: Name of the company.
- `filing_year`: Year of the 10-K filing.
- `insight`: Generated insight text.
- `sentiment`: Sentiment of the insight (positive, neutral, negative).

## Visualization

The Streamlit app provides:

- **Dataframe View**: Displays the insights and sentiments.
- **Sentiment Trend Line Chart**: Shows the average sentiment score over the years for different companies.
- **Ticker-based Insights**: Allows users to input a ticker to view specific insights for a company.


## Acknowledgements

- [Cohere API](https://cohere.ai/)
- [SEC EDGAR](https://www.sec.gov/edgar.shtml)
- [Streamlit](https://streamlit.io/)
- [Altair](https://altair-viz.github.io/)

---

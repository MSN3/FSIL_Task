from sec_edgar_downloader import Downloader
import os

def download_filings(tickers, start_year=1995, end_year=2023):
    dl = Downloader("GaTech","nshanbhogue6@gatech.edu","D:\Georgia_Tech\Courses\Fintech_Lab")
    for ticker in tickers:
        for year in range(start_year, end_year + 1):
            try:
                dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")
                print(f"Downloaded {ticker} 10-K for {year}")
            except Exception as e:
                print(f"Could not download {ticker} 10-K for {year}: {e}")

if __name__ == "__main__":
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    download_filings(tickers)

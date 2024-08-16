import json
import time
import pandas as pd
from polygon import RESTClient

client = RESTClient("YOUR_TOKEN")

# Takes in a path to a json file (string) and number of rows (integer) to load in
# Loads in the json file and searches for tickers
# Returns the tickers (list of strings)
def load_tickers(filename, num_rows=None):
    tickers = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if num_rows is not None and i >= num_rows:
                break
            try:
                data = json.loads(line)
                ticker = data.get("Symbol")
                if ticker:
                    tickers.append(ticker)
            except json.JSONDecodeError:
                print(f"Error decoding JSON on line: {line}")
    return tickers

# Takes in tickers (list of strings) and a date (string)
# Returns the json objects for each of those tickers in that specific date, containg info on high and low prices
def get_stocks(tickers, date):
    results = []
    for ticker in tickers:
        print(f"Getting data for ticker {ticker} for {date}.")
        try:
            request = client.get_daily_open_close_agg(ticker, date)
            results.append((ticker, request))
            time.sleep(13)  
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return results

companies = load_tickers('YOUR_DIR', num_rows=100)

stocks1 = get_stocks(companies, "SOME_DATE")
df1 = pd.DataFrame(stocks1)
df1.to_pickle('FILE_NAME')




import pandas as pd
import zipline
from trading_calendars import get_calendar
from yahoofinancials import YahooFinancials
import warnings
import os
import sys
import pandas_market_calendars as mcal

def get_date_indices(benchmark, start_date, end_date, freq):
    yahoo_financials = YahooFinancials(benchmark)

    df = yahoo_financials.get_historical_price_data(start_date, end_date, freq)
    df = pd.DataFrame(df[benchmark]['prices']).drop(['date'], axis=1) \
            .rename(columns={'formatted_date':'date'}) \
            .set_index('date')
    df.index = pd.to_datetime(df.index)
    return df.index


def download_csv_data(ticker, start_date, end_date, freq, path, date_mask):

    yahoo_financials = YahooFinancials(ticker)

    df = yahoo_financials.get_historical_price_data(start_date, end_date, freq)
    df = pd.DataFrame(df[ticker]['prices']).drop(['date'], axis=1) \
            .rename(columns={'formatted_date':'date'}) \
            .loc[:, ['date','open','high','low','close','volume']] \
            .set_index('date')
    df.index = pd.to_datetime(df.index)
    df['dividend'] = 0
    df['split'] = 1
    # save data to csv for later ingestion
    df = df[df.index.isin(date_mask)] # For consistency
    assert(len(df) == len(date_mask))

    df.to_csv(path, header=True, index=True)

try:
    os.mkdir('./daily')
except OSError as error:
    print(error)

tickers = ["SPY", "MSFT", "AMZN", "FB", "GOOG", "AAPL", "NFLX", "BTC-USD"]
start_date = os.environ.get('START_HISTORY')
end_date = os.environ.get('END_HISTORY')
freq = 'daily'
path = './daily/'

#nyse = mcal.get_calendar('NYSE')
#dates_used = nyse.valid_days(start_date=start_date, end_date=end_date)
dates_used = get_date_indices("SPY", start_date, end_date, freq)

for ticker in tickers:
    download_csv_data(ticker=ticker, 
                    start_date=start_date, 
                    end_date=end_date, 
                    freq='daily', 
                    path=path+ticker+'.csv',
                    date_mask = dates_used)

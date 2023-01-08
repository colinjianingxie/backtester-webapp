import numpy as np
import pandas as pd
import datetime
from securities_master.models import DailyPrice, Symbol
import warnings
warnings.filterwarnings("ignore")

def convert_columns_to_numeric(df, column_names):
    for col in column_names:
        df[col] = pd.to_numeric(df[col])
    return df

def convert_columns_to_date(df, column_names):
    for col in column_names:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df

def get_daily_price(ticker, start_date, end_date, values, vendor_name):
    queryset = DailyPrice.objects.filter(symbol=ticker, data_vendor__name=vendor_name, price_date__range=[start_date, end_date]).values(*values)
    df = pd.DataFrame.from_records(queryset)
    df.columns = values
    df = convert_columns_to_numeric(df, ["open_price", "high_price", "low_price", "close_price", "adj_close_price"])
    df = convert_columns_to_date(df, ["price_date"])
    df.set_index("price_date", inplace = True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return df

def get_daily_prices(ticker_names, start_date, end_date, quick_extract=True, vendor_name='AlphaVantage'):

    ticker_res = {}
    values = ["price_date", "open_price", "high_price", "low_price", "close_price", "adj_close_price", "volume"]

    if not end_date:
        end_date = datetime.datetime.today()

    for tname in ticker_names:

        try:
            ticker = Symbol.objects.get(ticker=tname.upper())
            df = get_daily_price(ticker, start_date, end_date, values, vendor_name)
            ticker_res[tname] = df
        except Symbol.DoesNotExist:
            ticker_res[tname] = None
            print(f"Ticker {tname} does not exist...")
            break

    if quick_extract and len(ticker_names) == 1:
        return ticker_res[ticker_names[0]]
    return ticker_res

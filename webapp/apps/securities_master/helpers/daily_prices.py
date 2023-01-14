import datetime
import warnings

import numpy as np
import pandas as pd
from securities_master.models import DailyPrice
from securities_master.models import Symbol
warnings.filterwarnings("ignore")

def convert_columns_to_numeric(df, column_names):
    for col in column_names:
        df[col] = pd.to_numeric(df[col])
    return df

def convert_columns_to_date(df, column_names):
    for col in column_names:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df

def get_daily_price_df(ticker, start_date=None, end_date=None):
    if start_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_date = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
    if end_date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.now()

    values = ["price_date", "open_price", "high_price", "low_price", "close_price", "adj_close_price", "volume"]
    queryset = DailyPrice.objects.filter(symbol__ticker=ticker, data_vendor__name="Yahoo Finance", price_date__range=[start_date, end_date]).values(*values)
    df = pd.DataFrame.from_records(queryset)
    df.columns = values
    df = convert_columns_to_numeric(df, ["open_price", "high_price", "low_price", "close_price", "adj_close_price"])
    df = convert_columns_to_date(df, ["price_date"])
    df.set_index("price_date", inplace = True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return df

# alpha_vantage.py
from datetime import datetime as dt
import json
import pandas as pd
import requests
from .settings import *

class AlphaVantage(object):
	"""
	Encapsulates calls to the AlphaVantage API with a provided
	API key.
	"""
	def __init__(self, api_key=ALPHAVANTAGE_API_KEY):
		"""
		Initialise the AlphaVantage instance.
		Parameters
		----------
		api_key : str: optional
		The API key for the associated AlphaVantage account
		"""

		self.api_key = api_key

	def _construct_alpha_vantage_symbol_call(self, ticker):
		"""
		Construct the full API call to AlphaVantage based on the user
		provided API key and the desired ticker symbol.
		Parameters
		----------
		ticker : str
		The ticker symbol, e.g. 'AAPL'
		Returns
		-------
		'str'
		The full API call for a ticker time series
		"""
		return f'{ALPHA_VANTAGE_BASE_URL}/{ALPHA_VANTAGE_TIME_SERIES_CALL}&symbol={ticker}&outputsize=full&apikey={self.api_key}'

	def get_daily_historic_data(self, ticker, start_date=None, end_date=None):
		"""
		Use the generated API call to query AlphaVantage with the
		appropriate API key and return a list of price tuples
		for a particular ticker.
		Parameters
		----------
		ticker : 'str'
		The ticker symbol, e.g. 'AAPL'
		start_date : 'datetime'
		The starting date to obtain pricing for
		end_date : 'datetime'
		The ending date to obtain pricing for
		Returns
		-------
			'pd.DataFrame'
		The frame of OHLCV prices and volumes
		"""

		av_url = self._construct_alpha_vantage_symbol_call(ticker)

		try:
			av_data_js = requests.get(av_url)
			data = json.loads(av_data_js.text)['Time Series (Daily)']
		except Exception as e:
			print(f"Could not download AlphaVantage data for {ticker} ticker ({e})...stopping.")
			return pd.DataFrame(columns=COLUMNS).set_index('Date')
		else:
			prices = []
			for date_str in sorted(data.keys()):
				date = dt.strptime(date_str, '%Y-%m-%d')
				bar = data[date_str]

				if start_date and end_date and (date < start_date or date > end_date):
					continue

				prices.append((
					date,
					float(bar['1. open']),
					float(bar['2. high']),
					float(bar['3. low']),
					float(bar['4. close']),
					int(bar['6. volume']),
					float(bar['5. adjusted close'])
				))

		return pd.DataFrame(prices, columns=COLUMNS).set_index('Date')

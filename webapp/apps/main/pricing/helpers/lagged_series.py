from datetime import datetime as dt, timedelta as td
import numpy as np
import pandas as pd

from main.pricing.helpers.get_daily_prices import get_daily_prices

def create_lagged_series(ticker_name, start_date, end_date, lags=5, column_name='adj_close_price', additional_columns=['volume'], vendor_name='AlphaVantage'):
	"""
	This creates a Pandas DataFrame that stores the
	percentage returns of the adjusted closing value of
	a stock obtained from AlphaVantage, along with a
	number of lagged returns from the prior trading days
	(lags defaults to 5 days). Trading volume, as well as
	the Direction from the previous day, are also included.
	Parameters
	----------
	av : 'AlphaVantage' The AlphaVantage API instance used to obtain pricing
	symbol : 'str'
	The ticker symbol to obtain from AlphaVantage
	start_date : 'datetime'
	The starting date of the series to obtain
	end_date : 'datetime'
		The ending date of the the series to obtain
	lags : 'int', optional
		The number of days to 'lag' the series by
	Returns
	-------
	'pd.DataFrame'
	Contains the Adjusted Closing Price returns and lags
	"""

	adj_start_date = start_date - td(days=365)

	daily_prices = get_daily_prices(ticker_names=ticker_name, start_date=adj_start_date, end_date=end_date, quick_extract=True, vendor_name=vendor_name)

	# Create the new lagged DataFrame
	tslag = pd.DataFrame(index=daily_prices.index)

	tslag['Today'] = daily_prices[column_name]


	for adcol in additional_columns:
		tslag[adcol.title()] = daily_prices[adcol]

	# Create the shifted lag series of prior trading period close values
	for i in range(0, lags):
		tslag[f'Lag{str(i+1)}'] = daily_prices[column_name].shift(i+1)

	# Create the returns DataFrame
	tsret = pd.DataFrame(index=tslag.index)

	for adcol in additional_columns:
		tsret[adcol.title()] = tslag[adcol.title()]

	tsret['Today'] = tslag['Today'].pct_change() * 100.0

	# If any of the values of percentage returns equal zero, set them to
	# a small number (stops issues with QDA model in scikit-learn)
	tsret.loc[tsret['Today'].abs() < 0.0001, ['Today']] = 0.0001

	# Create the lagged percentage returns columns
	for i in range(0, lags):
		tsret[f'Lag{str(i+1)}'] = tslag[f'Lag{str(i+1)}'].pct_change() * 100.0
	# Create the "Direction" column (+1 or -1) indicating an up/down day
	tsret['Direction'] = np.sign(tsret['Today'])
	tsret = tsret[tsret.index >= start_date]
	return tsret

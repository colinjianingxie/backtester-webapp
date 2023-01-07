from numpy import array, cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input

def hurst(time_series):
	"""
	Calculates the Hurst Exponent of the time series vector ts.
	Parameters
	----------
	ts : 'np.ndarray'
		Time series array of prices
	Returns
	-------
	'float'
		The Hurst Exponent of the time series
	"""
	# Create the range of lag values
	lags = range(2, 100)

	# Calculate the array of the variances of the lagged differences
	tau = [sqrt(std(subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]

	# Use a linear fit to estimate the Hurst Exponent
	poly = polyfit(log(lags), log(tau), 1)

	# Return the Hurst exponent from the polyfit output
	return poly[0] * 2.0


def perform_hurst():

	ticker_names, start_date, end_date = call_basic_security_input()

	# Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
	gbm = log(cumsum(randn(100000)) + 1000)
	mr = log(randn(100000) + 1000)
	tr = log(cumsum(randn(100000) + 1) + 1000)

	daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date)

	# Output the Hurst Exponent for each of the above series # and the price of Amazon (the Adjusted Close price) for
	# the ADF test given above in the article
	print(f"Hurst(GBM) - Geometric Brownian Motion: {hurst(gbm):0.2f}")
	print(f"Hurst(MR) - Mean Reverting: {hurst(mr):0.2f}")
	print(f"Hurst(TR) - Trending: {hurst(tr):0.2f}")
	print(f"Hurst({ticker_names[0]}): {hurst(array(daily_prices['adj_close_price'])):0.2f}")

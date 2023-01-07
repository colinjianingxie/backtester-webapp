
import numpy as np
from scipy.stats import norm
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input


def var_cov_var(P, c, mu, sigma):
	"""
	Variance-Covariance calculation of daily Value-at-Risk using confidence level c, with mean of returns mu
	and standard deviation of returns sigma, on a portfolio
	of value P.
	"""

	alpha = norm.ppf(1-c, mu, sigma) # Inverse of norm cdf

	return P - P*(alpha + 1)


def perform_var():

	ticker_names, start_date, end_date = call_basic_security_input()

	daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date)

	daily_prices["rets"] = daily_prices["adj_close_price"].pct_change()

	P = 1e6 # 1,000,000 USD
	c = 0.99 # 99% confidence interval
	mu = np.mean(daily_prices["rets"])
	sigma = np.std(daily_prices["rets"])

	var = var_cov_var(P, c, mu, sigma)

	print(f"Value-at-Risk: ${var:.2f}")

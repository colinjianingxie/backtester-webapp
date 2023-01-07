from datetime import datetime as dt
import numpy as np
import pandas as pd
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input

def annualised_sharpe(returns, N=252):
	"""
	Calculate the annualised Sharpe ratio of a returns stream based on a number of trading periods, N.
	N defaults to 252, which then assumes a stream of daily returns.
	The function assumes that the returns are the excess of
	those compared to a benchmark.
	"""
	return np.sqrt(N) * returns.mean() / returns.std()

def equity_sharpe(ticker, risk_free_rate=0.05):
	"""
	Calculates the annualised Sharpe ratio based on the daily
	returns of an equity ticker symbol listed in AlphaVantage.
	"""
	# Use the percentage change method to easily calculate daily returns
	ticker['daily_ret'] = ticker['close_price'].pct_change()

	# Assume an average annual risk-free rate over the period of 5%
	ticker['excess_daily_ret'] = ticker['daily_ret'] - risk_free_rate/252

	# Return the annualised Sharpe ratio based on the excess daily returns
	return annualised_sharpe(ticker['excess_daily_ret'])

def market_neutral_sharpe(ticker, benchmark):
	"""
	Calculates the annualised Sharpe ratio of a market
	neutral long/short strategy inolving the long of 'ticker'
	with a corresponding short of the ’benchmark’.
	"""
	# Calculate the percentage returns on each of the time series
	ticker['daily_ret'] = ticker['close_price'].pct_change()
	benchmark['daily_ret'] = benchmark['close_price'].pct_change()
	# Create a new DataFrame to store the strategy information
	# The net returns are (long - short)/2, since there is twice
	# the trading capital for this strategy
	strat = pd.DataFrame(index=ticker.index)
	strat['net_ret'] = (ticker['daily_ret'] - benchmark['daily_ret'])/2.0

	# Return the annualised Sharpe ratio for this strategy
	return annualised_sharpe(strat['net_ret'])

def perform_sharpe():

	ticker_names, start_date, end_date = call_basic_security_input()
	ticker_names.append('SPY')

	daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date)

	for t in ticker_names:
		print(f"{t} Sharpe Ratio: {equity_sharpe(daily_prices[t])}")

	print(f"{ticker_names[0]} Market Neutral Sharpe Ratio: {market_neutral_sharpe(daily_prices[ticker_names[0]], daily_prices[ticker_names[1]])}")

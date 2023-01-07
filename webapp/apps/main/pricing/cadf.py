import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import statsmodels.api as sm
import pprint
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input

def plot_price_series(df, ts1, ts2, start_date, end_date):
	"""
	Plot both time series on the same line graph for
	the specified date range.
	Parameters
	----------
	df : 'pd.DataFrame'
		The DataFrame containing prices for each series
	ts1 : 'str'
	The first time series column name
	ts2 : 'str'
		The second time series column name
	start_date : 'datetime'
		The starting date for the plot
	end_date : 'datetime'
	The ending date for the plot
	"""
	months = mdates.MonthLocator() # every month

	fig, ax = plt.subplots()
	ax.plot(df.index, df[ts1], label=ts1)
	ax.plot(df.index, df[ts2], label=ts2)
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
	ax.set_xlim(start_date, end_date)
	ax.grid(True)
	fig.autofmt_xdate()

	plt.xlabel('Month/Year')
	plt.ylabel('Price ($)')
	plt.title(f'{ts1} and {ts2} Daily Prices')
	plt.legend()

	plt.show()

def plot_scatter_series(df, ts1, ts2):
	"""
	Plot a scatter plot of both time series for
	via the provided DataFrame.
	Parameters
	----------
	df : 'pd.DataFrame'
		The DataFrame containing prices for each series
	ts1 : 'str'
	The first time series column name
	ts2 : 'str'
	The second time series column name
	"""
	plt.xlabel(f'{ts1} Price ($)')
	plt.ylabel(f'{ts2} Price ($)')
	plt.title(f'{ts1} and {ts2} Price Scatterplot')

	plt.scatter(df[ts1], df[ts2])
	plt.show()

def plot_residuals(df, start_date, end_date):
	"""
	 Plot the residuals of OLS procedure for both
	time series.
	 Parameters
	----------
	 df : 'pd.DataFrame'
		The residuals DataFrame
	start_date : 'datetime'
		 The starting date of the residuals plot
	end_date : 'datetime'
		The ending date of the residuals plot
	 """
	months = mdates.MonthLocator() # every month
	fig, ax = plt.subplots()
	ax.plot(df.index, df["res"], label="Residuals", c='blue')
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
	ax.set_xlim(start_date, end_date)
	ax.grid(True)
	fig.autofmt_xdate()


	plt.xlabel('Month/Year')
	plt.ylabel('Price ($)')
	plt.title('Residual Plot')
	plt.legend()
	plt.plot(df["res"])
	plt.show()

def perform_cadf():

	ticker_names, start_date, end_date = call_basic_security_input(2)


	daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date)

	# Place them into the Pandas DataFrame format
	df = pd.DataFrame(index=daily_prices[ticker_names[0]].index)

	for tname in ticker_names:
		df[tname] = np.array(daily_prices[tname]['adj_close_price'])

	# Plot the two time series
	plot_price_series(df, ticker_names[0], ticker_names[1], start_date, end_date)
	# Display a scatter plot of the two time series
	plot_scatter_series(df, ticker_names[0], ticker_names[1])


	# Calculate optimal hedge ratio "beta" via Statsmodels
	model = sm.OLS(df[ticker_names[1]], df[ticker_names[0]])
	res = model.fit()
	beta_hr = res.params[0]

	# Calculate the residuals of the linear combination
	df["res"] = df[ticker_names[1]] - beta_hr * df[ticker_names[0]]

	# Plot the residuals
	# plot_residuals(df, start_date, end_date)

	# Calculate and output the CADF test on the residuals
	print("---------")
	test_statistic, p_value, samples_run, sample_size, stats, x = ts.adfuller(df["res"])
	print(f"number samples: {sample_size}")
	print(f"test_statistic: {test_statistic}")
	print(f"p value: {p_value}")
	for key, value in stats.items():
		significant = f"significant and POSSIBLY possess a cointegrating relationship between {str(start_date)} and {str(end_date)}" if test_statistic < value else "not significant and NO possible cointegrating relationship"
		print(f"critical at {key}: {value} ({significant})")

import yfinance as yf
import warnings
from utils.helper.timer import time_function
from utils.helper.init_vendors import create_or_update_vendor
from utils.vendors.db_functions import obtain_list_of_db_tickers, insert_daily_data_into_db

def start_yahoo_finance():
	#TICKER_COUNT = 500 # Change this to 500 to download all tickers
	WAIT_TIME_IN_SECONDS = 15.0 # Adjust how frequently the API is called
	TARGETS = []
	START_INDEX = 140
	vendor = create_or_update_vendor('Yahoo Finance')

	# This ignores the warnings regarding Data Truncation
	# from the AlphaVantage precision to Decimal(19,4) datatypes
	warnings.filterwarnings('ignore')
	# Loop over the tickers and insert the daily historical # data into the database

	tickers = obtain_list_of_db_tickers(TARGETS, START_INDEX) if len(TARGETS) == 0 else obtain_list_of_db_tickers(TARGETS)

	lentickers = len(tickers)
	for i, t in enumerate(tickers):
		print(f"Adding data for {t.ticker}: {i+1} out of {lentickers}")
		yfinance_data = yf.download(t.ticker)
		#ticker = yf.Ticker(t.ticker)
		#print(ticker.actions)
		#print(ticker.dividends)
		#print(ticker.splits)
		#print(ticker.capital_gains)
		#print(ticker.shares)
		#print(ticker.income_stmt)
		#print(ticker.quarterly_income_stmt)
		#print(ticker.balance_sheet)
		#print(ticker.quarterly_balance_sheet)
		#print(ticker.cashflow)
		#print(ticker.quarterly_cashflow)
		#print(ticker.earnings)
		#print(ticker.quarterly_earnings)
		#print(ticker.revenue_forecasts)
		#print(ticker.earnings_forecasts)
		#print(ticker.earnings_trend)
		#print(ticker.earnings_dates)
		time_function(insert_daily_data_into_db, t, vendor, yfinance_data, "OVERRIDE")


	print("Successfully added AlphaVantage pricing data to DB.")

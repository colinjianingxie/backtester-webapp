import time
import warnings
from .alphavantage import AlphaVantage
from utils.helper.timer import time_function
from utils.helper.init_vendors import create_or_update_vendor
from utils.vendors.db_functions import obtain_list_of_db_tickers, insert_daily_data_into_db


def start_alphavantage():
	#TICKER_COUNT = 500 # Change this to 500 to download all tickers
	WAIT_TIME_IN_SECONDS = 15.0 # Adjust how frequently the API is called
	TARGETS = ['AAPL']

	vendor = create_or_update_vendor('AlphaVantage')

	# This ignores the warnings regarding Data Truncation
	# from the AlphaVantage precision to Decimal(19,4) datatypes
	warnings.filterwarnings('ignore')
	# Loop over the tickers and insert the daily historical # data into the database
	av = AlphaVantage()

	tickers = obtain_list_of_db_tickers() if len(TARGETS) == 0 else obtain_list_of_db_tickers(TARGETS)

	lentickers = len(tickers)
	for i, t in enumerate(tickers):
		print(f"Adding data for {t.ticker}: {i+1} out of {lentickers}")
		av_data = av.get_daily_historic_data(t.ticker)
		time_function(insert_daily_data_into_db, t, vendor, av_data, "OVERRIDE")
		time.sleep(WAIT_TIME_IN_SECONDS)

	print("Successfully added AlphaVantage pricing data to DB.")

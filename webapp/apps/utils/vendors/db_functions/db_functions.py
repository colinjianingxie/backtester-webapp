from securities_master.models import Symbol, DailyPrice
from datetime import datetime as dt

def obtain_list_of_db_tickers(ticker_list=[], start_index=None):
	"""
	Obtains a list of the ticker symbols in the database.
	"""
	if ticker_list:
		return Symbol.objects.filter(ticker__in=ticker_list)
	if start_index:
		return Symbol.objects.order_by('ticker').all()[start_index:]
	return Symbol.objects.order_by('ticker').all()


def insert_daily_data_into_db(symbol, vendor, daily_data, process_type="OVERRIDE"):
	# TODO: Find way to skip current data...
	"""
		Takes a list of tuples of daily data and adds it to the
		MySQL database. Appends the vendor ID and symbol ID to the data.

	"""
	now = dt.utcnow()
	# Amend the data to include the vendor ID and symbol ID
	list_of_data_to_insert = [
		DailyPrice(
			data_vendor=vendor,
			symbol=symbol,
			price_date=index,
			open_price=row['Open'],
			high_price=row['High'],
			low_price=row['Low'],
			close_price=row['Close'],
			adj_close_price=row['Adj Close'],
			volume=row['Volume'],
			created_date=now,
			last_updated_date=now,
		) for index, row in daily_data.iterrows()
	]

	DailyPrice.objects.bulk_create(list_of_data_to_insert)

	'''
	for index, row in daily_data.iterrows():

		try:
			obj = DailyPrice.objects.get(
				symbol=symbol,
				price_date=index,
				data_vendor=vendor,
			)
			# TODO: Should only update if the historical price is somehow different...
			if process_type == "OVERRIDE":
				obj.last_updated_date = now
				obj.open_price=row['Open']
				obj.high_price=row['High']
				obj.low_price=row['Low']
				obj.close_price=row['Close']
				obj.adj_close_price=row['Adj Close']
				obj.volume=row['Volume']
				obj.save()
				#print(f"Override {symbol} : {index}")
			else:
				#print(f"Price already exists on {index}")
				continue

		except DailyPrice.DoesNotExist:
			#print(f"{vendor} Inserting new price for {symbol} on {index}")
			obj = DailyPrice(
				data_vendor=vendor,
				symbol=symbol,
				price_date=index,
				open_price=row['Open'],
				high_price=row['High'],
				low_price=row['Low'],
				close_price=row['Close'],
				adj_close_price=row['Adj Close'],
				volume=row['Volume'],
				created_date=now,
				last_updated_date=now,
			)
			obj.save()
	'''

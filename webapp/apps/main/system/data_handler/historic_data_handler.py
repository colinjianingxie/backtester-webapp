import datetime

import numpy as np
import pandas as pd
from securities_master.helpers.daily_prices import get_daily_price_df
from main.system.event import MarketEvent

from .data_handler import DataHandler

class HistoricDataHandler(DataHandler):
	"""
	HistoricDataHandler is designed to read	each requested symbol from disk and provide an interface
	to obtain the "latest" bar in a manner identical to a live trading interface.
	"""

	def __init__(self, events, symbol_list, custom_parameters):
		"""
		Parameters:
		events - The Event Queue.
		symbol_list - A list of symbol strings.
		"""
		self.events = events
		self.symbol_list = symbol_list
		self.symbol_data = {}
		self.start_date = custom_parameters['data_handler']['start_date']
		self.end_date = custom_parameters['data_handler']['end_date']
		self.vendor_name = custom_parameters['data_handler']['vendor_name']
		self.latest_symbol_data = {}
		self.continue_backtest = True
		self._init_data()

	def _init_data(self):
		"""
		Obtain values from Securites Master DB, converting
		them into pandas DataFrames within a symbol dictionary.
		For this handler it will be assumed that the data is
		taken from AlphaVantage. Thus its format will be respected.
		"""
		comb_index = None

		for s in self.symbol_list:
			self.symbol_data[s] = get_daily_price_df(s, self.start_date, self.end_date)

		for s in self.symbol_list:
			# Combine the index to pad forward values
			# Combines all the dates to create full set of dates as index...
			if comb_index is None:
				comb_index = self.symbol_data[s].index
			else:
				comb_index.union(self.symbol_data[s].index)

			# Set the latest symbol_data to None
			self.latest_symbol_data[s] = []


		for s in self.symbol_list:
			self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='pad') # Set all of the indices to be the combined index
			self.symbol_data[s]["returns"] = self.symbol_data[s]["adj_close_price"].pct_change().dropna() # Percentage change between current value and prior value
			self.symbol_data[s] = self.symbol_data[s].iterrows() # Make each row iterable in the dataframe


	def _get_new_bar(self, symbol):
		"""
		Returns the latest bar from the data feed.
		Specifically returns a generator object:
		to get b[0], need to call: gen.next().
		to get b[1], call gen.next() again..
		"""
		for b in self.symbol_data[symbol]:
			yield b


	def get_latest_bar(self, symbol):
		"""
		Returns the last bar from the latest_symbol list.
		"""
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print(f"{symbol} is not available in the historical data set.")
			raise
		else:
			return bars_list[-1]

	def get_latest_bars(self, symbol, N=1):
		"""
		Returns the last N bars from the latest_symbol list,
		or N-k if less available.
		"""
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-N:] # Returns last N values...

	def get_latest_bar_datetime(self, symbol):
		"""
		Returns a Python datetime object for the last bar.
		"""
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-1][0] # Returns datetime for lastest value since it's index at 0

	def get_latest_bar_value(self, symbol, val_type):
		"""
		Returns one of the Open, High, Low, Close, Volume or OI
		values from the Pandas Bar series object.
		"""
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return getattr(bars_list[-1][1], val_type) # Utilizes getattr to get dict key

	def get_latest_bars_values(self, symbol, val_type, N=1):
		"""
		Returns the last N bar values from the
		latest_symbol list, or N-k if less available.
		"""
		try:
			bars_list = self.get_latest_bars(symbol, N)
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return np.array([getattr(b[1], val_type) for b in bars_list]) # Returns np array of all the values of the latest values


	def update_bars(self):
		"""
		Pushes the latest bar to the latest_symbol_data structure for all symbols in the symbol list.
		"""
		for s in self.symbol_list:
			try:
				bar = next(self._get_new_bar(s)) # Iterate through the generator function... get the next bar of data.
			except StopIteration:
				self.continue_backtest = False # stop the backtest when we reach the end of the iterator.
			else:
				if bar is not None:
					self.latest_symbol_data[s].append(bar) # Add the bar to the latest symbol data.
			self.events.put(MarketEvent()) # Put an empty market event onto the queue.

from datetime import datetime as dt

import numpy as np
from main.system.event import SignalEvent
from main.system.strategy.strategy import Strategy

class MovingAverageCrossover(Strategy):
	"""
	Carries out a basic Moving Average Crossover strategy with a
	short/long simple weighted moving average. Default short/long windows are 100/400 periods respectively.
	"""
	def __init__(self, bars, events, custom_parameters):
		"""
		Initialises the Moving Average Cross Strategy.
		Parameters:
		bars - The DataHandler object that provides bar information
		events - The Event Queue object.
		short_window - The short moving average lookback.
		long_window - The long moving average lookback.
		"""
		self.bars = bars
		self.symbol_list = self.bars.symbol_list
		self.events = events
		self.event_history = []
		self.short_window = int(custom_parameters['model']['short_window']) # TODO: Short window always <= long_window!
		self.long_window = int(custom_parameters['model']['long_window'])
		# Set to True if a symbol is in the market
		self.bought = self._calculate_initial_bought()

	def _calculate_initial_bought(self):
		"""
		Adds keys to the bought dictionary for all symbols
		and sets them to 'OUT'.
		"""
		bought = {}
		for s in self.symbol_list:
			bought[s] = 'OUT'
		return bought


	def calculate_signals(self, event):
		"""
		Generates a new set of signals based on the MAC
		SMA with the short window crossing the long window
		meaning a long entry and vice versa for a short entry.
		Parameters
		event - A MarketEvent object.
		"""
		if event.type == 'MARKET':
			for s in self.symbol_list:
				# Get latest "long_window" number bar values
				bars = self.bars.get_latest_bars_values(s, "adj_close_price", N=self.long_window)
				bar_date = self.bars.get_latest_bar_datetime(s) # Get latest datetime

				if bars is not None and bars != []:
					short_sma = np.mean(bars[-self.short_window:]) # From the latest long_window bars, average the last short_window.
					long_sma = np.mean(bars[-self.long_window:]) # Average the long_window bars
					symbol = s
					cur_date = dt.utcnow()
					sig_dir = ""
					# WILL alternate between "Long, Out, Long, Out"
					if short_sma > long_sma and self.bought[s] == "OUT":
						print(f"LONG: {bar_date}")
						sig_dir = 'LONG'
						signal = SignalEvent(1, symbol, cur_date, sig_dir, 1.0) # TODO: Strategy:id here... strength is 1.0...
						self.events.put(signal)
						self.bought[s] = 'LONG' # We've longed the equity...
					elif short_sma < long_sma and self.bought[s] == "LONG":
						print(f"SHORT: {bar_date}")
						sig_dir = 'EXIT'
						signal = SignalEvent(1, symbol, cur_date, sig_dir, 1.0)
						self.events.put(signal)
						self.bought[s] = 'OUT' # Change it back to "Out"...

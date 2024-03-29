import datetime
import pprint
from datetime import timedelta as td
try:
	import Queue as queue
except ImportError:
	import queue
import time


class Backtest(object):
	"""
	Enscapsulates the settings and components for carrying out
	an event-driven backtest.
	"""

	def __init__(self,
		symbol_list,
		initial_capital,
		heartbeat,
		data_handler,
		execution_handler,
		portfolio,
		strategy,
		custom_parameters,
		):
		# TODO: Differentiate MODEL start date and DATA start date...
		"""
		Initialises the backtest.
		Parameters:
		symbol_list - The list of symbol strings.
		intial_capital - The starting capital for the portfolio.
		heartbeat - Backtest "heartbeat" in seconds
		data_start_date - The start datetime of the portfolio/backtest.
		data_end_date - The end datetime of the portfolio/backtest
		data_handler - (Class) Handles the market data feed.
		execution_handler - (Class) Handles the orders/fills for trades.
		portfolio - (Class) Keeps track of portfolio current and prior positions.
		strategy - (Class) Generates signals based on market data.
		"""
		self.symbol_list = symbol_list
		self.initial_capital = initial_capital
		self.heartbeat = heartbeat
		self.data_handler_cls = data_handler
		self.execution_handler_cls = execution_handler
		self.portfolio_cls = portfolio
		self.strategy_cls = strategy
		self.custom_parameters = custom_parameters
		self.events = queue.Queue()
		self.signals = 0
		self.orders = 0
		self.fills = 0

		self._generate_trading_instances()

	def _generate_trading_instances(self):
		"""
		Generates the trading instance objects from
		their class types.
		"""
		print("Creating DataHandler, Strategy, Portfolio and ExecutionHandler")
		self.data_handler = self.data_handler_cls(self.events, self.symbol_list, self.custom_parameters)
		self.strategy = self.strategy_cls(self.data_handler, self.events, self.custom_parameters)
		self.portfolio = self.portfolio_cls(self.data_handler, self.events, self.initial_capital, self.custom_parameters)
		self.execution_handler = self.execution_handler_cls(self.events)


	def _run_backtest(self):
		"""
		Executes the backtest.
		"""
		i=0 # Counter for each tick..
		while True:
			i += 1
			print(i)
			# Update the market bars
			if self.data_handler.continue_backtest == True:
				self.data_handler.update_bars() # Continue to the next bar of data and put it on self.events
			else:
				break # Break out of whole backtest if we don't continue_backtest...

			# Handle the events
			while True:
				try:
					event = self.events.get(False) # Returns event if it is immediately available, else break.
				except queue.Empty:
					break
				else:
					#
					# TODO: Each event is processed here... Note that b/c each signal will generate order/fill...they should be equal.
					#
					if event is not None:
						if event.type == 'MARKET':
							self.strategy.calculate_signals(event)
							self.portfolio.update_timeindex(event)
						elif event.type == 'SIGNAL':
							self.signals += 1
							self.portfolio.update_signal(event)
						elif event.type == 'ORDER':
							self.orders += 1
							self.execution_handler.execute_order(event)
						elif event.type == 'FILL':
							self.fills += 1
							self.portfolio.update_fill(event)
				time.sleep(self.heartbeat) # Heartbeat is time it takes for each event to process...


	def _output_performance(self):
		"""
		Outputs the strategy performance from the backtest.
		"""
		self.portfolio.create_equity_curve_dataframe()
		print("Creating summary stats...")
		stats = self.portfolio.output_summary_stats()
		print("Creating equity curve...")
		print(self.portfolio.equity_curve.tail(10))
		pprint.pprint(stats)
		print(f"Signals: {self.signals}")
		print(f"Orders: {self.orders}")
		print(f"Fills: {self.fills}")
		stats['signals'] = self.signals
		stats['orders'] = self.orders
		stats['fills'] = self.fills
		return {
			'stats': stats,
		}


	def simulate_trading(self):
		"""
		Simulates the backtest and outputs portfolio performance.
		"""
		self._run_backtest()
		return self._output_performance()

import datetime
from math import floor

try:
	import Queue as queue
except ImportError:
	import queue

import numpy as np
import pandas as pd

from main.system.event import FillEvent, OrderEvent
from .performance import create_sharpe_ratio, create_drawdowns
from .plot_performance import plot_performance

class Portfolio(object):
	"""
	The Portfolio class handles the positions and market
	value of all instruments at a resolution of a "bar",
	i.e. secondly, minutely, 5-min, 30-min, 60 min or EOD.
	The positions DataFrame stores a time-index of the
	quantity of positions held.
	The holdings DataFrame stores the cash and total market
	holdings value of each symbol for a particular
	time-index, as well as the percentage change in
	portfolio total across bars.
	"""
	def __init__(self, bars, events, initial_capital, custom_parameters):
		"""
		Initialises the portfolio with bars and an event queue.
		Also includes a starting datetime index and initial capital
		(USD unless otherwise stated).
		The following method, construct_all_positions, simply creates a dictionary for each symbol,
		sets the value to zero for each and then adds a datetime key, finally adding it to a list.
		It uses a dictionary comprehension, which is similar in spirit to a list comprehension:

		Parameters:
		bars - The DataHandler object with current market data.
		events - The Event Queue object.
		start_date - The start date (bar) of the portfolio.
		initial_capital - The starting capital in USD.
		"""
		self.bars = bars
		self.events = events
		self.event_history = []
		self.symbol_list = self.bars.symbol_list
		self.start_date = custom_parameters['portfolio']['start_date']
		self.initial_capital = initial_capital
		self.all_positions = self.construct_all_positions()
		self.current_positions = dict((k,v) for k, v in [(s, 0) for s in self.symbol_list]) # {'ZBRA': 0, 'XYZ': 0}
		self.all_holdings = self.construct_all_holdings()
		self.current_holdings = self.construct_current_holdings()

	def construct_all_positions(self):
		"""
		Constructs the positions list using the start_date
		to determine when the time index will begin.
		e.g: [{
				'ZBRA': 0,
				'XYZ': 0,
				'datetime': datetime.datetime(2017, 1, 3, 0, 0, tzinfo=datetime.timezone.utc)
			 }]
		"""
		d = dict((k,v) for k, v in [(s, 0) for s in self.symbol_list])
		d['datetime'] = self.start_date
		return [d]

	def construct_all_holdings(self):
		"""
		Constructs the holdings list using the start_date
		to determine when the time index will begin.
		e.g: [{
				'ZBRA': 0.0,
				'XYZ': 0.0,
				'datetime': datetime.datetime(2017, 1, 3, 0, 0, tzinfo=datetime.timezone.utc),
				'cash': 100000.0,
				'commission': 0.0,
				'total': 100000.0
			}]
		"""
		d = dict((k,v) for k, v in [(s, 0.0) for s in self.symbol_list])
		d['datetime'] = self.start_date
		d['cash'] = self.initial_capital
		d['commission'] = 0.0
		d['total'] = self.initial_capital
		return [d]

	def construct_current_holdings(self):
		"""
		This constructs the dictionary which will hold the instantaneous value of the portfolio across all symbols.
		e.g: {
				'ZBRA': 0.0,
				'XYZ': 0.0,
				'cash': 100000.0,
				'commission': 0.0,
				'total': 100000.0
			}
		"""
		d = dict((k,v) for k, v in [(s, 0.0) for s in self.symbol_list])
		d['cash'] = self.initial_capital
		d['commission'] = 0.0
		d['total'] = self.initial_capital
		return d


	def update_timeindex(self, event):
		"""
		Adds a new record to the positions matrix for the current market data bar.
		This reflects the PREVIOUS bar, i.e. all
		current market data at this stage is known (OHLCV).
		Makes use of a MarketEvent from the events queue.
		"""

		latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])
		# Update positions
		# ================
		dp = dict((k,v) for k, v in [(s, 0) for s in self.symbol_list])
		dp['datetime'] = latest_datetime

		for s in self.symbol_list:
			dp[s] = self.current_positions[s]

		# Append the current positions
		self.all_positions.append(dp)

		# Update holdings
		# ===============
		dh = dict((k,v) for k, v in [(s, 0) for s in self.symbol_list])

		dh['datetime'] = latest_datetime
		dh['cash'] = self.current_holdings['cash']
		dh['commission'] = self.current_holdings['commission']
		dh['total'] = self.current_holdings['cash']
		for s in self.symbol_list:
			# Approximation to the real value
			market_value = self.current_positions[s] * self.bars.get_latest_bar_value(s, "adj_close_price") # Get the total amount bought from the adj_close_price
			dh[s] = market_value
			dh['total'] += market_value

		# Append the current holdings
		self.all_holdings.append(dh)


	def update_positions_from_fill(self, fill):
		"""
		Takes a Fill object and updates the position matrix to
		reflect the new position.

		Parameters:
		fill - The Fill object to update the positions with.
		"""

		# Check whether the fill is a buy or sell
		fill_dir = 0
		if fill.direction == 'BUY':
			fill_dir = 1
		if fill.direction == 'SELL':
			fill_dir = -1

		# Update positions list with new quantities
		self.current_positions[fill.symbol] += fill_dir*fill.quantity


	def update_holdings_from_fill(self, fill):
		"""
		Takes a Fill object and updates the holdings matrix to
		reflect the holdings value.
		Parameters:
		fill - The Fill object to update the holdings with.
		"""
		# Check whether the fill is a buy or sell
		fill_dir = 0
		if fill.direction == 'BUY':
			fill_dir = 1
		if fill.direction == 'SELL':
			fill_dir = -1

		# Update holdings list with new quantities
		fill_cost = self.bars.get_latest_bar_value(fill.symbol, "adj_close_price") 	# stock_price
		cost = fill_dir * fill_cost * fill.quantity # +-1 * stock price * quantity filled.
		self.current_holdings[fill.symbol] += cost # The cost for either purchasing or selling equity.
		self.current_holdings['commission'] += fill.commission # how much the commision was
		self.current_holdings['cash'] -= (cost + fill.commission) # Gain money from shorting, lose money from buying
		self.current_holdings['total'] -= (cost + fill.commission) # Since total equity is based on cash, same as cash

	def update_fill(self, event):
		"""
		Updates the portfolio current positions and holdings
		from a FillEvent.
		"""

		if event.type == 'FILL':
			self.update_positions_from_fill(event)
			self.update_holdings_from_fill(event)



	def generate_naive_order(self, signal):
		"""
		Simply files an Order object as a constant quantity
		sizing of the signal object, without risk management or
		position sizing considerations.
		Parameters:
		signal - The tuple containing Signal information.
		"""
		# TODO: Implement a risk system...
		order = None
		symbol = signal.symbol
		direction = signal.signal_type
		strength = signal.strength
		mkt_quantity = 100 # TODO: Here to change how much of the order we buy everytime...
		cur_quantity = self.current_positions[symbol]
		order_type = 'MKT'

		if direction == 'LONG' and cur_quantity == 0:
			order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
		if direction == 'SHORT' and cur_quantity == 0:
			order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')
		if direction == 'EXIT' and cur_quantity > 0:
			order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
		if direction == 'EXIT' and cur_quantity < 0:
			order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')

		self.event_history.append((direction, order))
		return order


	def update_signal(self, event):
		"""
		Acts on a SignalEvent to generate new orders
		based on the portfolio logic.
		"""
		if event.type == 'SIGNAL':
			order_event = self.generate_naive_order(event)
			self.events.put(order_event) # Put all the orders on the event queue...


	def create_equity_curve_dataframe(self):
		"""
		Creates a Pandas DataFrame from the all_holdings
		list of dictionaries.
		"""

		curve = pd.DataFrame(self.all_holdings)
		curve['datetime'] = curve['datetime'].apply(lambda t: t.replace(tzinfo=None)) # TODO: Need to figure out, but remove timezone for now
		curve.set_index('datetime', inplace=True)
		curve['returns'] = curve['total'].pct_change()
		curve['equity_curve'] = (1.0+curve['returns']).cumprod()
		self.equity_curve = curve[1:] # Skip first row.

	def output_summary_stats(self):
		"""
		Creates a list of summary statistics for the portfolio.
		"""

		total_return = self.equity_curve['equity_curve'][-1]
		returns = self.equity_curve['returns']
		pnl = self.equity_curve['equity_curve']
		# periods=252*60*6.5 for minuteley
		sharpe_ratio = create_sharpe_ratio(returns, periods=252)
		drawdown, max_dd, dd_duration = create_drawdowns(pnl)
		self.equity_curve['drawdown'] = drawdown
		'''
		stats = [
			(f"Total Return: {(total_return - 1.0) * 100.0:.2f}%"),
			(f"Sharpe Ratio: {sharpe_ratio:.2f}"),
			(f"Max Drawdown: {max_dd * 100.0:.2f}%"),
			(f"Drawdown Duration: {dd_duration:.2f}")
		]

			# Plot three charts: Equity curve,

		'''
		#plot_performance(self.equity_curve)
		self.equity_curve['returns'] = self.equity_curve['returns'].fillna(0).apply(lambda x: (x)*100.0).round(2)
		self.equity_curve['drawdown'] = self.equity_curve['drawdown'].fillna(0).apply(lambda x: (x)*100.0).round(2)
		#print(self.equity_curve.index.strftime('%Y-%m-%d'))
		#self.equity_curve.to_csv(’equity.csv’)
		return {
			'total_return': total_return,
			'sharpe_ratio': sharpe_ratio,
			'max_drawdown': max_dd,
			'drawdown_duration': dd_duration,
			'equity_curve': self.equity_curve,
		}

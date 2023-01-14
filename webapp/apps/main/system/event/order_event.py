from .event import Event

class OrderEvent(Event):
	"""
	Handles the event of sending an Order to an execution system.
	The order contains a symbol (e.g. GOOG), a type (market or limit),
	quantity and a direction.
	"""
	def __init__(self, symbol, order_type, quantity, direction):
		"""
		Initialises the order type, setting whether it is
		a Market order ('MKT') or Limit order ('LMT'), has
		a quantity (integral) and its direction ('BUY' or
		'SELL').
		Parameters:
			symbol - The instrument to trade.
			order_type - 'MKT’ or 'LMT' for Market or Limit.
			quantity - Non-negative integer for quantity.
			direction - 'BUY’ or 'SELL' for long or short.
		"""
		self.type = 'ORDER'
		self.symbol = symbol
		self.order_type = order_type
		self.quantity = self._check_set_quantity_positive(quantity)
		self.direction = direction

	def _check_set_quantity_positive(self, quantity):
		"""
		Checks that quantity is a positive integer.
		"""
		if not isinstance(quantity, int) or quantity <= 0:
			raise ValueError("Order event quantity is not a positive integer")
		return quantity

	def print_order(self):
		"""
		Outputs the values within the Order.
		"""
		print(f"Order: Symbol={self.symbol}, Type={self.order_type}, Quantity={self.quantity}, Direction={self.direction}")

	def __str__(self):
		return f"Order: Symbol={self.symbol}, Type={self.order_type}, Quantity={self.quantity}, Direction={self.direction}"

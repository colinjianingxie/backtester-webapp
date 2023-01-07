from datetime import datetime as dt

import pandas as pd

from sklearn.discriminant_analysis import (
	QuadraticDiscriminantAnalysis as QDA
)
from .strategy import Strategy
from main.system.event import SignalEvent
from main.pricing.helpers.lagged_series import create_lagged_series


class SPYDailyForecastStrategy(Strategy):
	"""
	S&P500 forecast strategy. It uses a Quadratic Discriminant Analyser to predict the returns for a
	subsequent time period and then generated long/exit signals based on the
	prediction.
	"""
	def __init__(self, bars, events, custom_parameters):
		self.bars = bars
		self.symbol_list = self.bars.symbol_list
		self.events = events
		self.datetime_now = dt.utcnow()
		self.model_start_date = custom_parameters['model']['start_date']#dt(2016,1,10)
		self.model_end_date = custom_parameters['model']['end_date'] #dt(2017,12,31)
		self.model_start_test_date = custom_parameters['model']['start_test_date']
		self.vendor_name = custom_parameters['data_handler']['vendor_name']
		self.long_market = False
		self.short_market = False
		self.bar_index = 0
		self.model = self.create_symbol_forecast_model()


	def create_symbol_forecast_model(self):
		# Create a lagged series of the S&P500 US stock market index

		snpret = create_lagged_series(
			[self.symbol_list[0]],
			self.model_start_date,
			self.model_end_date,
			lags=5,
			vendor_name=self.vendor_name
		)
		#snpret = create_lagged_series(ticker_name, start_date, end_date, lags=5, column_name='adj_close_price', additional_columns=['volume'], vendor_name='AlphaVantage')
		print(snpret)

		# Use the prior two days of returns as predictor
		# values, with direction as the response
		X = snpret[["Lag1","Lag2"]]
		y = snpret["Direction"]
		# Create training and test sets

		start_test = self.model_start_test_date
		X_train = X[X.index < start_test]
		X_test = X[X.index >= start_test]
		y_train = y[y.index < start_test]
		y_test = y[y.index >= start_test]

		model = QDA()
		model.fit(X_train, y_train)

		return model


	def calculate_signals(self, event):
		"""
		Calculate the SignalEvents based on market data.
		"""
		sym = self.symbol_list[0]
		cur_date = self.datetime_now

		if event.type == 'MARKET':
			self.bar_index += 1
			if self.bar_index > 5:
				lags = self.bars.get_latest_bars_values(self.symbol_list[0], "returns", N=3)
				pred_series = pd.Series(
				{
					'Lag1': lags[1]*100.0,
					'Lag2': lags[2]*100.0
				})

				pred_reshape = pred_series.values.reshape(1, -1)
				pred = self.model.predict(pred_reshape)
				if pred > 0 and not self.long_market:
					self.long_market = True
					signal = SignalEvent(1, sym, cur_date, 'LONG', 1.0)
					self.events.put(signal)
				if pred < 0 and self.long_market:
					self.long_market = False
					signal = SignalEvent(1, sym, cur_date, 'EXIT', 1.0)
					self.events.put(signal)

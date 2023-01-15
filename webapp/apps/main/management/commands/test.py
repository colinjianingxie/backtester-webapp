import os
from django.core.management.base import BaseCommand
from securities_master.helpers import get_daily_price_df
import pandas as pd
import numpy as np
from utils.helper.datetime_helper import trading_day_range

def bounded_random_walk(length, lower_bound,  upper_bound, start, end, std):
	assert (lower_bound <= start and lower_bound <= end)
	assert (start <= upper_bound and end <= upper_bound)

	bounds = upper_bound - lower_bound

	rand = (std * (np.random.random(length) - 0.5)).cumsum()
	rand_trend = np.linspace(rand[0], rand[-1], length)
	rand_deltas = (rand - rand_trend)
	rand_deltas /= np.max([1, (rand_deltas.max()-rand_deltas.min())/bounds])

	trend_line = np.linspace(start, end, length)
	upper_bound_delta = upper_bound - trend_line
	lower_bound_delta = lower_bound - trend_line

	upper_slips_mask = (rand_deltas-upper_bound_delta) >= 0
	upper_deltas =  rand_deltas - upper_bound_delta
	rand_deltas[upper_slips_mask] = (upper_bound_delta - upper_deltas)[upper_slips_mask]

	lower_slips_mask = (lower_bound_delta-rand_deltas) >= 0
	lower_deltas =  lower_bound_delta - rand_deltas
	rand_deltas[lower_slips_mask] = (lower_bound_delta + lower_deltas)[lower_slips_mask]

	return trend_line + rand_deltas

class Command(BaseCommand):
	"""
	Command that performs adf on ticker symbol
	"""

	help = ""


	def handle(self, *args, **options):
		print("HELLO")
		equity = "AMD"

		df = get_daily_price_df(equity)
		df_std = df['adj_close_price'].std()

		min_date = df.index[0]
		max_date = df.index[-1]
		print(df)
		print(df['open_price'].std())
		print(df['adj_close_price'].max())
		new_df = None

		for i in range(len(df[-10:])):
			a = pd.DataFrame()
			temp = trading_day_range(df.index[i], df.index[i], bday_freq='B', iday_freq='1T')
			number_points = len(temp)
			a['date']= temp

			lower = df['adj_close_price'][:i+1].min() - df_std
			upper = df['adj_close_price'][:i+1].max() + df_std
			randomData = bounded_random_walk(number_points, lower_bound=lower, upper_bound=upper, start=df.iloc[i]['open_price'], end=df.iloc[i]['adj_close_price'], std=10)
			a['price'] = pd.DataFrame(randomData)

			#print(a)
			if new_df is None:
				new_df = a
			else:
				new_df = new_df.append(a)
			#print(randomData)
			#print(df.iloc[i-1].index.values)
		#a = trading_day_range(min_date,max_date, bday_freq='B', iday_freq='1T')
		#print(len(a))
		#randomData = bounded_random_walk(390, lower_bound=50, upper_bound=100, start=50, end=100, std=10)
		#print(randomData)
		print(new_df)

import os
from django.core.management.base import BaseCommand
from securities_master.helpers import get_daily_price_df
import pandas as pd
from utils.helper.datetime_helper import trading_day_range


class Command(BaseCommand):
	"""
	Command that performs adf on ticker symbol
	"""

	help = ""


	def handle(self, *args, **options):
		print("HELLO")
		equity = "ZBRA"

		df = get_daily_price_df(equity)
		min_date = df.index[0]
		max_date = df.index[-1]

		print(df.index[0])
		print(df.index[-1])
		a = trading_day_range(min_date,max_date, bday_freq='B', iday_freq='1T')
		print(len(a))

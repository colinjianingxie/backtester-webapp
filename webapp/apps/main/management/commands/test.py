import os
from django.core.management.base import BaseCommand
from securities_master.helpers import get_minute_price_df

class Command(BaseCommand):
	"""
	Command that performs adf on ticker symbol
	"""

	help = ""


	def handle(self, *args, **options):
		equity = "AMD"

		df = get_minute_price_df(equity)
		print(df)

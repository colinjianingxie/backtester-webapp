import os
from django.core.management.base import BaseCommand

from main.models import Backtest
from oauth.models import Account
from main.models import Strategy

class Command(BaseCommand):
	"""
	Command that performs adf on ticker symbol
	"""

	help = ""


	def handle(self, *args, **options):
		symbol_list = ['AMD', 'INTC']
		curr_acc = Account.objects.all().filter(username="colinjianingxie").first()
		strategy_obj = Strategy.objects.all().filter(name="IntradayOLSMRStrategy").first()
		a = Backtest(
			account=curr_acc,
			name="test_pair_intra",
			symbol_list=symbol_list,
			initial_capital=100000.0,
			heartbeat=0.0,
			data_handler="HistoricHFTDataHandler",
			execution_handler="SimulatedExecutionHandler",
			portfolio="PortfolioHFT",
			strategy=strategy_obj,
			strategy_parameters={},
			data_start_date = "2020-01-01",
			data_end_date = "2023-01-01",
			portfolio_start_date = "2020-01-01",
		)
		response_data = a.perform_backtest(save_result=False)

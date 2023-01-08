import datetime
import os

from django.core.management.base import BaseCommand
from main.models import Backtest
from main.models import BacktestResults
from oauth.models import Account

class Command(BaseCommand):
    """
    Testing
    """

    help = "backtest"

    def handle(self, *args, **options):

        curr_acc = Account.objects.all().filter(username='colinjianingxie').first()


        strat_a = {
            'short_window': 100,
            'long_window': 400,
        }
        model_start_date = datetime.datetime.strptime('2016-01-10', "%Y-%m-%d")
        model_end_date = datetime.datetime.strptime('2017-12-31', "%Y-%m-%d")
        model_start_test_date = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d")
        strat_b = {
            'start_date': model_start_date,
            'end_date': model_end_date,
            'start_test_date': model_start_test_date,
        }

        start_date = datetime.datetime.strptime('1998-01-02', "%Y-%m-%d")
        end_date = datetime.datetime.strptime('2018-01-31', "%Y-%m-%d")
        portfolio_start_date = datetime.datetime.strptime('2017-01-03', "%Y-%m-%d")


        a = Backtest(
            account=curr_acc,
            name="Test_bt",
            symbol_list=['XEL'],
            initial_capital=100000.00,
            heartbeat=0.0,
            data_handler="HistoricDataHandler",
            execution_handler="SimulatedExecutionHandler",
            portfolio="Portfolio",
            strategy="SPYDailyForecastStrategy",
            strategy_parameters=strat_b,
            data_start_date = start_date,
            data_end_date = end_date,
            portfolio_start_date = portfolio_start_date,
        )

        print(a)
        a.perform_backtest()

import datetime
import os

from django.core.management.base import BaseCommand
from main.models import Backtest
from main.models import BacktestResults
from main.pricing.helpers.basic_input import call_basic_security_input
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.var import perform_var
from main.system.backtest import Backtest as bt
from main.system.data_handler import HistoricDataHandler
from main.system.execution_handler import SimulatedExecutionHandler
from main.system.portfolio import HFTPortfolio
from main.system.portfolio import Portfolio
from main.system.strategy import MovingAverageCrossStrategy
from main.system.strategy import SPYDailyForecastStrategy
#from main.pricing.helpers.lagged_series import create_lagged_series
#from main.pricing.confusion_matrix import generate_confusion_matrix


class Command(BaseCommand):
    """
    Testing
    """

    help = "backtest"
    def create_model_parameters(self, model_name):
        if model_name == 'SPYDailyForecastStrategy':

            model_start_date = '2016-01-10'
            model_end_date = '2017-12-31'
            model_start_test_date = '2017-01-01'
            model_start_date = datetime.datetime.strptime(model_start_date, "%Y-%m-%d")
            model_end_date = datetime.datetime.strptime(model_end_date, "%Y-%m-%d")
            model_start_test_date = datetime.datetime.strptime(model_start_test_date, "%Y-%m-%d")

            return {
                'start_date': model_start_date,
                'end_date': model_end_date,
                'start_test_date': model_start_test_date,
            }
        elif model_name == 'MovingAverageCrossStrategy':
            return {
                'short_window': 100,
                'long_window': 400,
            }
    def create_parameters(self, model_name):

        start_date = '1998-01-02'
        end_date = '2018-01-31'
        portfolio_start_date = '2017-01-03'

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        portfolio_start_date = datetime.datetime.strptime(portfolio_start_date, "%Y-%m-%d")

        return {
            'portfolio': {
                'start_date': portfolio_start_date,
            },
            'data_handler': {
                'start_date': start_date,
                'end_date': end_date,
                'vendor_name': 'Yahoo Finance'
            },
            'model': self.create_model_parameters(model_name)
        }
    def handle(self, *args, **options):
        #ticker_names, start_date, end_date = call_basic_security_input()
        ticker_names=['SPY']


        #daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date, quick_extract=True, vendor_name="Yahoo Finance")
        initial_capital = 100000.0
        heartbeat = 0.0
        #symbol_list, initial_capital, heartbeat, start_date, end_date, data_handler, execution_handler, portfolio, strategy, csv_dir=None
        model_parameters = self.create_parameters(SPYDailyForecastStrategy.__name__)
        backtest = bt(
            symbol_list=ticker_names,
            initial_capital=initial_capital,
            heartbeat=heartbeat,
            data_handler=HistoricDataHandler,
            execution_handler=SimulatedExecutionHandler,
            portfolio=Portfolio,
            strategy=SPYDailyForecastStrategy,
            custom_parameters=model_parameters
        )


        backtest.simulate_trading()

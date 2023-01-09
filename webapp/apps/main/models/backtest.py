import datetime
import json
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.duration import duration_string
from jsonfield import JSONField
from main.system.backtest import Backtest as bt
from main.system.data_handler import HistoricDataHandler
from main.system.execution_handler import SimulatedExecutionHandler
from main.system.portfolio import Portfolio
from main.system.strategy import MovingAverageCrossStrategy
from main.system.strategy import SPYDailyForecastStrategy
from oauth.models.user_model import Account
# Functions for actual backtesting

class Backtest(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    symbol_list = ArrayField(models.CharField(max_length=10, blank=True), size=15)
    initial_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    heartbeat = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    data_handler = models.CharField(max_length=200)
    execution_handler = models.CharField(max_length=200)
    portfolio = models.CharField(max_length=200)
    strategy = models.CharField(max_length=200)
    strategy_parameters = JSONField(default={})
    data_start_date = models.DateTimeField("data start date")
    data_end_date = models.DateTimeField("data end date")
    portfolio_start_date = models.DateTimeField("portfolio start date")
    created_date = models.DateTimeField("created date", auto_now_add=True)

    def create_backtest_parameters(self):

        return {
            'portfolio': {
                'start_date': self.portfolio_start_date,
            },
            'data_handler': {
                'start_date': self.data_start_date,
                'end_date': self.data_end_date,
                'vendor_name': 'Yahoo Finance'
            },
            'model': self.strategy_parameters
        }

    def get_data_handler(self):
        if self.data_handler == "HistoricDataHandler":
            return HistoricDataHandler

    def get_execution_handler(self):
        if self.execution_handler == "SimulatedExecutionHandler":
            return SimulatedExecutionHandler

    def get_strategy(self):
        if self.strategy == 'SPYDailyForecastStrategy':
            return SPYDailyForecastStrategy

        elif self.strategy == 'MovingAverageCrossStrategy':
            return MovingAverageCrossStrategy

    def create_backtest(self):
        backtest = bt(
            symbol_list=self.symbol_list,
            initial_capital=float(self.initial_capital),
            heartbeat=float(self.heartbeat),
            data_handler=self.get_data_handler(),
            execution_handler=self.get_execution_handler(),
            portfolio=Portfolio,
            strategy=self.get_strategy(),
            custom_parameters=self.create_backtest_parameters(),
        )
        return backtest

    def perform_backtest(self):
        backtest = self.create_backtest()
        start_simulation_time=datetime.datetime.now()
        results = backtest.simulate_trading()
        end_simulation_time=datetime.datetime.now()
        duration = end_simulation_time - start_simulation_time
        stats = results['stats']

        backtest_result = BacktestResult(
            backtest=self,
            total_return=stats['total_return'],
            sharpe_ratio=stats['sharpe_ratio'],
            max_drawdown=stats['max_drawdown'],
            drawdown_duration=stats['drawdown_duration'],
            signals = stats['signals'],
            orders = stats['orders'],
            fills = stats['fills'],
            status="SUCCESS",
            start_simulation_time=start_simulation_time,
            end_simulation_time=end_simulation_time,
            duration=duration
            )

        backtest_result.save()

        response_data = {
            'backtest_id': str(self.id),
            'backtest_result_id': str(backtest_result.id),
        }

        return response_data

    def __str__(self):
        return f"{self.id}"

class BacktestResult(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE)
    events = JSONField(default={})
    total_return = models.DecimalField(max_digits=8, decimal_places=2)
    sharpe_ratio = models.DecimalField(max_digits=8, decimal_places=2)
    max_drawdown = models.DecimalField(max_digits=8, decimal_places=2)
    drawdown_duration = models.DecimalField(max_digits=8, decimal_places=2)
    signals = models.IntegerField()
    orders = models.IntegerField()
    fills = models.IntegerField()
    status = models.CharField(max_length=200)
    start_simulation_time = models.DateTimeField("start_simulation_time")
    end_simulation_time = models.DateTimeField("end_simulation_time")
    duration = models.DurationField()
    created_date = models.DateTimeField("created date", auto_now_add=True)

    @property
    def display_duration(self):
        total_ms = self.duration.total_seconds() * 1000.0
        return f"{total_ms:.2f}"

    @property
    def portfolio_balance_return(self):
        return float(self.backtest.initial_capital) * (1.0 + float(self.total_return)/100.0)

    @property
    def display_portfolio_profit(self):
        starting_capital = float(self.backtest.initial_capital)
        profit = self.portfolio_balance_return - starting_capital
        return f"{profit:.2f}"

    @property
    def display_portfolio_return(self):
        return f"{self.portfolio_balance_return:.2f}"

    def __str__(self):
        return f"{self.id}"

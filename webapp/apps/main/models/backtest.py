import datetime
import json
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
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
            result=stats,
            status="SUCCESS",
            start_simulation_time=start_simulation_time,
            end_simulation_time=end_simulation_time,
            duration=duration
            )
        backtest_result.save()

    def __str__(self):
        return f"{self.id}"

class BacktestResult(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE)
    result = JSONField(default={})
    status = models.CharField(max_length=200)
    start_simulation_time = models.DateTimeField("start_simulation_time")
    end_simulation_time = models.DateTimeField("end_simulation_time")
    duration = models.DurationField()
    created_date = models.DateTimeField("created date", auto_now_add=True)


    def __str__(self):
        return f"{self.id}"

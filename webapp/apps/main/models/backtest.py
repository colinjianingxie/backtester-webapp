import datetime
import json
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.duration import duration_string
from jsonfield import JSONField
from main.models.strategy import Strategy
from main.system.backtest import Backtest as bt
from main.system.data_handler import HistoricDataHandler
from main.system.data_handler import HistoricHFTDataHandler
from main.system.execution_handler import SimulatedExecutionHandler
from main.system.portfolio import Portfolio
from main.system.portfolio import PortfolioHFT
from main.system.strategy.default.intraday_mr import IntradayOLSMRStrategy
from main.system.strategy.default.ml_forecast import MLForecast
from main.system.strategy.default.moving_average_crossover import MovingAverageCrossover
from oauth.models.user_model import Account
from securities_master.models import Symbol
# Functions for actual backtesting

class Backtest(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    symbol_list = models.ManyToManyField(Symbol, related_name='symbol_list', blank=True)
    initial_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
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

    @property
    def get_data_handler(self):
        if self.strategy.use_hft:
            return HistoricHFTDataHandler
        return HistoricDataHandler

    @property
    def get_execution_handler(self):
        return SimulatedExecutionHandler

    @property
    def get_strategy(self):
        if self.strategy.name == 'MLForecast':
            return MLForecast
        elif self.strategy.name == 'MovingAverageCrossover':
            return MovingAverageCrossover
        elif self.strategy.name == 'IntradayOLSMRStrategy':
            return IntradayOLSMRStrategy

    @property
    def get_portfolio(self):
        if self.strategy.use_hft:
            return PortfolioHFT
        return Portfolio

    @property
    def get_ticker_list(self):
        return [t.ticker for t in self.symbol_list.all()]

    def create_backtest(self):
        backtest = bt(
            symbol_list=self.get_ticker_list,
            initial_capital=float(self.initial_capital),
            heartbeat=0.0,
            data_handler=self.get_data_handler,
            execution_handler=self.get_execution_handler,
            portfolio=self.get_portfolio,
            strategy=self.get_strategy,
            custom_parameters=self.create_backtest_parameters(),
        )
        return backtest

    def perform_backtest(self, save_result=True):
        backtest = self.create_backtest()
        start_simulation_time=datetime.datetime.now()
        results = backtest.simulate_trading()
        end_simulation_time=datetime.datetime.now()
        duration = end_simulation_time - start_simulation_time
        stats = results['stats']
        equity_curve = stats['equity_curve']
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
            graph_indexes = equity_curve.index.strftime("%Y-%m-%d").tolist(),
            graph_returns = equity_curve['returns'].tolist(),
            graph_drawdowns = equity_curve['drawdown'].tolist(),
            graph_portfolio_values = equity_curve['equity_curve'].fillna(0).round(3).tolist(),
            end_simulation_time=end_simulation_time,
            duration=duration
            )

        if save_result:
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
    graph_indexes = ArrayField(models.CharField(max_length=10, blank=True))
    graph_returns = ArrayField(models.DecimalField(max_digits=10, decimal_places=3))
    graph_drawdowns = ArrayField(models.DecimalField(max_digits=10, decimal_places=3))
    graph_portfolio_values = ArrayField(models.DecimalField(max_digits=15, decimal_places=3))
    created_date = models.DateTimeField("created date", auto_now_add=True)


    @property
    def result_returns_coordinates(self):
        return [{"x": x, "y": float(y)} for x, y in zip(self.graph_indexes, self.graph_returns)]

    @property
    def result_drawdowns_coordinates(self):
        return [{"x": x, "y": float(y)} for x, y in zip(self.graph_indexes, self.graph_drawdowns)]

    @property
    def result_values_coordinates(self):
        return [{"x": x, "y": float(y)} for x, y in zip(self.graph_indexes, self.graph_portfolio_values)]

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

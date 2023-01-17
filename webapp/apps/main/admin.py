from django.contrib import admin
from main.models import Backtest
from main.models import BacktestResult
from main.models import Strategy

class BacktestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "name",
        "symbol_list",
        "initial_capital",
        "heartbeat",
        "strategy",
        "strategy_parameters",
        "data_start_date",
        "data_end_date",
        "portfolio_start_date",
        "created_date",
    )  # What to display as columns in
    search_fields = ("id",)
    readonly_fields = (
        "id",
        "account",
        "name",
        "symbol_list",
        "initial_capital",
        "heartbeat",
        "strategy",
        "strategy_parameters",
        "data_start_date",
        "data_end_date",
        "portfolio_start_date",
        "created_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class BacktestResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "backtest",
        "total_return",
        "sharpe_ratio",
        "max_drawdown",
        "drawdown_duration",
        "signals",
        "orders",
        "fills",
        "status",
        "start_simulation_time",
        "end_simulation_time",
        "duration",
        "created_date",
    )  # What to display as columns in
    search_fields = (
    "id",
    )
    readonly_fields = (
        "id",
        "backtest",
        "status",
        "start_simulation_time",
        "end_simulation_time",
        "duration",
        "created_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class StrategyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "name",
        "strategy_parameters",
        "strategy_defaults",
        "strategy_min",
        "strategy_max",
        "number_stocks",
        "use_ml",
    )  # What to display as columns in
    search_fields = (
    "id",
    )
    readonly_fields = (
        "id",
        "account",
        "name",
        "strategy_parameters",
        "use_ml",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Backtest, BacktestAdmin)
admin.site.register(BacktestResult, BacktestResultAdmin)
admin.site.register(Strategy, StrategyAdmin)

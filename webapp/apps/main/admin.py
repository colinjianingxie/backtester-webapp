from django.contrib import admin
from main.models import Backtest
from main.models import BacktestResult

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
        "result",
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
        "result",
        "status",
        "start_simulation_time",
        "end_simulation_time",
        "duration",
        "created_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Backtest, BacktestAdmin)
admin.site.register(BacktestResult, BacktestResultAdmin)

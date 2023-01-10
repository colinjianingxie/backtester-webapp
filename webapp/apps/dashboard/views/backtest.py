from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Backtest
from main.models import BacktestResult
from oauth.constants import UserGroup
from securities_master.helpers.daily_prices import get_daily_price_df
from securities_master.models import DailyPrice
# User Access
# Helpers

class BacktestView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "apps/dashboard/backtest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        default_random_dp = DailyPrice.objects.all().order_by('-price_date').first()

        df = get_daily_price_df(default_random_dp.symbol.ticker)
        res = [{
            'date': index.strftime("%Y-%m-%d"),
            'high': row['high_price'],
            'low': row['low_price'],
            'close': row['close_price'],
            'adj_close': row['adj_close_price'],
            'volume': row['volume'],
            'open': row['open_price']} for index, row in df.iterrows()]


        context['backtest_selected_stock_0'] = default_random_dp
        context['backtest_daily_price'] = res
        return context


class BacktestResultsView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "apps/dashboard/backtest_results.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        results = self.get_backtest_result(context)

        context['backtest_results'] = results

        return context

    def get_backtest_result(self, context):
        backtest_id = context.get('backtest_id', None)
        backtest_result_id = context.get('backtest_result_id', None)
        if backtest_id and backtest_result_id:
            # TODO: Check if backtest result actually exists
            return BacktestResult.objects.all().filter(id=backtest_result_id,backtest__id=backtest_id)
        elif backtest_id and not backtest_result_id:
            return BacktestResult.objects.all().filter(backtest__id=backtest_id)

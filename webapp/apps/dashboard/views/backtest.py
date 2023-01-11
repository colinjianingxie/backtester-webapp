from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Backtest
from main.models import BacktestResult
from main.models import Strategy
from oauth.constants import UserGroup
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

        default_strategies = Strategy.objects.all()
        context['backtest_selected_stock_0'] = default_random_dp
        context['backtest_default_strategy'] = default_strategies.first()
        context['default_strategies'] = default_strategies
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

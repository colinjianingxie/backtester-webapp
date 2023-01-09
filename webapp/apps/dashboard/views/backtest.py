from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Backtest
from main.models import BacktestResult
from oauth.constants import UserGroup
# User Access
# Helpers

class BacktestView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "backtest.html"

class BacktestResultsView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "backtest_results.html"


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

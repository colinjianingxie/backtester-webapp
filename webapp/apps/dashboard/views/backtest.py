from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Backtest
from main.models import BacktestResults
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

        result = self.get_backtest_result(context)

        context['backtest_result'] = result

        return context

    def get_backtest_result(self, context):
        backtest_id = context.get('id', None)
        if backtest_id:
            # TODO: Check if backtest result actually exists
            found_result = BacktestResults.objects.all().filter(backtest__id=backtest_id).first()
            return found_result

from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Backtest
from main.models import BacktestResult
from oauth.constants import UserGroup
# User Access
# Helpers

class BacktestHistoryView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "apps/dashboard/backtest_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_backtest_results = BacktestResult.objects.all().filter(backtest__account=self.request.user).order_by('-created_date')

        context['backtest_results'] = user_backtest_results
        return context

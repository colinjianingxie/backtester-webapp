from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from oauth.constants import UserGroup
# User Access
# Helpers

class BacktestView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "backtest.html"

import json

from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from oauth.constants import UserGroup
from securities_master.helpers.daily_prices import get_daily_price_df
# User Access
# Helpers

class DisplayDailyPriceView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "display_price.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ticker = context['ticker']

        return context

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
        df = get_daily_price_df(ticker)
        res = [{
            'date': index.strftime("%Y-%m-%d"),
            'high': row['high_price'],
            'low': row['low_price'],
            'close': row['close_price'],
            'adj_close': row['adj_close_price'],
            'volume': row['volume'],
            'open': row['open_price']} for index, row in df.iterrows()]

        context[f'display_daily_price'] = res

        return context

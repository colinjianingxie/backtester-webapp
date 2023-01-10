import datetime
import json

from api.views.helper import api_response
from api.views.helper import ResponseStatus
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from securities_master.helpers.daily_prices import get_daily_price_df
from securities_master.models import DailyPrice
from securities_master.models import Symbol
#from utils.helper import api_response
#TODO: Possible race condition of sending requests at same time...

class BacktestDailyPriceView(APIView):
    """
    """
    def post(self, request):

        ticker = request.POST['ticker']
        context = self.context_daily_price_helper(ticker)
        return render(request, "apps/dashboard/components/backtest/stock_selection.html", context)

    def context_daily_price_helper(self, ticker):
        context = {}
        latest_price = DailyPrice.objects.all().filter(symbol__ticker=ticker).order_by('-price_date').first()
        context["backtest_selected_stock_0"] = latest_price
        return context

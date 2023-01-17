import datetime
import json

from api.views.helper import api_response
from api.views.helper import ResponseStatus
from django.shortcuts import render
from main.models import Strategy
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

        tickers = json.loads(request.POST['tickers'])
        strategy = request.POST['strategy']
        context = self.context_daily_price_helper(tickers, strategy)
        return render(request, "apps/dashboard/components/backtest/backtest_parameters.html", context)

    def context_daily_price_helper(self, tickers, strategy):
        context = {}
        context['selected_stocks'] = {}
        selected_strategy = Strategy.objects.all().filter(name=strategy).first()
        context["backtest_selected_strategy"] = selected_strategy
        for i in range(len(tickers)):
            curr_symb = Symbol.objects.all().filter(ticker=tickers[i]).first()
            context[f"selected_stocks"][i] = curr_symb


        return context

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

        tickers = request.POST['tickers']
        context = self.context_daily_price_helper(tickers)
        return render(request, "apps/dashboard/components/backtest/backtest_parameters.html", context)

    def context_daily_price_helper(self, tickers):
        context = {}
        '''
        context['selected_stocks'] = {}
        Symbol.objects.filter(ticker=ticker).first()
        for i in backtest_selected_strategy.number_stocks_range:
            curr_symb = distinct_symbols[i]
            curr_dp = DailyPrice.objects.all().filter(symbol=curr_symb).order_by('-price_date').first()
            context[f"selected_stocks"][i] = curr_symb

        latest_price = DailyPrice.objects.all().filter(symbol__ticker=ticker).order_by('-price_date').first()
        context["backtest_selected_stock_0"] = latest_price
        '''
        return context

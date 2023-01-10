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

class PostBacktestDailyPriceView(APIView):
    """
    """

    def post(self, request):

        ticker = request.POST['ticker']
        context = self.context_daily_price_helper(ticker)
        return render(request, "apps/dashboard/components/backtest/stock_selection.html", context)

    def context_daily_price_helper(self, ticker):
        context = {}
        latest_price = DailyPrice.objects.all().filter(symbol__ticker=ticker).order_by('-price_date').first()
        df = get_daily_price_df(ticker)
        res = [{
            'date': index.strftime("%Y-%m-%d"),
            'high': row['high_price'],
            'low': row['low_price'],
            'close': row['close_price'],
            'adj_close': row['adj_close_price'],
            'volume': row['volume'],
            'open': row['open_price']} for index, row in df.iterrows()]

        context["backtest_selected_stock_0"] = latest_price
        context['backtest_daily_price'] = res

        return context

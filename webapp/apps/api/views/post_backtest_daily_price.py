import datetime
import json

from api.views.helper import api_response
from api.views.helper import ResponseStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from securities_master.models import Symbol
#from utils.helper import api_response
#TODO: Possible race condition of sending requests at same time...

class PostBacktestDailyPriceView(APIView):
    """
    """

    def post(self, request):
        ticker = request.POST['ticker']

        response_data = self.post_daily_price_helper(
        )
        return Response(response_data)

    def post_daily_price_helper(self, ticker):
        try:
            symbol = Symbol.objects.get(ticker=ticker)
        except Backtest.DoesNotExist:
            return api_response(
                type='backtest',
                view='post_backtest_daily_price',
                status=ResponseStatus.FAIL.value,
                message=f'Unable to find symbol',
            )

        return api_response(
            type='backtest',
            view='post_backtest_daily_price',
            status=ResponseStatus.SUCCESS.value,
            message=f'successfully performed backtest',
        )

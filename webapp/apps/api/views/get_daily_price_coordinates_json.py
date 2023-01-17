import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from securities_master.helpers.daily_prices import get_daily_price_df

class GetDailyPriceCoordinatesJSONView(APIView):
    """Verifies that the server is running"""
    def get(self, request, ticker):
        content = {}

        price_df = self.get_prices(ticker, request)
        content['data'] = {
            'name': ticker,
            'data': price_df
        }
        return Response(content)

    def get_prices(self, ticker, request):

        price_df = get_daily_price_df(ticker)

        res = [
        {
            'x': index.strftime("%Y-%m-%d"),
            'y': [{row["open_price"]}, {row["high_price"]}, {row["low_price"]}, {row["close_price"]}]
        } for index, row in price_df.iterrows()]

        return res

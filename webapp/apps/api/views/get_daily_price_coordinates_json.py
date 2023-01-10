import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from securities_master.helpers.daily_prices import get_daily_price_df

class GetDailyPriceCoordinatesJSONView(APIView):
    """Verifies that the server is running"""
    def get(self, request, ticker):
        content = {}
        price_df = self.get_prices(ticker, request)
        content['data'] = price_df
        return Response(content)

    def get_prices(self, ticker, request):
        # TODO: Need better date handling
        start_date = request.GET.get('start', "2019-01-01")
        end_date = request.GET.get('end', "2019-01-10")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        vendor_name = "Yahoo Finance"
        price_df = get_daily_price_df(ticker)

        res = [
        {
            'x': index.strftime("%Y-%m-%d"),
            'y': [{row["open_price"]}, {row["high_price"]}, {row["low_price"]}, {row["close_price"]}]
        } for index, row in price_df.iterrows()]

        return res

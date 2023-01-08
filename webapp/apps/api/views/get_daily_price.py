import datetime

from main.pricing.helpers.get_daily_prices import get_daily_prices as gdp
from rest_framework.response import Response
from rest_framework.views import APIView

class GetDailyPriceView(APIView):
    """Verifies that the server is running"""
    def get(self, request, ticker):
        content = {'message': 'Server is running!'}
        price_df = self.get_price(ticker, request)
        return Response(price_df)

    def get_price(self, ticker, request):
        # TODO: Need better date handling
        start_date = request.GET.get('start', "2019-01-01")
        end_date = request.GET.get('end', "2019-01-10")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        vendor_name = "Yahoo Finance"
        return gdp([ticker], start_date, end_date, quick_extract=False, vendor_name=vendor_name)

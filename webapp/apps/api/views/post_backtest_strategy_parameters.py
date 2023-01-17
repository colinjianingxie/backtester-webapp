from api.views.helper import api_response
from api.views.helper import ResponseStatus
from django.shortcuts import render
from main.models import Strategy
from rest_framework.response import Response
from rest_framework.views import APIView
from securities_master.models import DailyPrice
from securities_master.models import Symbol

class PostBacktestStrategyParametersView(APIView):
    """
    """
    def post(self, request):

        strategy = request.POST['strategy']
        context = self.strategy_parameter_helper(strategy)
        return render(request, "apps/dashboard/components/backtest/backtest_parameters.html", context)

    def strategy_parameter_helper(self, strategy):
        context = {}
        backtest_selected_strategy = Strategy.objects.all().filter(name=strategy).first()

        distinct_symbol_ids = [dpid['symbol_id'] for dpid in DailyPrice.objects.values('symbol_id').distinct()]
        distinct_symbols = Symbol.objects.filter(id__in=distinct_symbol_ids)
        context['selected_stocks'] = {}
        for i in backtest_selected_strategy.number_stocks_range:
            curr_symb = distinct_symbols[i]
            curr_dp = DailyPrice.objects.all().filter(symbol=curr_symb).order_by('-price_date').first()
            context[f"selected_stocks"][i] = curr_symb

        context["backtest_selected_strategy"] = backtest_selected_strategy
        return context

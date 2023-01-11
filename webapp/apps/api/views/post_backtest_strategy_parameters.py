from api.views.helper import api_response
from api.views.helper import ResponseStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Strategy
from django.shortcuts import render

class PostBacktestStrategyParametersView(APIView):
    """
    """
    def post(self, request):

        strategy = request.POST['strategy']
        context = self.strategy_parameter_helper(strategy)
        return render(request, "partials/dashboard/components/cards/strategy_parameter_cards/default_card.html", context)

    def strategy_parameter_helper(self, strategy):
        context = {}
        backtest_default_strategy = Strategy.objects.all().filter(name=strategy).first()
        context["backtest_default_strategy"] = backtest_default_strategy
        return context

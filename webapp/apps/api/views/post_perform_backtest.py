import datetime
import json

from api.views.helper import api_response
from api.views.helper import ResponseStatus
from main.models import Backtest
from rest_framework.response import Response
from rest_framework.views import APIView
#from utils.helper import api_response
#TODO: Possible race condition of sending requests at same time...

class PostPerformBacktestView(APIView):
    """
    """

    def post(self, request):
        name = request.POST['name']
        symbol_list = request.POST['symbol_list']
        initial_capital = request.POST['initial_capital']
        heartbeat = request.POST['heartbeat']
        data_handler = request.POST['data_handler']
        execution_handler = request.POST['execution_handler']
        portfolio = request.POST['portfolio']
        strategy = request.POST['strategy']
        strategy_parameters = request.POST['strategy_parameters']
        data_start_date = request.POST['data_start_date']
        data_end_date = request.POST['data_end_date']
        portfolio_start_date = request.POST['portfolio_start_date']

        response_data = self.perform_backtest_helper(
            request,
            name,
            symbol_list,
            initial_capital,
            heartbeat,
            data_handler,
            execution_handler,
            portfolio,
            strategy,
            strategy_parameters,
            data_start_date,
            data_end_date,
            portfolio_start_date,
        )
        return Response(response_data)

    def perform_backtest_helper(self,
        request,
        name,
        symbol_list,
        initial_capital,
        heartbeat,
        data_handler,
        execution_handler,
        portfolio,
        strategy,
        strategy_parameters,
        data_start_date,
        data_end_date,
        portfolio_start_date):

        symbol_list = json.loads(symbol_list)
        strategy_parameters = json.loads(strategy_parameters)
        data_start_date = datetime.datetime.strptime(data_start_date, "%Y-%m-%d")
        data_end_date = datetime.datetime.strptime(data_end_date, "%Y-%m-%d")
        portfolio_start_date = datetime.datetime.strptime(portfolio_start_date, "%Y-%m-%d")


        try:
            backtest = Backtest.objects.get(
                account=request.user,
                name=name,
                symbol_list=symbol_list,
                initial_capital=initial_capital,
                heartbeat=heartbeat,
                data_handler=data_handler,
                execution_handler=execution_handler,
                portfolio=portfolio,
                strategy=strategy,
                strategy_parameters=strategy_parameters,
                data_start_date = data_start_date,
                data_end_date = data_end_date,
                portfolio_start_date = portfolio_start_date,
            )
        except Backtest.DoesNotExist:
            backtest = Backtest(
                account=request.user,
                name=name,
                symbol_list=symbol_list,
                initial_capital=initial_capital,
                heartbeat=heartbeat,
                data_handler=data_handler,
                execution_handler=execution_handler,
                portfolio=portfolio,
                strategy=strategy,
                strategy_parameters=strategy_parameters,
                data_start_date = data_start_date,
                data_end_date = data_end_date,
                portfolio_start_date = portfolio_start_date,
            )
            backtest.save()

        backtest_ids = backtest.perform_backtest()

        return api_response(
            type='backtest',
            view='post_perform_backtest',
            status=ResponseStatus.SUCCESS.value,
            message=f'successfully performed backtest',
            data=backtest_ids
        )

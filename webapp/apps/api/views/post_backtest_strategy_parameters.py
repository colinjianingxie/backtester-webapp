from api.views.helper import api_response
from api.views.helper import ResponseStatus
from rest_framework.response import Response
from rest_framework.views import APIView

class PostBacktestStrategyParametersView(APIView):
    """
    """
    def post(self, request):

        strategy = request.POST['strategy']
        context = self.strategy_parameter_helper(strategy)
        return render(request, "partials/dashboard/components/modals/paramater_select_modal/modal.html", context)

    def strategy_parameter_helper(self, strategy):
        context = {}

        return context

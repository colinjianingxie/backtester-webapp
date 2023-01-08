from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
#from oauth.models import AnalysisSettings
#from technical_analysis.models import Stock
#from technical_analysis.models import StockData
#from technical_analysis.models import TechnicalFunctionOption
#from technical_analysis.structures.charts import ApexChart
#from technical_analysis.structures.charts import LineChartOptions
#from technical_analysis.structures.functions import TechnicalFunction
from oauth.constants import UserGroup
#from utils.helper.model_helper import get_current_account
#from utils.helper.model_helper import get_field_list
# User Access
# Models
# Functions
# Charts
# Helpers

class AnalysisView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "analysis.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        analysis_id = kwargs['analysis_id'] if 'analysis_id' in kwargs else 'none'
        function_list = []
        data = []

        if analysis_id != 'none':
            chosen_analysis = AnalysisSettings.objects.filter(id=analysis_id).first()
            selected_tickers = get_field_list(chosen_analysis.selected_tickers)
            selected_functions= get_field_list(chosen_analysis.selected_functions)
            number_trends = chosen_analysis.number_trends
            for i in range(number_trends):
                data = StockData.objects.all().filter(stock__ticker=selected_tickers[i])
                function = TechnicalFunctionOption.objects.all().filter(name=selected_functions[i]).first()
                function_list.append(function.function(input_data=data, color=Color.RED.value))

        # Generates the chart.
        context['line_chart'] = ApexChart(html_id='#line_chart_dashed', options=LineChartOptions(function_list))
        '''

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

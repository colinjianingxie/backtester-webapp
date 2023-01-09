from django.urls import path

from .views import BacktestResultsView
from .views import BacktestView
from .views import DashboardView
from .views import portal_redirect

urlpatterns = [
    ################################################
    #   Main Redirection
    ################################################
    path("login_redirect_success/",portal_redirect.login_redirect_success,name="login_redirect_success"),
    path('', DashboardView.as_view(), name='dashboard'),
    #path('analysis_settings/', analysis_settings.AnalysisSettingsView.as_view(), name='analysis_settings'),
    #path('analysis/analysis_id=<str:analysis_id>', analysis.AnalysisView.as_view(), name='analysis'),
    #path('analysis/', analysis.AnalysisView.as_view(), name='analysis_redirect'),
    path('backtest/', BacktestView.as_view(), name='backtest'),
    path('backtest_result/<str:id>', BacktestResultsView.as_view(), name='backtest_result'), # Need ID for backtest results
]

from django.urls import path

from .views import BacktestHistoryView
from .views import BacktestResultsView
from .views import BacktestView
from .views import DashboardView
from .views import ExploreView
from .views import ForumView
from .views import portal_redirect

urlpatterns = [
    ################################################
    #   Main Redirection
    ################################################
    path("login_redirect_success/",portal_redirect.login_redirect_success,name="login_redirect_success"),
    path('', DashboardView.as_view(), name='dashboard'),
    path('forum/', ForumView.as_view(), name='forum'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('backtest/', BacktestView.as_view(), name='backtest'),
    path('backtest_history/', BacktestHistoryView.as_view(), name='backtest_history'),
    path('backtest_result/<str:backtest_id>/<str:backtest_result_id>', BacktestResultsView.as_view(), name='backtest_result'), # Need ID for backtest results
]

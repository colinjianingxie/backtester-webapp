from django.urls import path

from .views import GetDailyPriceView
from .views import PostPerformBacktestView

urlpatterns = [
    path('get_daily_price/<str:ticker>/', GetDailyPriceView.as_view(), name='get_daily_price'),
    path('perform_backtest/', PostPerformBacktestView.as_view(), name='perform_backtest'),
]
from django.urls import path

from .views import BacktestDailyPriceView
from .views import GetDailyPriceCoordinatesJSONView
from .views import GetDailyPriceView
from .views import PostPerformBacktestView
urlpatterns = [
    path('get_daily_price/<str:ticker>/', GetDailyPriceView.as_view(), name='get_daily_price'),
    path('get_daily_price_coordinates_json/<str:ticker>/', GetDailyPriceCoordinatesJSONView.as_view(), name='get_daily_price_coordinates_json'),
    path('perform_backtest/', PostPerformBacktestView.as_view(), name='perform_backtest'),
    path('backtest_daily_price/', BacktestDailyPriceView.as_view(), name='backtest_daily_price'),
]

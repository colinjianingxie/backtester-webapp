from django.urls import path

from .views import GetDailyPriceView

urlpatterns = [
    path('get_daily_price/<str:ticker>/', GetDailyPriceView.as_view(), name='get_daily_price'),
]

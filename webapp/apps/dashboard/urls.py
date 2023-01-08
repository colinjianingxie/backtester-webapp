from django.urls import path

from .views import analysis
from .views import dashboard
from .views import portal_redirect

urlpatterns = [
    ################################################
    #   Main Redirection
    ################################################
    path("login_redirect_success/",portal_redirect.login_redirect_success,name="login_redirect_success"),
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    #path('analysis_settings/', analysis_settings.AnalysisSettingsView.as_view(), name='analysis_settings'),
    #path('analysis/analysis_id=<str:analysis_id>', analysis.AnalysisView.as_view(), name='analysis'),
    #path('analysis/', analysis.AnalysisView.as_view(), name='analysis_redirect'),
    path('backtests/', dashboard.DashboardView.as_view(), name='backtests'),
]

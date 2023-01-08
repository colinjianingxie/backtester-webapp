from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.views.generic import TemplateView
#from oauth.models import AnalysisSettings
from oauth.constants import UserGroup

class AnalysisSettingsView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):

    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "analysis_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #analysis_settings = AnalysisSettings.objects.all().filter(account__id=self.request.user.id)

        #context['analysis_settings'] = analysis_settings

        return context

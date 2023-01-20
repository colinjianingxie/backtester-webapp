from braces.views import GroupRequiredMixin
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from main.models import Strategy
from oauth.constants import UserGroup
# User Access
# Helpers

class ExploreView(LoginRequiredMixin, GroupRequiredMixin,TemplateView):
    group_required = UserGroup.ADMIN.value
    raise_exception = True
    redirect_unauthenticated_users = True
    template_name = "apps/dashboard/explore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        default_strategies = Strategy.objects.all()
        context['explore_strategies'] = default_strategies
        return context

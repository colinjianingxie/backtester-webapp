from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView
from oauth.forms.create_account_form import RegistrationForm
from oauth.models import Admin
from oauth.models import User
#from oauth.models import Portfolio
from oauth.constants import UserGroup


class AccountCreationFormView(SuccessMessageMixin, CreateView):

    account_type = UserGroup.USER.value  # Default User Group is client
    template_name = "registration/register.html"
    form_class = RegistrationForm

    def save_model(self, user):
        if self.account_type == UserGroup.ADMIN.value:
            Admin(account=user).save()
        else:
            User(account=user).save()
        #Portfolio(account=user).save()

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.account_type = (
                self.account_type
            )  # Changing the account registration type
            self.save_model(user)
            user.save()
            user_group = Group.objects.get(name=self.account_type)
            user_group.user_set.add(user)
            return redirect("login")
        else:
            return render(request, self.template_name, {"form": form})

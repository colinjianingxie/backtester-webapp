from django.urls import include, path
from .views import account_creation_view as acv
from oauth.constants import UserGroup

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "accounts/create/",
        acv.AccountCreationFormView.as_view(account_type=UserGroup.USER.value),
        name="account_registration",
    ),
]

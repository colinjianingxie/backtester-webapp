from django.shortcuts import redirect
from oauth.constants import UserGroup


def login_redirect_success(request):
    """
    Redirects users based on whether they are in the certain group
    """
    if request.user.groups.filter(name=UserGroup.ADMIN.value).exists():
        # user is an admin
        return redirect("dashboard")
    elif request.user.groups.filter(name=UserGroup.USER.value).exists():
        return redirect("dashboard")
    return redirect("dashboard")

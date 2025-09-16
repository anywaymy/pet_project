from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import auth

from users.forms import UserLoginForm

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main:index")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
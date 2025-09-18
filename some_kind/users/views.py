from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import auth, messages

from  users.models import User
from users.forms import UserLoginForm, UserRegistrationForm

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main:index")

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        messages.success(self.request, "Поздравляем, вы успешно прошли регистрацию!")
        return super().form_valid(form)

class UserProfileView(ListView):
    model = User
    template_name = "users/profile.html"

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
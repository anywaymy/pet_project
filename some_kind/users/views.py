import uuid
from datetime import timedelta

from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import auth, messages
from django.utils import timezone

from users.models import User, EmailVerification
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

        user = form.save()
        expiration = timezone.now() + timedelta(hours=48)
        record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
        record.send_verification_email()

        messages.success(self.request, "Поздравляем, вы успешно прошли регистрацию! "
                                       "Вам на почту было направлено сообщение с кодом подтверждения")

        return super().form_valid(form)

class EmailVerificationView(TemplateView):
    template_name = "users/verification.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(email=self.kwargs.get("email")).first()
        verify = EmailVerification.objects.get(user=user, code=self.kwargs.get("code"))
        if verify:
            user.is_verify = True
            user.save()

        return super().get(request, *args, **kwargs)

class UserProfileView(ListView):
    model = User
    template_name = "users/profile.html"

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
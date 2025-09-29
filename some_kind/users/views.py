import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView

from common.view import TitleMixin
from users.forms import (StyledSetPasswordForm, UserLoginForm,
                         UserRegistrationForm, UsersResetPasswordForm)
from users.models import EmailVerification, User, UserPasswordResetToken


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main:index")
    title = "login"

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно авторизовались!")
        return super().form_valid(form)


class UserRegistrationView(TitleMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    title = "registration"

    def form_valid(self, form):
        messages.success(self.request, "Поздравляем, вы успешно прошли регистрацию! "
                                       "Вам на почту было направлено сообщение с кодом подтверждения")
        user = form.save()
        expiration = timezone.now() + timedelta(hours=48)
        record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
        record.send_verification_email()

        # WORK WITH CELERY
        # send_email_verify.delay(user.id)

        return super().form_valid(form)


class UsersResetPasswordView(TitleMixin, FormView):
    form_class = UsersResetPasswordForm
    template_name = "users/forgot_password.html"
    success_url = reverse_lazy("users:password_reset_info")
    title = "reset"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            code_obj = UserPasswordResetToken.objects.create(user=user, code=uuid.uuid4())
            link = reverse_lazy("users:recovery", kwargs={"code": code_obj.code, "email": user.email})
            full_link = f"{settings.DOMAIN_NAME}{link}"
            send_mail(
                subject="Восстановление",
                message="Восстановление пароля для пользователя {}. Чтобы восстановить пароль, перейдите по ссылке {}".format(user.username, full_link),
                from_email="solid@gmail.com",
                recipient_list=[user.email]
            )

        return super().form_valid(form)


class UsersPasswordConfirmResetView(TitleMixin, View):
    title = "new password"

    def get(self, request, *args, **kwargs):
        code_obj = get_object_or_404(UserPasswordResetToken, code=self.kwargs.get("code"), user__email=self.kwargs.get("email"))
        form = StyledSetPasswordForm(user=code_obj.user)
        if not code_obj:
            return render(request, template_name="users/recovery_invalid_link.html")

        return render(request, template_name="users/recovery_link.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        code_obj = get_object_or_404(UserPasswordResetToken, code=self.kwargs.get("code"), user__email=self.kwargs.get("email"))

        if not code_obj:
            return render(request, template_name="users/recovery_invalid_link.html")

        form = StyledSetPasswordForm(user=code_obj.user, data=request.POST)

        if form.is_valid():
            form.save()
            code_obj.delete()
            return HttpResponseRedirect(reverse("users:password_reset_complete"))

        return render(request, template_name="users/recovery_link.html", context={"form": form})


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = "users/verification.html"
    title = "verify"

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(email=self.kwargs.get("email")).first()
        verify = EmailVerification.objects.filter(user=user, code=self.kwargs.get("code"))

        if verify.exists() and not verify.first().is_expired():
            user.is_verify = True
            user.save()

            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('main:index'))


class UserProfileView(TitleMixin, ListView):
    model = User
    template_name = "users/profile.html"
    title = "profile"


def password_reset_info(request):
    return render(request, template_name="users/password_reset_info.html", context={"title": "info"})


def password_reset_complete(request):
    return render(request, template_name="users/password_reset_complete.html", context={"title": "complete"})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))

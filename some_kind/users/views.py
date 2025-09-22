import uuid
from datetime import timedelta

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import auth, messages
from django.utils import timezone
from django.conf import settings


from users.models import User, EmailVerification, UserPasswordResetToken
from users.forms import UserLoginForm, UserRegistrationForm, UsersResetPasswordForm, StyledSetPasswordForm

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

class UsersResetPasswordView(FormView):
    form_class = UsersResetPasswordForm
    template_name = "users/forgot_password.html"
    success_url = reverse_lazy("main:index")

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
                from_email = "solid@gmail.com",
                recipient_list = [user.email]
            )

        return super().form_valid(form)

class UsersPasswordConfirmResetView(View):
    # template_name = "users/recovery_link.html"
    def get(self, request, *args, **kwargs):
        code_obj = get_object_or_404(UserPasswordResetToken, code=self.kwargs.get("code"), user__email=self.kwargs.get("email"))
        form = StyledSetPasswordForm(user=code_obj.user)
        if not code_obj:
            return render(request, template_name="users/recovery_invalid_link.html")

        return render(request, template_name="users/recovery_link.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        code_obj = get_object_or_404(UserPasswordResetToken, code=self.kwargs.get("code"), user__email=self.kwargs.get("email"))

        if not code_obj:
            return render(request, template_name="users/recovery_invalid_link.html")

        form = StyledSetPasswordForm(user=code_obj.user, data=request.POST)

        if form.is_valid():
            form.save()
            code_obj.delete()
            return HttpResponseRedirect(reverse("users:password_reset_complete"))

        return render(request, template_name="users/recovery_link.html", context={"form":form})

class EmailVerificationView(TemplateView):
    template_name = "users/verification.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(email=self.kwargs.get("email")).first()
        verify = EmailVerification.objects.filter(user=user, code=self.kwargs.get("code"))

        if verify.exists() and not verify.first().is_expired():
            user.is_verify = True
            user.save()

            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('main:index'))

class UserProfileView(ListView):
    model = User
    template_name = "users/profile.html"

def password_reset_complete(request):
    return render(request, template_name="users/password_reset_complete.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=24, unique=True)
    email = models.EmailField(max_length=40, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="users_images", null=True, blank=True)
    is_verify = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse_lazy("users:verify", kwargs={"code": self.code, "email": self.user.email})
        full_link = f"{settings.DOMAIN_NAME}{link}"

        send_mail(
            subject=f"Подтверждение почты для {self.user.username}",
            message="для подтверждения почты для {}, перейдите по ссылке - {}".format(self.user.email, full_link),
            from_email="solid@gmail.com",
            recipient_list=[self.user.email]
        )

    def is_expired(self):
        return True if timezone.now() >= self.expiration else False


class UserPasswordResetToken(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib import admin

from users.models import EmailVerification, User, UserPasswordResetToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(UserPasswordResetToken)
class UserPasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')

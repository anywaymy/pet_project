from django.contrib import admin
from users.models import User, EmailVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)



@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user',)

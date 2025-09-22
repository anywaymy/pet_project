from django.urls import path
from users.views import (UserLoginView, UserRegistrationView, EmailVerificationView,
                         UserProfileView, UsersResetPasswordView, UsersPasswordConfirmResetView, logout, password_reset_complete)

app_name = "users"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),

    path('verify/<uuid:code>/<str:email>', EmailVerificationView.as_view(), name='verify'),

    path('forgot_password/', UsersResetPasswordView.as_view(), name='forgot_password'),
    path('recovery/<uuid:code>/<str:email>', UsersPasswordConfirmResetView.as_view(), name='recovery'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
]
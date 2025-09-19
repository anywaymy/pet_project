from django.urls import path
from users.views import UserLoginView, UserRegistrationView, EmailVerificationView, UserProfileView, logout

app_name = "users"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),

    path('verify/<uuid:code>/<str:email>', EmailVerificationView.as_view(), name='verify'),

]
from django.urls import path
from users.views import UserLoginView, UserRegistrationView, UserProfileView, logout

app_name = "users"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
]
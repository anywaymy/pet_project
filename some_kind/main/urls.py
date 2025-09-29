from django.urls import path

from main.views import IndexView, PostDetailView

app_name = "main"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('details/<slug:slug>/', PostDetailView.as_view(), name='details'),
]

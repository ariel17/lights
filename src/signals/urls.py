from django.urls import path

from .views import FlagAPIView

app_name = "signals"
urlpatterns = [
    path('<str:name>', FlagAPIView.as_view(), name="flag"),
]


from django.urls import path
from .views import run_command_view

urlpatterns = [
    path("", run_command_view, name="run_command"),
]

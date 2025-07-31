from django.urls import path
from .views import CommandRunTerminalView
from . import views

app_name = "django_admin_command_runner"

urlpatterns = [
    path("run-command/", views.run_command_view, name="run_command_view"),
    path("run-terminal/", CommandRunTerminalView.as_view(), name="run_command_view"),
]

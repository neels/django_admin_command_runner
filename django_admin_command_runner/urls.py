from django.urls import path
from .views import CommandRunTerminalView
from . import views
urlpatterns = [
    path("run-command/", views.run_command_view, name="run_command_view"),
    path("run-terminal/", CommandRunTerminalView.as_view(), name="run_command_view"),
]

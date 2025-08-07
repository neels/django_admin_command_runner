
from django.urls import path
from .views import run_command_form_view, live_output_view, CommandRunTerminalView


urlpatterns = [
    path("commandlog/run/", run_command_form_view, name="run_command"),
    path("commandlog/<int:log_id>/live/", live_output_view, name="live_output"),
    path("run-terminal/", CommandRunTerminalView.as_view(), name="run_terminal"),
]

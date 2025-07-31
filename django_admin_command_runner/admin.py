from django.contrib import admin
from django.urls import path
from .models import CommandLog
from .views import CommandRunTerminalView, run_command_form_view
@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "started_at")
    change_list_template = "admin/command_runner/commandlog_changelist.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run/", self.admin_site.admin_view(run_command_form_view), name="run_command_form"),
            path("run/terminal/", self.admin_site.admin_view(CommandRunTerminalView.as_view()), name="run_command_view"),
        ]
        return custom_urls + urls

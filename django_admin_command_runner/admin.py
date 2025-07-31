from django.contrib import admin
from django.urls import path
from django_admin_command_runner.models import CommandLog
from django_admin_command_runner.views import run_command_form_view

@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
    change_list_template = "admin/command_runner/commandlog_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run/", admin.site.admin_view(run_command_form_view), name="commandlog-run"),
        ]
        return custom_urls + urls

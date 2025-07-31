
from django.contrib import admin
from django.urls import path
from .views import run_command_view
from .models import CommandLog


@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
    list_display = ("command", "user", "created_at", "return_code")
    search_fields = ("command", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("command", "user", "output", "error", "return_code", "created_at")


class CommandRunnerLink:
    # Dummy class to represent a custom admin page.
    pass


@admin.register(CommandRunnerLink)
class CommandRunnerLinkAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return run_command_view(request)

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

    class Meta:
        verbose_name = "Command Runner"
        verbose_name_plural = "Command Runner"

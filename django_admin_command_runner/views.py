
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import get_commands
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import CommandLog
from .threaded_runner import thread_registry


@method_decorator(staff_member_required, name='dispatch')
class CommandRunTerminalView(View):
    def get(self, request, *args, **kwargs):
        command = request.GET.get("command")
        args = request.GET.get("args", "")
        kwargs_json = request.GET.get("kwargs", "{}")

        context = {
            "command": command,
            "args": args,
            "kwargs": kwargs_json
        }
        return render(request, "admin/commandlog/run_command.html", context)


@staff_member_required
def command_output(request, command_log_id):
    log = get_object_or_404(CommandLog, pk=command_log_id)

    if log.status == "RUNNING":
        def stream():
            while thread_registry.is_running(log.id):
                output = thread_registry.get_output(log.id)
                yield output or ""
        return StreamingHttpResponse(stream(), content_type="text/plain")
    else:
        return JsonResponse({"output": log.output or ""})

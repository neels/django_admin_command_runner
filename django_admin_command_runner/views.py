
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.core.management import get_commands
from django.urls import reverse
import subprocess
@method_decorator(staff_member_required, name='dispatch')
class CommandRunTerminalView(View):
    def get(self, request, *args, **kwargs):
        command = request.GET.get("command")
        args = request.GET.get("args", "")
        if not command:
            return HttpResponse("No command provided.", status=400)
        def stream_output():
            full_command = f"python manage.py {command} {args}".strip()
            process = subprocess.Popen(full_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(process.stdout.readline, ''):
                yield line.replace('\n', '<br>')
            process.stdout.close()
        return StreamingHttpResponse(stream_output(), content_type='text/html')
@staff_member_required
def run_command_form_view(request):
    commands = get_commands()
    grouped = {}
    for cmd, app in commands.items():
        grouped.setdefault(app, []).append(cmd)
    for cmds in grouped.values():
        cmds.sort()
    if request.method == "POST":
        command = request.POST.get("command")
        args = request.POST.get("args", "")
        url = f"{request.path}terminal/?command={command}&args={args}"
        return HttpResponseRedirect(url)
    return render(request, "admin/command_runner/run_command.html", {"commands": grouped})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CommandLog
from .threaded_runner import CommandExecutionThread, thread_registry

@staff_member_required
def run_command_form_view(request):
    from django.core.management import get_commands

    commands = get_commands()
    grouped = {}
    for cmd, app in commands.items():
        grouped.setdefault(app, []).append(cmd)
    for cmds in grouped.values():
        cmds.sort()

    if request.method == "POST":
        command = request.POST.get("command")
        args = request.POST.get("args", "")

        log = CommandLog.objects.create(name=command, args=args, user=request.user)
        runner = CommandExecutionThread(log.id, command, args)
        runner.start()
        return HttpResponseRedirect(reverse("admin:django_admin_command_runner_commandlog_changelist") + "?ran=true")

    return render(request, "admin/command_runner/run_command_form.html", {"commands": sorted(commands)})


@csrf_exempt
@staff_member_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
from .models import CommandLog
from .threaded_runner import thread_registry

def live_output_view(request, log_id):
    log = get_object_or_404(CommandLog, id=log_id)

    if log.status == "COMPLETED":
        return HttpResponse(f"<pre>{log.output}</pre>")

    # Still running — return streaming output
    thread = next((t for t in thread_registry.values() if t.log_id == log.id), None)

    def stream():
        if thread:
            for line in thread.output[-50:]:
                yield line + "<br>"
        else:
            for line in log.output.splitlines()[-50:]:
                yield line + "<br>"

    return StreamingHttpResponse(stream(), content_type="text/html")

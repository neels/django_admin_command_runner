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

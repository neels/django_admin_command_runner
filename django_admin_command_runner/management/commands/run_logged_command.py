from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.timezone import now
from django_admin_command_runner.models import CommandLog
import threading
import io
import sys
def run_command_in_thread(log_id):
    log = CommandLog.objects.get(id=log_id)
    out = io.StringIO()
    try:
        log.status = "RUNNING"
        log.save()
        call_command(log.name, *log.args.split(), stdout=out)
        log.output = out.getvalue()
        log.return_code = 0
        log.status = "SUCCESS"
    except Exception as e:
        log.output = out.getvalue()
        log.error = str(e)
        log.status = "FAILED"
        log.return_code = 1
    log.finished_at = now()
    log.save()
class Command(BaseCommand):
    help = "Run a Django management command and log the result"
    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Command name")
        parser.add_argument("--args", type=str, default="", help="Space-separated arguments")
        parser.add_argument("--user_id", type=int, help="Optional user ID who triggered the command")
    def handle(self, *args, **options):
        user = None
        if options.get("user_id"):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=options["user_id"])
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING("User ID not found. Proceeding without linking a user."))
        log = CommandLog.objects.create(
            name=options["name"],
            args=options["args"],
            user=user
        )
        thread = threading.Thread(target=run_command_in_thread, args=(log.id,))
        thread.start()
        self.stdout.write(f"Started command '{log.name}' with ID {log.id}")

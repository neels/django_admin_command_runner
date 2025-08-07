
from threading import Thread
import subprocess
import uuid
from django.utils.timezone import now
from .models import CommandLog

thread_registry = {}

class CommandExecutionThread(Thread):
    def __init__(self, log_id, command, args):
        super().__init__()
        self.log_id = log_id
        self.command = command
        self.args = args
        self.output = []
        self.return_code = None
        self.uuid = str(uuid.uuid4())
        thread_registry[self.uuid] = self

    def run(self):
        log = CommandLog.objects.get(id=self.log_id)
        log.status = "RUNNING"
        log.started_at = now()
        log.save()

        cmd = ["python", "manage.py", self.command] + self.args.split()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            self.output.append(line)
            log.output += line
            log.save(update_fields=["output"])

        process.stdout.close()
        self.return_code = process.wait()

        log.status = "COMPLETED" if self.return_code == 0 else "FAILED"
        log.return_code = self.return_code
        log.finished_at = now()
        log.save()

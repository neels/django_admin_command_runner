from django.db import models
from django.conf import settings
class CommandLog(models.Model):
    name = models.CharField(max_length=100)
    args = models.TextField(blank=True)
    kwargs = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="PENDING")
    return_code = models.IntegerField(null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.name} ({self.status})"

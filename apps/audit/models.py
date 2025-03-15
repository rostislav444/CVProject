from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10)  # GET, POST, PUT, etc.
    path = models.CharField(max_length=255)
    query_string = models.TextField(blank=True, null=True)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"

from django.contrib import admin
from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Admin configuration for RequestLog model."""
    list_display = ('timestamp', 'method', 'path', 'remote_addr', 'user')
    list_filter = ('method', 'timestamp')
    search_fields = ('path', 'remote_addr', 'user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp', 'method', 'path', 'query_string', 'remote_addr', 'user')

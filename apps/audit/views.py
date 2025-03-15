from django.views.generic import ListView

from apps.audit.models import RequestLog


class RecentRequestsView(ListView):
    model = RequestLog
    template_name = "audit/recent_requests.html"
    context_object_name = "requests"
    paginate_by = 10

    def get_queryset(self):
        return RequestLog.objects.all().order_by("-timestamp")

from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog


class RequestLogMiddleware(MiddlewareMixin):    
    def process_request(self, request):
        # Only log if the path is not a static or media file
        if not (request.path.startswith('/static/') or 
                request.path.startswith('/media/')):
            
            # Create a RequestLog entry
            RequestLog.objects.create(
                method=request.method,
                path=request.path,
                query_string=request.META.get('QUERY_STRING', ''),
                remote_addr=self._get_client_ip(request),
                user=request.user if request.user.is_authenticated else None
            )
        
        # Always return None to continue processing the request
        return None

    def _get_client_ip(self, request):
        """Extract the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Return the first IP in the list
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', None)
# decorators.py
from functools import wraps
from django.http import HttpResponseForbidden

def allow_specific_ip(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Define the allowed IP address
        allowed_ip = '127.0.0.1'  # Replace with the actual IP address of the lab PC
        
        # Get the client's IP address
        client_ip = request.META.get('REMOTE_ADDR')
        print(client_ip)    

        # Check if the client's IP matches the allowed IP
        if client_ip != allowed_ip:
            return HttpResponseForbidden("Access forbidden. You are not allowed to access this website.")
        
        # Call the original view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view

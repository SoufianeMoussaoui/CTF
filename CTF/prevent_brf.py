from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.http import HttpResponseForbidden
from functools import wraps


def brute_force_protect(view_func): 
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ip = get_client_ip(request)
        attempts = cache.get(ip, 0)
        if attempts >= 10:
            return HttpResponseForbidden(
                'Too many flag submission attempts. ' 
                'Try again later after 5 min.')
        response = view_func(request, *args, **kwargs)
        if request.session.get('flag_failed'):
            cache.set(ip, attempts + 1, timeout=300) 
            request.session['flag_failed'] = False 
        else:
            cache.delete(ip) 
        return response
    
    return _wrapped_view


# Helper function to get the ip 
def get_client_ip(request):
   
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip

from functools import wraps
from django.http import JsonResponse
from .models import AccessKey

def require_valid_key(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get('X-Access-Key')
        if not key:
            return JsonResponse({'error': 'Access key required'}, status=401)
        
        try:
            access_key = AccessKey.objects.get(key=key)
            if not access_key.is_valid():
                return JsonResponse({'error': 'Invalid or expired key'}, status=403)
        except AccessKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid key'}, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

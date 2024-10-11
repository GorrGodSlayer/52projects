from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, AccessKey
import json
import uuid
from datetime import datetime, timedelta

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'user_type': 'owner' if user.is_owner else 'waiter'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success'})

@csrf_exempt
def generate_key(request):
    if request.method == 'POST' and request.user.is_owner:
        key = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(days=30)
        AccessKey.objects.create(key=key, expires_at=expires_at)
        return JsonResponse({'status': 'success', 'key': key})
    return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

@csrf_exempt
def validate_key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        try:
            access_key = AccessKey.objects.get(key=key, is_active=True)
            if access_key.expires_at > datetime.now():
                return JsonResponse({'status': 'success', 'valid': True})
            else:
                access_key.is_active = False
                access_key.save()
        except AccessKey.DoesNotExist:
            pass
        return JsonResponse({'status': 'success', 'valid': False})

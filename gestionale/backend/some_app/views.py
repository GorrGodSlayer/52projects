from core.decorators import require_valid_key

@require_valid_key
def some_protected_view(request):
    # Your view logic here
    pass

"""
Views for session management and user switching.
"""
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def switch_to_original_user(request):
    """
    Switch back to the original user from admin session.
    This view can be called manually if automatic switching doesn't work.
    """
    preserved_user_id = request.session.get('_original_user_id')
    
    if preserved_user_id and request.user.is_superuser:
        try:
            original_user = User.objects.get(id=preserved_user_id)
            # Logout current admin user
            logout(request)
            # Login as original user
            login(request, original_user, backend='django.contrib.auth.backends.ModelBackend')
            # Clear the preserved user ID
            if '_original_user_id' in request.session:
                del request.session['_original_user_id']
            return redirect('/')
        except User.DoesNotExist:
            pass
    
    return redirect('/')


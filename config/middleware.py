"""
Middleware to preserve regular user session when accessing admin panel.
This prevents admin login from logging out regular users.
"""
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


class PreserveUserSessionMiddleware:
    """
    Middleware that preserves the original user session when accessing admin.
    When a user logs into admin, their original user session is stored.
    When they navigate back to the regular site, the original user is automatically restored.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_admin_path = request.path.startswith('/admin/')
        preserved_user_id = request.session.get('_original_user_id')
        
        # BEFORE processing request:
        # If we're navigating away from admin to regular site and current user is superuser
        # Restore the original user BEFORE processing the request
        if not is_admin_path and preserved_user_id:
            if request.user.is_authenticated and request.user.is_superuser:
                try:
                    original_user = User.objects.get(id=preserved_user_id)
                    # Only switch if the original user is different from current
                    if original_user.id != request.user.id:
                        # Logout current admin user and login as original user
                        logout(request)
                        login(request, original_user, backend='django.contrib.auth.backends.ModelBackend')
                        # Clear the preserved user ID
                        if '_original_user_id' in request.session:
                            del request.session['_original_user_id']
                        # Reload the user object
                        from django.contrib.auth import get_user
                        request.user = get_user(request)
                except User.DoesNotExist:
                    # Original user doesn't exist, clear the session variable
                    if '_original_user_id' in request.session:
                        del request.session['_original_user_id']
        
        # If we're on admin path and user is authenticated but not superuser
        # Store the original user ID before they log in as admin
        if is_admin_path:
            if request.user.is_authenticated and not request.user.is_superuser:
                # Store the original user before admin login
                if '_original_user_id' not in request.session:
                    request.session['_original_user_id'] = request.user.id
                    request.session.save()
        
        # Process the request
        response = self.get_response(request)
        
        return response


"""
Middleware to isolate admin sessions from main site sessions.
This prevents admin login from affecting main site user sessions across different tabs.

This middleware works ALONGSIDE Django's SessionMiddleware by:
1. Intercepting session cookie reads/writes
2. Using different cookie names for admin vs main site
3. Modifying the response to use the correct cookie name
"""
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings


class IsolatedSessionMiddleware(SessionMiddleware):
    """
    Extends Django's SessionMiddleware to use separate session cookies for admin and main site.
    
    - Admin uses: 'adminsessionid' cookie
    - Main site uses: 'sessionid' cookie (default)
    
    This prevents admin login from affecting main site sessions in other tabs.
    """
    
    def process_request(self, request):
        """Override to use different cookie names based on path."""
        is_admin_path = request.path.startswith('/admin/')
        
        # Store which cookie name to use
        if is_admin_path:
            request._session_cookie_name = 'adminsessionid'
            # Get session key from admin cookie
            session_key = request.COOKIES.get('adminsessionid', None)
        else:
            request._session_cookie_name = 'sessionid'
            # Get session key from default cookie
            session_key = request.COOKIES.get('sessionid', None)
        
        # Manually set up session with the correct cookie's session key
        # Import SessionStore from configured backend
        session_engine = getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db')
        engine = __import__(session_engine, {}, {}, ['SessionStore'])
        request.session = engine.SessionStore(session_key)

    def process_response(self, request, response):
        """Override to set the correct cookie name in response."""
        # First, let parent handle session saving
        # But we need to intercept and change the cookie name
        
        # Check if session was accessed
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            return response
        
        # Get the cookie name we determined in process_request
        cookie_name = getattr(request, '_session_cookie_name', 'sessionid')
        
        # If session was modified, save it and set cookie with correct name
        if modified:
            request.session.save()
            
            # Remove the default sessionid cookie if it was set
            if 'sessionid' in response.cookies and cookie_name != 'sessionid':
                del response.cookies['sessionid']
            if 'adminsessionid' in response.cookies and cookie_name != 'adminsessionid':
                del response.cookies['adminsessionid']
            
            # Set cookie with correct name
            # Use max_age (not expires) - Django's set_cookie doesn't allow both
            if request.session.get_expire_at_browser_close():
                max_age = None
            else:
                max_age = request.session.get_expiry_age()
            
            # Get cookie settings
            cookie_domain = getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
            cookie_path = getattr(settings, 'SESSION_COOKIE_PATH', '/')
            cookie_secure = getattr(settings, 'SESSION_COOKIE_SECURE', False)
            cookie_httponly = getattr(settings, 'SESSION_COOKIE_HTTPONLY', True)
            cookie_samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')
            
            # Build cookie kwargs
            cookie_kwargs = {
                'domain': cookie_domain,
                'path': cookie_path,
                'secure': cookie_secure or None,
                'httponly': cookie_httponly or None,
                'samesite': cookie_samesite,
            }
            
            # Add max_age only if it's not None (session expires at browser close if None)
            if max_age is not None:
                cookie_kwargs['max_age'] = max_age
            
            response.set_cookie(
                cookie_name,
                request.session.session_key,
                **cookie_kwargs
            )
        
        return response


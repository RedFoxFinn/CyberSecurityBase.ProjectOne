"""
Custom middleware for the CSB Project.
"""

from django.shortcuts import redirect


class AdminAccessMiddleware:
    """
    Middleware to restrict admin panel access to superusers only.
    Regular staff users will be redirected to the home page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if accessing the admin panel
        if request.path.startswith('/admin/'):
            # Allow access to login page for everyone
            if request.path == '/admin/login/':
                return self.get_response(request)

            # Check if user is authenticated and is a superuser
            if request.user.is_authenticated:
                if not request.user.is_superuser:
                    # Regular staff users trying to access admin - redirect to home
                    return redirect('/')
            else:
                # Allow unauthenticated users to see login page
                pass

        response = self.get_response(request)
        return response

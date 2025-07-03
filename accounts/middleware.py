from django.shortcuts import redirect
from django.conf import settings

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/accounts/logout/',
            '/accounts/request-verification/',
            '/accounts/password-reset/',
            '/accounts/password-reset/done/',
            '/accounts/reset/<uidb64>/<token>/',
            '/accounts/reset/done/',
        ] + getattr(settings, 'VERIFICATION_EXEMPT_URLS', [])

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None
            
        if hasattr(request.user, 'profile') and not request.user.profile.email_verified:
            if request.path not in self.exempt_urls and not request.path.startswith('/admin/'):
                return redirect('request_verification')
        
        return None
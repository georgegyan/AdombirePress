from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('logout'),
            reverse('request_verification'),
            reverse('verify_email'),
            reverse('password_reset'),
            reverse('password_reset_done'),
            reverse('password_reset_confirm'),
            reverse('password_reset_complete'),
        ] + getattr(settings, 'VERIFICATION_EXEMPT_URLS', [])

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None
            
        if hasattr(request.user, 'profile') and not request.user.profile.email_verified:
            if request.path not in self.exempt_urls:
                return redirect('request_verification')
        
        return None
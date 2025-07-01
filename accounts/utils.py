from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(user):
    profile = user.profile
    subject = render_to_string('accounts/verification_email_subject.txt')
    html_message = render_to_string('accounts/verification_email.html', {
        'user': user,
        'domain': settings.DOMAIN,
        'protocol': 'https' if settings.USE_HTTPS else 'http',
        'token': profile.verification_token,
        'site_name': settings.SITE_NAME,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
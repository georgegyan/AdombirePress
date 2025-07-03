from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserActivity, Profile
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_activity_email(user, activity):
    subject = f"New activity on your account: {activity.get_activity_type_display()}"
    html_message = render_to_string('accounts/activity_notification_email.html', {
        'user': user,
        'activity': activity,
        'site_name': settings.SITE_NAME
    })
    send_mail(
        subject,
        strip_tags(html_message),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message
    )

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    
    activity = UserActivity.objects.create(
        user=user,
        activity_type='login',
        ip_address=ip_address,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    profile, created = Profile.objects.get_or_create(user=user)
    # Update profile with login IP
    previous_ip = profile.last_login_ip
    profile.last_login_ip = ip_address
    profile.save()
    
    # Send email notification for suspicious logins if this isn't the first login
    if previous_ip and ip_address != previous_ip:
        send_activity_email(user, activity)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        activity_type='logout',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
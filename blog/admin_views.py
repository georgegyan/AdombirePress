from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from accounts.models import UserActivity
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
import csv

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # Time ranges
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    
    # Activity metrics
    recent_activities = UserActivity.objects.all().order_by('-timestamp')[:20]
    active_users = UserActivity.objects.filter(
        timestamp__gte=last_24h
    ).values('user').annotate(total=Count('user')).count()
    
    # Activity types breakdown
    activity_types = UserActivity.objects.filter(
        timestamp__gte=last_7d
    ).values('activity_type').annotate(total=Count('activity_type')).order_by('-total')
    
    # Login locations (requires geoip2)
    login_locations = []
    try:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        unique_ips = UserActivity.objects.filter(
            activity_type='login'
        ).values('ip_address').distinct()
        
        for ip in unique_ips:
            if ip['ip_address']:
                try:
                    location = g.city(ip['ip_address'])
                    login_locations.append({
                        'ip': ip['ip_address'],
                        'city': location['city'],
                        'country': location['country_name']
                    })
                except:
                    continue
    except:
        pass
    
    context = {
        'recent_activities': recent_activities,
        'active_users': active_users,
        'activity_types': activity_types,
        'login_locations': login_locations,
        'time_ranges': {
            'last_24h': last_24h,
            'last_7d': last_7d
        }
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def export_activities(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_activities.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['User', 'Activity Type', 'IP Address', 'Timestamp', 'User Agent'])
    
    activities = UserActivity.objects.all().order_by('-timestamp')
    for activity in activities:
        writer.writerow([
            activity.user.username,
            activity.get_activity_type_display(),
            activity.ip_address,
            activity.timestamp,
            activity.user_agent
        ])
    
    return response
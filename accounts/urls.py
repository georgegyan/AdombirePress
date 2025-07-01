from django.urls import path
from . import views
from .views import verify_email, request_verification_email

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('request-verification/', request_verification_email, name='request_verification'),
    path('activity/', views.activity_log, name='activity_log'),
]
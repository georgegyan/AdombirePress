from django.urls import path
from . import views
from .views import CategoryListView, post_search, contact_view, post_create, post_update, post_delete, post_publish
from .admin_views import admin_dashboard, export_activities

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_posts'),
    path('search/', post_search, name='post_search'),
    path('contact/', contact_view, name='contact'),
    path('create/', post_create, name='post_create'),
    path('<slug:slug>/edit/', post_update, name='post_update'),
    path('<slug:slug>/delete/', post_delete, name='post_delete'),
    path('<slug:slug>/publish/', post_publish, name='post_publish'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-export/', export_activities, name='admin_export'),
]

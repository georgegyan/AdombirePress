from django.urls import path
from . import views
from .views import CategoryListView, post_search, contact_view

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_posts'),
    path('search/', post_search, name='post_search'),
    path('contact/', contact_view, name='contact'),
]
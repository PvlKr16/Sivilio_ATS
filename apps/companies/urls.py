"""URL patterns for the Companies module."""

from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='index'),
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='delete'),
]

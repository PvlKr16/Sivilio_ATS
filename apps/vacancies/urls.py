"""URL patterns for the Vacancies module."""

from django.urls import path
from . import views

app_name = 'vacancies'

urlpatterns = [
    path('',              views.VacancyListView.as_view(),   name='index'),
    path('create/',       views.VacancyCreateView.as_view(), name='create'),
    path('<int:pk>/',     views.VacancyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.VacancyUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='delete'),
]

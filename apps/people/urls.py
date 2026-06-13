"""URL patterns for the People module."""

from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('',               views.PersonListView.as_view(),   name='index'),
    path('create/',        views.PersonCreateView.as_view(), name='create'),
    path('<int:pk>/',      views.PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PersonUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PersonDeleteView.as_view(), name='delete'),
    path('autocomplete/',  views.person_autocomplete,        name='autocomplete'),
    path('parse-cv/',      views.parse_cv,                   name='parse_cv'),
]

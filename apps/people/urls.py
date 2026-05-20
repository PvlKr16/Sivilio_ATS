"""URL patterns for the People module."""

from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    # People CRUD
    path('', views.PersonListView.as_view(), name='index'),
    path('create/', views.PersonCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PersonUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PersonDeleteView.as_view(), name='delete'),

    # Education nested under person
    path('<int:person_pk>/education/add/', views.EducationCreateView.as_view(), name='education_add'),
    path('education/<int:pk>/delete/', views.EducationDeleteView.as_view(), name='education_delete'),

    # Work experience nested under person
    path('<int:person_pk>/work/add/', views.WorkCreateView.as_view(), name='work_add'),
    path('work/<int:pk>/delete/', views.WorkDeleteView.as_view(), name='work_delete'),

    # AJAX
    path('autocomplete/', views.person_autocomplete, name='autocomplete'),
]

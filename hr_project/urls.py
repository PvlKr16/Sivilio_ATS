"""
Root URL configuration for HR IT platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('people/', include('apps.people.urls', namespace='people')),
    path('companies/', include('apps.companies.urls', namespace='companies')),
    path('vacancies/', include('apps.vacancies.urls', namespace='vacancies')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('', include('apps.core.urls', namespace='core')),
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

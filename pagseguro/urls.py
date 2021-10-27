from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('core.urls')),
    path('api/', include('api.urls')),
    path('providers/', include('providers.urls')),
    path('payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )

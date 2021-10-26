import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    # path('', include('payments.urls')),
    path('providers/', include('providers.urls')),
    path('payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]

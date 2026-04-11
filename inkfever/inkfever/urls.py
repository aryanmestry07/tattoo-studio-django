from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('studio.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin-login/', dashboard_views.admin_login, name='admin_login'),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
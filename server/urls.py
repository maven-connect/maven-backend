from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('group/', include('group.urls')),
    path('lost-found/', include('lostandfound.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls', namespace='home')),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='user')),
    path('email/', include('email_manager.urls', namespace='email')),
    path('client/', include('email_manager.urls', namespace='client')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Intelligent Trader Admin Panel'

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]


# Added for vercel deployment
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
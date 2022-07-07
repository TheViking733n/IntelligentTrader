from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Intelligent Trader Admin Panel'

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]

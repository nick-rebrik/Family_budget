from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('budget.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('admin/', admin.site.urls),
]

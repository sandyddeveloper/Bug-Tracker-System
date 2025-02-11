from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('Auth.urls')),
    path('api/v1/auth/', include('SocialAuth.urls')),
    path('api/core', include('Core.urls')),
]

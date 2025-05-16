# core/urls.py

import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT endpoints
    path('api/auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),

    # Admin
    path('admin/', admin.site.urls),

    # Your API
    path('api/', include('api.urls')),

    # Serve your custom OpenAPI schema
    path(
        'api/schema/',
        serve,
        {
            'path': 'schema.yaml',
            'document_root': os.path.join(settings.BASE_DIR, 'docs'),
        },
        name='schema'
    ),


    path(
        'api/docs/',
        SpectacularRedocView.as_view(
            url='/api/schema/',
            template_name='redoc.html'     
        ),
        name='redoc'
    ),


    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(
            url='/api/schema/'
        ),
        name='swagger-ui'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

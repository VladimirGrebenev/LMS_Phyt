from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken import views
from rest_framework import permissions
from users.views import RegisterUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api-auth/', include('rest_framework.urls')),
    path('token-api-auth/', views.obtain_auth_token),
    path('', include('courses.urls')),
    path('users/', include('users.urls')),
]


# API Docs (Swagger, ReDoc)
schema_view = get_schema_view(
    openapi.Info(
        title="LMS Phyt",
        default_version='v1',
        description="API documentation for LMS Phyt",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="grebenev-81@mail.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

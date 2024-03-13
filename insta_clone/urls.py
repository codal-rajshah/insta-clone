from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Insta Clone Available APIs",
        default_version="v1",
        description="Instagram APIs",
        terms_of_service="http://127.0.0.1:8000/terms/",
        contact=openapi.Contact(email="rshah3@codal.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_patterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += schema_patterns

# users app urls
urlpatterns += [path("api/", include("apps.users.urls"))]

# common app urls
urlpatterns += [path("api/", include("apps.common.urls"))]

# friends app urls
urlpatterns += [path("api/", include("apps.friends.urls"))]

# posts app urls
urlpatterns += [path("api/", include("apps.posts.urls"))]

# oauth2 provider urls
urlpatterns += [
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider"))
]


# static and media patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

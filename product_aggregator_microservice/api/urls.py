from api.views.product import ProductViewSet
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions, routers

router = routers.DefaultRouter(trailing_slash=True)
router.include_format_suffixes = False
router.register("products", ProductViewSet, "product")

docs_schema_view = get_schema_view(
    openapi.Info(
        title="Product Microservice API",
        default_version="v1",
        description="Applifting project for Product Microservice",
        contact=openapi.Contact(email="daniel.klic96@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("v1/", include(router.urls)),
    re_path(
        r"docs/swagger(?P<format>\.json|\.yaml)$",
        docs_schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/swagger/",
        docs_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "docs/redoc/",
        docs_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

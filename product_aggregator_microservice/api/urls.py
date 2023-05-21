from api.views.product import ProductViewSet
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.include_format_suffixes = False
router.register("products", ProductViewSet, "product")

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("v1/", include(router.urls)),
]

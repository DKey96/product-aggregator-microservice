from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.include_format_suffixes = False

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
]

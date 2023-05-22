from authentication.views.registration import RegistrationView
from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("api-token/", obtain_auth_token, name="api_token_auth"),
]

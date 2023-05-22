import datetime

import requests
from applifting_client.models import AppliftingToken
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.utils import json

APPLIFTING_TOKEN_VALIDITY = 5 * 60  # 5 minutes


class AppliftingException(Exception):
    def __init__(self, message, status_code):
        self.status_code = status_code
        self.message = message


class AppliftingClient:
    def __init__(self):
        self.refresh_token = settings.APPLIFTING_REFRESH_TOKEN
        self.base_url = settings.APPLIFTING_SERVICE_BASE_URL

    def get_valid_token(self) -> str:
        try:
            token_model = (
                AppliftingToken.objects.filter(is_valid=True)
                .order_by("-created_at")
                .first()
            )
            token = token_model.token

            token_freshness = (
                datetime.datetime.now(datetime.timezone.utc) - token_model.created_at
            )
            if token_freshness.total_seconds() >= APPLIFTING_TOKEN_VALIDITY:
                token = self.refresh_auth_token()
        except ObjectDoesNotExist:
            token = self.refresh_auth_token()
        return token

    def refresh_auth_token(self) -> str:
        response = requests.post(
            f"{self.base_url}/auth", headers={"Bearer": self.refresh_token}
        )
        if response.status_code != 201:
            raise AppliftingException(response.text, response.status_code)

        for token_model in AppliftingToken.objects.all():
            token_model.delete()

        new_token = response.json()["access_token"]
        AppliftingToken.objects.create(token=new_token)

        return new_token

    def register_new_product(
        self, product_uuid: str, name: str, description: str
    ) -> None:
        headers = {
            "Bearer": f"{self.get_valid_token()}",
            "Content-Type": "application/json",
        }
        body = {"id": str(product_uuid), "name": name, "description": description}
        response = requests.post(
            f"{self.base_url}/products/register",
            headers=headers,
            data=json.dumps(body),
        )
        if response.status_code != 201:
            raise AppliftingException(response.text, response.status_code)

    def get_product_offers(self, product_uuid: str) -> list[dict[str, str]]:
        headers = {
            "Bearer": f"{self.get_valid_token()}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{self.base_url}/products/{product_uuid}/offers", headers=headers
        )
        if response.status_code != 200:
            if response.status_code == 404:
                self.get_product_offers(product_uuid)
            else:
                raise AppliftingException(response.text, response.status_code)

        offers = response.json()
        return offers

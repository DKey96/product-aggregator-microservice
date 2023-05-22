from unittest import mock

import pytest
from api.models import Offer, Product
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    # Add authentication credentials
    user = User.objects.create_user(username="testuser", password="testpassword")
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.mark.django_db
@override_settings(APPLIFTING_SERVICE_BASE_URL="http://test-service-url")
@mock.patch("api.models.product.AppliftingClient")
def test_create_product(mock_client, api_client):
    url = reverse("product-list")
    data = {"name": "New Product", "description": "New Description"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1

    product = Product.objects.first()
    assert product.name == "New Product"
    assert product.description == "New Description"

    # Verify that the post_save signal was called
    mock_client.return_value.register_new_product.assert_called_once_with(
        product.id, product.name, product.description
    )


@pytest.mark.django_db
@override_settings(APPLIFTING_SERVICE_BASE_URL="http://test-service-url")
@mock.patch("api.models.product.AppliftingClient")
def test_update_product(mock_client, api_client):
    product = Product.objects.create(
        name="Test Product", description="Test Description"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})
    data = {"name": "Updated Product", "description": "Updated Description"}

    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK

    product.refresh_from_db()
    assert product.name == "Updated Product"
    assert product.description == "Updated Description"


@pytest.mark.django_db
@override_settings(APPLIFTING_SERVICE_BASE_URL="http://test-service-url")
@mock.patch("api.models.product.AppliftingClient")
def test_delete_product(mock_client, api_client):
    product = Product.objects.create(
        name="Test Product", description="Test Description"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0


@pytest.mark.django_db
@override_settings(APPLIFTING_SERVICE_BASE_URL="http://test-service-url")
@mock.patch("api.models.product.AppliftingClient")
def test_product_view_set_offers(mock_client, api_client):
    product = Product.objects.create(
        name="Test Product", description="Test Description"
    )
    offer1 = Offer.objects.create(product=product, price=10)
    offer2 = Offer.objects.create(product=product, price=15)

    url = reverse("product-offers", kwargs={"pk": product.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = [
        {
            "id": str(offer1.id),
            "product": str(product.id),
            "price": 10,
            "items_in_stock": 0,
        },
        {
            "id": str(offer2.id),
            "product": str(product.id),
            "price": 15,
            "items_in_stock": 0,
        },
    ]
    assert response.json() == expected_data

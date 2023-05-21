from unittest import mock

import pytest
from api.models import Product
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
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

    # Verify that the post_save signal was called
    mock_client.return_value.register_new_product.assert_called_once_with(
        product.id, product.name, product.description
    )


@pytest.mark.django_db
@mock.patch("api.models.product.AppliftingClient")
def test_delete_product(mock_client, api_client):
    product = Product.objects.create(
        name="Test Product", description="Test Description"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0

    # Verify that the post_save signal was called
    mock_client.return_value.register_new_product.assert_not_called()

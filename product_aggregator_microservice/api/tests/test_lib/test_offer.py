import logging
import uuid
from unittest.mock import patch

import pytest
from api.lib.offer import (
    AppliftingException,
    delete_soldout_offers,
    get_and_create_products_offers,
)
from api.models import Offer, Product

TEST_ID_1 = str(uuid.uuid4())
TEST_ID_2 = str(uuid.uuid4())
TEST_ID_3 = str(uuid.uuid4())


@pytest.fixture
def mock_applifting_client():
    with patch("api.lib.offer.AppliftingClient") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def product():
    with patch("api.models.product.AppliftingClient"):
        return Product.objects.create(name="Product")


@pytest.fixture
def offer(product):
    return Offer.objects.create(
        product=product,
        price=10,
        items_in_stock=0,
    )


@pytest.mark.django_db
def test_get_and_create_products_offers(mock_applifting_client, product):
    mock_applifting_client.get_product_offers.return_value = [
        {"id": TEST_ID_1, "price": 10, "items_in_stock": 5},
        {"id": TEST_ID_2, "price": 15, "items_in_stock": 1},
    ]

    get_and_create_products_offers()

    assert Offer.objects.count() == 2
    assert Offer.objects.filter(product=product).count() == 2

    mock_applifting_client.get_product_offers.assert_called_once_with(
        product_uuid=str(product.id)
    )


@pytest.mark.django_db
def test_get_and_create_products_offers_with_exception(
    mock_applifting_client, caplog, product
):
    mock_applifting_client.get_product_offers.side_effect = AppliftingException(
        "Test exception", 404
    )

    get_and_create_products_offers()

    assert Offer.objects.count() == 0
    assert (
        "There was an error with the communication to the Offer service." in caplog.text
    )
    assert mock_applifting_client.get_product_offers.called


@pytest.mark.django_db
def test_delete_soldout_offers(mock_applifting_client, caplog, offer):
    with caplog.at_level(logging.INFO):
        delete_soldout_offers()

    assert Offer.objects.count() == 0

    assert f"Deleting Offer with ID {str(offer.id)}" in caplog.text


@pytest.mark.django_db
def test_get_and_create_products_offers_empty(mock_applifting_client, caplog, product):
    mock_applifting_client.get_product_offers.return_value = []

    with caplog.at_level(logging.INFO):
        get_and_create_products_offers()

    assert Offer.objects.count() == 0
    assert "Getting offers for 1/1 product" in caplog.text


@pytest.mark.django_db
def test_get_and_create_products_offers_multiple_products(
    mock_applifting_client, product
):
    with patch("api.models.product.AppliftingClient"):
        product1 = Product.objects.create(name="Product 1")
        product2 = Product.objects.create(name="Product 2")

    mock_applifting_client.get_product_offers.side_effect = [
        [{"id": TEST_ID_1, "price": 10, "items_in_stock": 5}],
        [{"id": TEST_ID_2, "price": 15, "items_in_stock": 1}],
        [{"id": TEST_ID_3, "price": 15, "items_in_stock": 1}],
    ]

    get_and_create_products_offers()

    assert Offer.objects.count() == 3
    assert Offer.objects.filter(product=product).count() == 1
    assert Offer.objects.filter(product=product2).count() == 1

    mock_applifting_client.get_product_offers.assert_any_call(
        product_uuid=str(product1.id)
    )
    mock_applifting_client.get_product_offers.assert_any_call(
        product_uuid=str(product2.id)
    )

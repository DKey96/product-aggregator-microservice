from datetime import datetime, timedelta, timezone

import pytest
import requests_mock
from applifting_client.core.client import (
    AppliftingClient,
    AppliftingException,
    ProductDoesNotExist,
)
from applifting_client.models import AppliftingToken
from django.test import override_settings

OVERRIDE_URL = "https://test-service-url"


@pytest.fixture
@override_settings(APPLIFTING_SERVICE_BASE_URL=OVERRIDE_URL)
def applifting_client():
    return AppliftingClient()


@pytest.mark.django_db
def test_refresh_auth_token(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            json={"access_token": "new_token"},
            status_code=201,
        )

        new_token = applifting_client.refresh_auth_token()

        assert new_token == "new_token"


@pytest.mark.django_db
def test_refresh_auth_token_failure(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            text="Bad request",
            status_code=400,
        )

        with pytest.raises(AppliftingException) as context:
            applifting_client.refresh_auth_token()

        assert context.value.status_code == 400
        assert context.value.message == "Bad request"


@pytest.mark.django_db
def test_get_valid_token_existing_token(applifting_client):
    AppliftingToken.objects.create(
        token="valid_token",
        created_at=datetime.now(timezone.utc) - timedelta(minutes=4),
    )
    token = applifting_client.get_valid_token()

    assert token == "valid_token"


@pytest.mark.django_db
def test_get_valid_token_no_token(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            json={"access_token": "new_token"},
            status_code=201,
        )

        token = applifting_client.get_valid_token()

        assert token == "new_token"


@pytest.mark.django_db
def test_register_new_product(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            status_code=201,
            json={"access_token": "valid_token"},
        )
        mock_session.post(
            f"{OVERRIDE_URL}/products/register",
            status_code=201,
        )

        applifting_client.register_new_product("123", "Test Product", "Description")

        assert mock_session.called
        last_request = mock_session.request_history[-1]
        assert last_request.method == "POST"
        assert last_request.url == f"{OVERRIDE_URL}/products/register"
        assert last_request.headers["Bearer"] == "valid_token"
        assert last_request.headers["Content-Type"] == "application/json"
        assert last_request.json() == {
            "id": "123",
            "name": "Test Product",
            "description": "Description",
        }


@pytest.mark.django_db
def test_register_new_product_failure(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            status_code=201,
            json={"access_token": "valid_token"},
        )
        mock_session.post(
            f"{OVERRIDE_URL}/products/register",
            text="Bad request",
            status_code=400,
        )

        with pytest.raises(AppliftingException) as context:
            applifting_client.register_new_product("123", "Test Product", "Description")

        assert context.value.status_code == 400
        assert context.value.message == "Bad request"


@pytest.mark.django_db
def test_get_product_offers(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            status_code=201,
            json={"access_token": "valid_token"},
        )
        mock_session.get(
            f"{OVERRIDE_URL}/products/123/offers",
            json=[{"offer_id": "1", "price": "100"}, {"offer_id": "2", "price": "200"}],
            status_code=200,
        )

        offers = applifting_client.get_product_offers("123")

        assert offers == [
            {"offer_id": "1", "price": "100"},
            {"offer_id": "2", "price": "200"},
        ]


@pytest.mark.django_db
def test_get_product_offers_failure(applifting_client):
    with requests_mock.Mocker() as mock_session:
        mock_session.post(
            f"{OVERRIDE_URL}/auth",
            status_code=201,
            json={"access_token": "valid_token"},
        )
        mock_session.get(
            f"{OVERRIDE_URL}/products/123/offers",
            text="Not found",
            status_code=404,
        )

        with pytest.raises(ProductDoesNotExist) as context:
            applifting_client.get_product_offers("123")

        assert context.value.message == "Not found"

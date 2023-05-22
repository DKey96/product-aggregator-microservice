import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status


@pytest.mark.django_db
def test_valid_registration(client):
    url = reverse("registration")
    data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "User successfully created!"
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_registration_missing_fields(client):
    url = reverse("registration")
    data = {
        "username": "testuser",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


@pytest.mark.django_db
def test_registration_existing_username(client):
    username = "testuser"

    user_model = get_user_model()
    user_model.objects.create(username=username)

    url = reverse("registration")
    data = {
        "username": username,
        "password": "testpassword",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

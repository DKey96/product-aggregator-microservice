from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["username", "password"]
        model = get_user_model()

    def save(self, **kwargs) -> User:
        if self.validated_data.get("username", None) and self.validated_data.get(
            "password", None
        ):
            user_model = get_user_model()
            user = user_model(
                username=self.validated_data["username"],
            )
            user.set_password(self.validated_data["password"])
            user.save()
        else:
            raise ValidationError(
                {"registration": "Must include 'username' and 'password'."}
            )
        return user

    def validate_username(self, username: str) -> str:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
            if user:
                raise serializers.ValidationError(
                    {
                        "email": "User with this username already exists. Do you have an account already?"
                    }
                )
        except ObjectDoesNotExist:
            return username

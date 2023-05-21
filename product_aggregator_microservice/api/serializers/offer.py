from api.models import Offer

from rest_framework import serializers


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Offer


class OffersResponseSerializer(serializers.Serializer):
    offers = serializers.ListField(child=OfferSerializer())

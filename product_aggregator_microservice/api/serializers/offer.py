from api.models import Offer

from rest_framework import serializers


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = "__all__"
        model = Offer

from api.models import Product
from api.serializers.offer import OfferSerializer
from api.serializers.product import ProductSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=True)
    def offers(self, request, *args, **kwargs):
        product = self.get_object()

        serializer = OfferSerializer(
            product.offers.all(),
            many=True,
        )
        return Response(serializer.data)

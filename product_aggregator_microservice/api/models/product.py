import uuid

from applifting_client.core.client import AppliftingClient, AppliftingException
from django.db import models
from django.db.models.signals import post_save

import rest_framework.exceptions


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return

        client = AppliftingClient()
        try:
            client.register_new_product(
                instance.id, instance.name, instance.description
            )
        except AppliftingException:
            instance.delete()
            raise rest_framework.exceptions.ValidationError(
                "Product cannot be saved at the moment. Applifting application is not available."
            )


post_save.connect(Product.post_create, sender=Product)

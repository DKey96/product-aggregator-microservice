import uuid

from django.db import models


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField(default=0)
    items_in_stock = models.IntegerField(default=0)
    product = models.ForeignKey(
        "Product", related_name="offers", on_delete=models.CASCADE
    )

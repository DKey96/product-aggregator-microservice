import logging
import uuid

from api.models import Offer, Product
from applifting_client.core.client import AppliftingClient, AppliftingException

log = logging.getLogger(__name__)


def get_and_create_products_offers() -> None:
    products = Product.objects.all()
    for idx, product in enumerate(products, start=1):
        log.info("Getting offers for %s/%s product", idx, len(products))
        offers = get_offers_by_product_uuid(str(product.id))
        for offer in offers:
            Offer.objects.update_or_create(
                id=uuid.UUID(offer.get("id")).hex,
                defaults={
                    "price": offer.get("price"),
                    "items_in_stock": offer.get("items_in_stock"),
                    "product": product,
                },
            )
    delete_soldout_offers()


def get_offers_by_product_uuid(product_uuid):
    try:
        offers = AppliftingClient().get_product_offers(product_uuid=str(product_uuid))
    except AppliftingException as e:
        log.error(
            "Product with ID %s does not exist in the Offer service. Exception: %s",
            product_uuid,
            e.message,
        )
        offers = []

    return offers


def delete_soldout_offers() -> None:
    for offer in Offer.objects.all():
        if offer.items_in_stock == 0:
            log.info("Deleting Offer with ID %s", str(offer.id))
            offer.delete()

from api.lib.offer import get_and_create_products_offers
from apscheduler.schedulers.background import BackgroundScheduler


def start_get_products_offers_job():
    scheduler = BackgroundScheduler()
    try:
        # 5 seconds are added to the refresh interval due to token limited timeout (5 minutes)
        # of the Offer Microservice
        scheduler.add_job(
            get_and_create_products_offers, "interval", minutes=1, seconds=5, id="offers_job"
        )
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)

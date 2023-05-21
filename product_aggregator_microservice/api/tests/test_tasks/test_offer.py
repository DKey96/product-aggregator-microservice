from unittest.mock import patch

from api.lib.offer import get_and_create_products_offers
from api.tasks.offer import start_get_products_offers_job


@patch("api.tasks.offer.BackgroundScheduler")
def test_start_get_products_offers_job(mock_scheduler):
    scheduler_instance = mock_scheduler.return_value

    start_get_products_offers_job()

    # Assert that the BackgroundScheduler was instantiated and configured correctly
    mock_scheduler.assert_called_once()
    scheduler_instance.add_job.assert_called_once_with(
        get_and_create_products_offers, "interval", minutes=1, id="offers_job"
    )
    scheduler_instance.start.assert_called_once()

    # Simulate KeyboardInterrupt to test scheduler shutdown
    scheduler_instance.shutdown.assert_not_called()  # Assert shutdown not called before KeyboardInterrupt
    mock_scheduler.side_effect = KeyboardInterrupt
    start_get_products_offers_job()
    scheduler_instance.shutdown.assert_called_once_with(wait=False)

import time

import schedule
import structlog

from notifier.api_client import ApiClient, ApiAuth
from notifier.email_client import EmailClient
from notifier.services import (
    fetch_subscriptions,
    fetch_weather,
    format_email_body,
    generate_alerts,
)
from notifier.settings import Settings

logger = structlog.get_logger()


def main() -> None:
    """
    Entrypoint for one cycle of fetching data from the API and sending alerts

    """
    settings = Settings()

    client = ApiClient(settings.subscription_api_url)

    weather_client = ApiClient(
        "https://api.openweathermap.org/data/2.5",
        auth=ApiAuth(api_key=settings.api_key.get_secret_value()),
    )

    email_client = EmailClient(settings.smtp_host)

    logger.msg("Fetching subscriptions...")

    for sub in fetch_subscriptions(client):
        sub_logger = logger.bind(
            user_email=sub.email,
            subscription_city=sub.city,
            subscription_country_code=sub.country_code,
        )

        weather = fetch_weather(weather_client, sub.city, sub.country_code)

        sub_logger.msg("Fetched weather condition", **weather.dict())

        alerts = generate_alerts(sub.conditions, weather)
        sub_logger.msg("Generated alerts", alerts=alerts)
        email_client.send_email(
            sub.email,
            subject=f"Weather Notification for {sub.city}",
            body=format_email_body(alerts, sub.city, sub.country_code),
        )
        sub_logger.msg("Email sent")


def scheduled_run(schedule_minutes=1):
    """
    Scheduler entrypoint. Schedules the main function to run every `schedule_minutes`

    Parameters
    ----------
    schedule_minutes
        The schedule interval

    Returns
    -------
    None
    """
    logger.msg("Started notifying...")
    schedule.every(schedule_minutes).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    scheduled_run()

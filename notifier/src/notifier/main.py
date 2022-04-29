import smtplib
import time

import schedule

from notifier.client import ApiClient, Auth, EmailClient
from notifier.services import fetch_subscriptions, fetch_weather, format_email_body, \
    generate_alerts

import structlog

from notifier.settings import Settings

logger = structlog.get_logger()


def main():
    settings = Settings()

    client = ApiClient(settings.subscription_api_url)

    weather_client = ApiClient("https://api.openweathermap.org/data/2.5",
                               auth=Auth(api_key=settings.api_key.get_secret_value()))

    email_client = EmailClient(smtplib.SMTP(settings.smtp_host))

    logger.msg("Fetching subscriptions...")

    for sub in fetch_subscriptions(client):
        sub_logger = logger.bind(user_email=sub.email,
                                 subscription_city=sub.city,
                                 subscription_country_code=sub.country_code)

        weather = fetch_weather(weather_client, sub)

        sub_logger.msg("Fetched weather condition", **weather.dict())

        alerts = generate_alerts(sub, weather)
        sub_logger.msg("Generated alerts", alerts=alerts)
        email_client.send_email(sub.email,
                                subject=f"Weather Notification for {sub.city}",
                                body=format_email_body(alerts, sub))
        sub_logger.msg("Email sent")


def run():
    logger.msg("Started notifying...")
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()

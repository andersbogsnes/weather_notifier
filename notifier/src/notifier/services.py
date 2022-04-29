import operator
import textwrap
from typing import Any, Optional

from notifier.client import ApiClientInterface
from notifier.schemas import Subscription, WeatherConditions, Condition


def fetch_subscriptions(client: ApiClientInterface) -> list[Subscription]:
    subscription_data = client.get("/subscriptions")
    return [Subscription.parse_obj(data) for data in subscription_data]


def fetch_weather(client: ApiClientInterface, subscription: Subscription) -> WeatherConditions:
    query = subscription.city

    if subscription.country_code:
        query = f"{query},{subscription.country_code}"

    data = client.get("/weather", params={
        "appid": client.auth.api_key,
        "q": query,
        "units": "metric"
    })

    return WeatherConditions.parse_obj(data["main"])


def format_message(alert: dict, subscription: Subscription) -> str:
    op_mappings = {
        "gt": "greater than",
        "ge": "greater than or equal to",
        "lt": "less than",
        "le": "less than or equal to",
        "eq": "equal to"
    }

    return textwrap.dedent(f"""
            The {alert['condition']} in {subscription.city} is now {alert['actual']}.
            This is {op_mappings[alert['op']]} your threshold of {alert['threshold']}
         """)


def format_email_body(alerts: list[dict], subscription: Subscription) -> str:
    notifications = '\n'.join(format_message(alert, subscription) for alert in alerts)

    return textwrap.dedent(
        f"""
Hello,

You've received the following weather notifications:
        
{notifications}
""")


def compare_threshold(condition: Condition,
                      weather_condition: WeatherConditions) -> Optional[dict[str, Any]]:
    actual = weather_condition.dict()[condition.condition]

    op = getattr(operator, condition.op)

    if op(actual, condition.threshold):
        return {
            **condition.dict(),
            "actual": actual
        }


def generate_alerts(subscription: Subscription, weather: WeatherConditions) -> list[dict[str, Any]]:
    return [compare_threshold(condition, weather)
            for condition
            in subscription.conditions
            if compare_threshold(condition, weather) is not None]

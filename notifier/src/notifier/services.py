import operator
import textwrap
from typing import Optional, TypedDict

from notifier.api_client import ApiClientInterface
from notifier.schemas import Subscription, WeatherConditions, AlertCondition


class AlertDict(TypedDict):
    condition: str
    actual: str
    threshold: float | int
    op: str


class WeatherConditionDict(TypedDict):
    temp: float
    pressure: float
    humidity: float


def fetch_subscriptions(client: ApiClientInterface) -> list[Subscription]:
    """
    Get all subscriptions from the API

    Parameters
    ----------
    client
        An API client which can get data from an API
    Returns
    -------
    list of Subscriptions
        A list of all subscriptions returned from the API

    """
    # TODO: Implement streaming responses / paginated batches
    subscription_data = client.get("/subscriptions")
    return [Subscription.parse_obj(data) for data in subscription_data]


def fetch_weather(
    client: ApiClientInterface, city: str, country_code: Optional[str] = None
) -> WeatherConditions:
    """
    Get the weather conditions for a given location defined by the subscription

    Parameters
    ----------
    client
        An instance of an ApiClient which can get data from the weather api
    city
        The city to fetch the data for
    country_code
        An optional country code to get the correct city in case of multiple cities with the same
        name in different countries

    Returns
    -------
    WeatherConditions

    """
    query = city

    if country_code:
        query = f"{query},{country_code}"

    data = client.get(
        "/weather", params={"appid": client.auth.api_key, "q": query, "units": "metric"}
    )

    return WeatherConditions.parse_obj(data["main"])


def format_alert_message(
    alert: AlertDict, city: str, country_code: Optional[str] = None
) -> str:
    """
    Returns a formatted string with for the alert. Used to format the message appropriately
    for the end-user

    Parameters
    ----------
    alert
        A dictionary of alert-related information
    city
        The city in which the alert took place
    country_code
        The country in which the alert took place

    Returns
    -------
    str
        The formatted alert message string
    """
    op_mappings = {
        "gt": "greater than",
        "ge": "greater than or equal to",
        "lt": "less than",
        "le": "less than or equal to",
        "eq": "equal to",
    }

    location = city if country_code is None else f"{city}, {country_code}"
    str_op = op_mappings[alert["op"]]

    return textwrap.dedent(
        f"""
            The {alert['condition']} in {location} is now {alert['actual']}.
            This is {str_op} your threshold of {alert['threshold']}
         """
    )


def format_email_body(
    alerts: list[AlertDict], city: str, country_code: Optional[str] = None
) -> str:
    """
    Format the body of the email with all alerts

    Parameters
    ----------
    alerts
        A list of all alerts to put into the email
    city
        The city where the alert took place
    country_code
        Optionally, the country where the alert took place

    Returns
    -------
    str
        The formatted email body
    """
    notifications = "\n".join(
        format_alert_message(alert, city=city, country_code=country_code)
        for alert in alerts
    )

    return textwrap.dedent(
        f"""
Hello,

You've received the following weather notifications:

{notifications}
"""
    )


def compare_threshold(
    condition: str, op: str, threshold: float, weather_condition: WeatherConditionDict
) -> Optional[AlertDict]:
    """
    Compares the given condition with actual weather conditions and returns an alert
    if the weather matches the trigger

    Parameters
    ----------
    condition
        What weather condition to compare against
    op
        The comparison method
    threshold
        The threshold for alerting
    weather_condition
        A dictionary of weather conditions

    Returns
    -------
    None or an alert dict
    """
    actual: str = weather_condition[condition]  # type: ignore

    op_func = getattr(operator, op)

    if op_func(actual, threshold):
        return {
            "condition": condition,
            "op": op,
            "threshold": threshold,
            "actual": actual,
        }


def generate_alerts(
    conditions: list[AlertCondition], weather: WeatherConditions
) -> list[AlertDict]:
    """
    Generate all relevant alerts based on the comparison between each condition and the
    weather

    Parameters
    ----------
    conditions
        A list of alert conditions
    weather
        The weather conditions of the requested location

    Returns
    -------
    list of dict
        Returns a list of alert dictionaries
    """
    all_comparisons = [
        compare_threshold(**condition.dict(), weather_condition=weather.dict())
        for condition in conditions
    ]
    return [c for c in all_comparisons if c is not None]

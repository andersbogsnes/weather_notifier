from typing import Optional, Any

import pytest
import attr

from notifier.api_client import JsonResponseType, ApiAuth
from notifier import services
from notifier.schemas import Subscription


@attr.define()
class StubApiClient:
    data: JsonResponseType
    auth: ApiAuth = ApiAuth(api_key="123")

    def get(self, endpoint: str, params: Optional[dict] = None) -> JsonResponseType:
        return self.data


@pytest.fixture(scope="session")
def subscription_data() -> dict:
    return {
        "email": "tester@test.com",
        "city": "London",
        "country_code": "GB",
        "conditions": [
            {"condition": "temp", "op": "gt", "threshold": 0},
            {"condition": "pressure", "op": "lt", "threshold": 5},
        ],
        "subscription_uuid": "dae77ff3-6d26-4c56-ba22-4eb137e9be92",
    }


@pytest.fixture(scope="session")
def subscription(subscription_data: dict) -> Subscription:
    return Subscription.parse_obj(subscription_data)


@pytest.fixture(scope="session")
def weather_data() -> dict[str, Any]:
    return {
        "coord": {"lon": -122.08, "lat": 37.39},
        "weather": [
            {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
        ],
        "base": "stations",
        "main": {
            "temp": 282.55,
            "feels_like": 281.86,
            "temp_min": 280.37,
            "temp_max": 284.26,
            "pressure": 1023,
            "humidity": 100,
        },
        "visibility": 10000,
        "wind": {"speed": 1.5, "deg": 350},
        "clouds": {"all": 1},
        "dt": 1560350645,
        "sys": {
            "type": 1,
            "id": 5122,
            "message": 0.0139,
            "country": "US",
            "sunrise": 1560343627,
            "sunset": 1560396563,
        },
        "timezone": -25200,
        "id": 420006353,
        "name": "Mountain View",
        "cod": 200,
    }


def test_fetch_subscriptions_returns_list_of_subscriptions(subscription_data: dict):
    client = StubApiClient(data=[subscription_data])

    subs = services.fetch_subscriptions(client)

    assert subs == [Subscription.parse_obj(subscription_data)]


def test_fetch_weather_returns_correct_conditions(
    weather_data: dict, subscription: Subscription
):
    client = StubApiClient(data=weather_data)

    conditions = services.fetch_weather(
        client, subscription.city, subscription.country_code
    )

    for condition in ["temp", "pressure", "humidity"]:
        assert conditions.dict()[condition] == weather_data["main"][condition]

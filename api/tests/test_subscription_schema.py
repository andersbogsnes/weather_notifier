import itertools

import pytest
from pydantic import BaseModel, ValidationError

from weather_notifier.subscriptions import schemas

in_schema_data = [
    {
        "email": "my@fake.com",
        "country_code": "DK",
        "city": "Copenhagen",
        "conditions": [
            {"op": "gt", "condition": "temp", "threshold": 20},
            {"op": "lt", "condition": "humidity", "threshold": 5},
        ],
    },
    {
        "email": "my@fake.com",
        "country_code": "DK",
        "city": "Copenhagen",
        "conditions": [{"op": "gt", "condition": "temp", "threshold": 20}],
    },
    {
        "email": "my@fake.com",
        "country_code": "DK",
        "city": "Copenhagen",
        "conditions": [],
    },
]

subscription_out_data = [
    {
        "email": "my@fake.com",
        "country_code": "DK",
        "city": "Copenhagen",
        "subscription_uuid": "a600d79c-6bab-45ec-b285-77ccd67a894c",
        "conditions": [
            {
                "op": "gt",
                "condition": "temp",
                "threshold": 20,
            },
            {
                "op": "lt",
                "condition": "humidity",
                "threshold": 5,
            },
        ],
    },
    {
        "email": "my@fake.com",
        "country_code": "DK",
        "city": "Copenhagen",
        "subscription_uuid": "a600d79c-6bab-45ec-b285-77ccd67a894c",
        "conditions": [
            {
                "op": "gt",
                "condition": "temp",
                "threshold": 20,
            }
        ],
    },
]


@pytest.mark.parametrize(
    "in_data,schema",
    itertools.chain(
        [(data, schemas.SubscriptionInSchema) for data in in_schema_data],
        [(data, schemas.SubscriptionOutSchema) for data in subscription_out_data],
    ),
)
def test_valid_subscription_schemas(in_data, schema):
    assert schema.parse_obj(in_data)

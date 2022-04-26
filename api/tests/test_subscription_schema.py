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
                "condition_uuid": "42530866-76fd-4d0e-aa89-20d981c1e7c8",
                "op": "gt",
                "condition": "temp",
                "threshold": 20,
            },
            {
                "condition_uuid": "74d5cee3-e884-45f3-ad57-de97f0b5c308",
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
                "condition_uuid": "42530866-76fd-4d0e-aa89-20d981c1e7c8",
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


@pytest.mark.parametrize("schema", [schemas.ConditionOut, schemas.ConditionUpdate])
def test_condition_schema_fails_with_invalid_uuid(schema: BaseModel):
    with pytest.raises(ValidationError) as e:
        schema.parse_obj(
            {
                "condition_uuid": "invalid-uuid",
                "op": "lt",
                "threshold": 5,
                "condition": "temp",
            }
        )
    assert e.value.errors()[0]["loc"][0] == "condition_uuid"

import uuid

import sqlalchemy as sa

from weather_notifier.db import mapper_registry


@mapper_registry.mapped
class Subscription:
    __tablename__ = "subscriptions"

    id: int = sa.Column(sa.Integer, primary_key=True)
    subscription_uuid: str = sa.Column(sa.VARCHAR(36), unique=True, index=True)
    country_code: str = sa.Column(sa.VARCHAR(2))
    city: str = sa.Column(sa.VARCHAR(100))
    email: str = sa.Column(sa.VARCHAR(250))
    conditions: list[dict] = sa.Column(sa.JSON())

    def __init__(
        self,
        country_code: str,
        city: str,
        email: str,
        subscription_uuid: str,
        conditions: list[dict],
    ):
        self.subscription_uuid = subscription_uuid
        self.country_code = country_code
        self.city = city
        self.email = email
        self.conditions = conditions

    @classmethod
    def from_dict(cls, data: dict) -> "Subscription":
        return cls(
            subscription_uuid=data.get("subscription_uuid", str(uuid.uuid4())),
            country_code=data["country_code"],
            city=data["city"],
            email=data["email"],
            conditions=data["conditions"],
        )

    def update_from_dict(self, data: dict) -> "Subscription":
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
        return self

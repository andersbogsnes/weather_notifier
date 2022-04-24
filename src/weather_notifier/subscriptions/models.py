from decimal import Decimal

from sqlalchemy.orm import relationship

from weather_notifier.db import mapper_registry
import sqlalchemy as sa


@mapper_registry.mapped
class Condition:
    __tablename__ = "conditions"

    id: int = sa.Column(sa.Integer, primary_key=True)
    subscription_id: int = sa.Column(sa.Integer, sa.ForeignKey("subscriptions.id"))
    condition_uuid: str = sa.Column(sa.VARCHAR(25))
    condition: str = sa.Column(sa.VARCHAR(25))
    op: str = sa.Column(sa.VARCHAR(3))
    threshold: Decimal = sa.Column(sa.Numeric(19, 4))


@mapper_registry.mapped
class Subscription:
    __tablename__ = "subscriptions"

    id: int = sa.Column(sa.Integer, primary_key=True)
    subscription_uuid: str = sa.Column(sa.VARCHAR(36), unique=True, index=True)
    country_code: str = sa.Column(sa.VARCHAR(2))
    city: str = sa.Column(sa.VARCHAR(100))
    email: str = sa.Column(sa.VARCHAR(250))

    conditions = relationship("Condition", cascade="all, delete")

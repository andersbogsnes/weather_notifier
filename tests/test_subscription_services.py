from typing import Callable

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from weather_notifier.db import mapper_registry
from weather_notifier.exceptions import EntityNotFoundException
from weather_notifier.settings import Settings
import sqlalchemy as sa

from weather_notifier.subscriptions import services, models, schemas


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    return sa.create_engine(
        settings.db.db_url.get_secret_value(),
        future=True,
        connect_args={"check_same_thread": False},
    )


@pytest.fixture(scope="session")
def create_tables(engine: Engine) -> None:
    mapper_registry.metadata.create_all(engine)
    yield
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture()
def session(engine: Engine, create_tables) -> Session:
    with Session(engine) as session:
        with session.begin():
            yield session
            session.rollback()


@pytest.fixture()
def subscription_factory() -> Callable[[], models.Subscription]:
    def new_subscription() -> models.Subscription:
        return models.Subscription(
            subscription_uuid="4301583f-05a3-4b55-bf32-048975dfedff",
            email="test@test.email.com",
            country_code="DK",
            city="Copenhagen",
            conditions=[
                models.Condition(
                    condition_uuid="03217e65-44bf-4201-a21b-77998d0fff6a",
                    op="lt",
                    threshold=0,
                    condition="temp",
                )
            ],
        )

    return new_subscription


@pytest.fixture()
def subscription_db(
    subscription_factory: Callable[[], models.Subscription], session: Session
) -> models.Subscription:
    sub = subscription_factory()
    session.add(sub)
    return sub


@pytest.fixture()
def subscription_update_schema(
    subscription_db: models.Subscription,
) -> schemas.SubscriptionUpdateInSchema:
    return schemas.SubscriptionUpdateInSchema.parse_obj(
        {
            "email": "my@new-email.com",
            "city": subscription_db.city,
            "country_code": subscription_db.country_code,
            "conditions": [
                schemas.ConditionUpdate.parse_obj(
                    {
                        "condition_uuid": obj.condition_uuid,
                        "condition": obj.condition,
                        "op": obj.op,
                        "threshold": obj.threshold,
                    }
                )
                for obj in subscription_db.conditions
            ],
        }
    )


def test_get_all_subscriptions_when_empty_returns_empty_list(session: Session):
    assert services.get_all_subscriptions(session) == []


def test_get_all_subscriptions_returns_list_of_subscriptions(
    session: Session, subscription_db: models.Subscription
):
    assert services.get_all_subscriptions(session) == [subscription_db]


def test_get_a_subscription_returns_single_subscription(
    session: Session, subscription_db: models.Subscription
):
    result = services.get_subscription_by_uuid(
        session, subscription_db.subscription_uuid
    )
    assert result == subscription_db


def test_delete_subscription_removes_correct_subscription(
    session: Session, subscription_db: models.Subscription
):
    current = services.get_subscription_by_uuid(
        session, subscription_db.subscription_uuid
    )
    assert current == subscription_db

    services.delete_subscription_by_uuid(session, subscription_db.subscription_uuid)

    result = services.get_subscription_by_uuid(
        session, subscription_db.subscription_uuid
    )
    assert result is None


def test_update_subscription_updates_data_correctly(
    session: Session,
    subscription_db: models.Subscription,
    subscription_update_schema: schemas.SubscriptionUpdateInSchema,
):
    current = services.get_subscription_by_uuid(
        session, subscription_db.subscription_uuid
    )
    assert current == subscription_db

    result = services.update_subscription_by_uuid(
        session, subscription_db.subscription_uuid, subscription_update_schema
    )

    assert result.email == "my@new-email.com"

    result = services.get_subscription_by_uuid(
        session, subscription_db.subscription_uuid
    )
    assert result.email == "my@new-email.com"


def test_update_subscription_with_incorrect_ids_raises(
    session: Session, subscription_db: subscription_db, subscription_update_schema
):
    with pytest.raises(
        EntityNotFoundException, match="Subscription: clearly-wrong-uuid not found"
    ):
        services.update_subscription_by_uuid(
            session, "clearly-wrong-uuid", subscription_update_schema
        )

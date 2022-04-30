from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from weather_notifier.exceptions import EntityNotFoundException
from weather_notifier.subscriptions import schemas
from weather_notifier.subscriptions.models import Subscription
from weather_notifier.subscriptions.schemas import SubscriptionInSchema


def get_all_subscriptions(session: Session) -> list[Subscription]:
    """
    Get all subscriptions from the database

    Parameters
    ----------
    session
        An open session to the database

    Returns
    -------
    list of Subscriptions

    """
    sql = sa.select(Subscription)

    return session.execute(sql).scalars().all()


def get_subscription_by_uuid(
    session: Session, subscription_uuid: str
) -> Optional[Subscription]:
    """
    Get a given subscription by uuid from the database. Returns None if the subscription doesn't
    exist

    Parameters
    ----------
    session
        An open session to the database
    subscription_uuid
        The UUID of the subscription

    Returns
    -------
    Subscription or None
    """
    sql = sa.select(Subscription).filter_by(subscription_uuid=subscription_uuid)

    return session.execute(sql).scalar_one_or_none()


def create_subscription(
    session: Session, subscription: SubscriptionInSchema
) -> Subscription:
    """
    Create a new subscription

    Parameters
    ----------
    session
        An open session to the database
    subscription
        A Pydantic schema representing a new subscription

    Returns
    -------
    The saved Subscription
    """

    new_subscription = Subscription.from_dict(subscription.dict())
    session.add(new_subscription)
    return new_subscription


def delete_subscription_by_uuid(session: Session, subscription_uuid: str) -> None:
    subscription = get_subscription_by_uuid(session, subscription_uuid)
    session.delete(subscription)


def update_subscription_by_uuid(
    session: Session,
    subscription_uuid: str,
    subscription: schemas.SubscriptionInSchema,
) -> Optional[Subscription]:
    if not (
        existing_subscription := get_subscription_by_uuid(session, subscription_uuid)
    ):
        raise EntityNotFoundException(f"Subscription: {subscription_uuid}")
    existing_subscription = existing_subscription.update_from_dict(subscription.dict())
    session.add(existing_subscription)
    return existing_subscription

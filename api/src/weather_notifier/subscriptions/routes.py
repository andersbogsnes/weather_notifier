from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from weather_notifier.db import get_session
from weather_notifier.exceptions import EntityNotFoundException
from weather_notifier.subscriptions import schemas, services

router = APIRouter(tags=["Subscription"])

@router.get("/subscriptions", response_model=list[schemas.SubscriptionOutSchema])
def get_subscriptions(session: Session = Depends(get_session)):
    """Get all subscriptions"""
    return services.get_all_subscriptions(session)


@router.get(
    "/subscription/{subscription_uuid}", response_model=schemas.SubscriptionOutSchema
)
def get_subscription_for_id(
        subscription_uuid: str, session: Session = Depends(get_session)
):
    """Get a given subscription"""
    if (
            subscription := services.get_subscription_by_uuid(session, subscription_uuid)
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription Not found"
        )
    return subscription


@router.post(
    "/subscriptions",
    response_model=schemas.SubscriptionOutSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_new_subscription(
        subscription: schemas.SubscriptionInSchema, session: Session = Depends(get_session)
):
    """Create a new subscription"""
    return services.create_subscription(session, subscription)


@router.put(
    "/subscription/{subscription_uuid}",
    response_model=schemas.SubscriptionOutSchema,
    status_code=status.HTTP_200_OK,
)
def update_subscription(
        subscription_uuid: str,
        update_data: schemas.SubscriptionInSchema,
        session: Session = Depends(get_session),
):
    try:
        return services.update_subscription_by_uuid(
            session, subscription_uuid, update_data
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=e.code, detail=str(e))


@router.delete(
    "/subscription/{subscription_uuid}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_subscription(
        subscription_uuid: str, session: Session = Depends(get_session)
):
    """Delete an existing subscription"""

    return services.delete_subscription_by_uuid(session, subscription_uuid)

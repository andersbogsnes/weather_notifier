import uuid
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, EmailStr, validator


class ConditionEnum(str, Enum):
    temp = "temp"
    pressure = "pressure"
    humidity = "humidity"


class OpEnum(str, Enum):
    gt = "gt"
    lt = "lt"
    eq = "eq"
    gte = "gte"
    lte = "lte"


class Condition(BaseModel):
    """Base Condition schema"""

    condition: ConditionEnum
    op: OpEnum
    threshold: Decimal


class ConditionUpdate(Condition):
    condition_uuid: str

    @validator("condition_uuid")
    def valid_uuid(cls, v):
        uuid.UUID(v)
        return v


class ConditionOut(ConditionUpdate):
    class Config:
        orm_mode = True


class SubscriptionBaseSchema(BaseModel):
    email: EmailStr
    city: str
    country_code: str

    @validator("country_code")
    def valid_country_code(cls, v):
        if len(v) != 2:
            raise ValueError("Must be a valid 2-letter country code")
        return v


class SubscriptionInSchema(SubscriptionBaseSchema):
    conditions: list[Condition]


class SubscriptionUpdateInSchema(SubscriptionBaseSchema):
    conditions: list[ConditionUpdate]


class SubscriptionOutSchema(SubscriptionBaseSchema):
    subscription_uuid: str
    conditions: list[ConditionOut]

    @validator("subscription_uuid")
    def valid_uuid(cls, v):
        uuid.UUID(v)
        return v

    class Config:
        orm_mode = True

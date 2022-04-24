import uuid
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, EmailStr, constr, validator


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


class SubscriptionInSchema(BaseModel):
    email: EmailStr
    city: str
    country_code: constr(min_length=2, max_length=2)
    conditions: list[Condition]


class SubscriptionUpdateInSchema(SubscriptionInSchema):
    conditions: list[ConditionUpdate]


class SubscriptionOutSchema(SubscriptionUpdateInSchema):
    subscription_uuid: str
    conditions: list[ConditionOut]

    @validator("subscription_uuid")
    def valid_uuid(cls, v):
        uuid.UUID(v)
        return v

    class Config:
        orm_mode = True

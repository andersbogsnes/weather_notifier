from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, UUID4, EmailStr


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
    condition: ConditionEnum
    op: OpEnum
    threshold: Decimal


class ConditionOut(Condition):
    class Config:
        orm_mode = True


class SubscriptionInSchema(BaseModel):
    email: EmailStr
    city: str
    country: str
    conditions: list[Condition]


class SubscriptionOutSchema(SubscriptionInSchema):
    subscription_uuid: UUID4
    conditions: list[ConditionOut]

    class Config:
        orm_mode = True

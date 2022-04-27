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


class ConditionSchema(BaseModel):
    """Base Condition schema"""

    condition: ConditionEnum
    op: OpEnum
    threshold: float


class SubscriptionInSchema(BaseModel):
    email: EmailStr
    city: str
    country_code: str
    conditions: list[ConditionSchema]

    @validator("country_code")
    def valid_country_code(cls, v):
        if len(v) != 2:
            raise ValueError("Must be a valid 2-letter country code")
        return v


class SubscriptionOutSchema(SubscriptionInSchema):
    subscription_uuid: str

    @validator("subscription_uuid")
    def valid_uuid(cls, v):
        uuid.UUID(v)
        return v

    class Config:
        orm_mode = True

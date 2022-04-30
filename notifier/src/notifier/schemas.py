from pydantic import BaseModel, EmailStr, validator


class AlertCondition(BaseModel):
    """
    Represents a given alert condition

    Parameters
    ----------
    op
        The comparison operation as a two-character code
    threshold
        The threshold at which an alert occurs
    condition
        The weather condition to measure
    """

    op: str
    threshold: float
    condition: str

    @validator("op")
    def op_should_be_two_chars(cls, v):
        if len(v) != 2:
            raise ValueError("Op should be exactly 2 characters")
        return v

    @validator("condition")
    def condition_should_be_in_list(cls, v):
        possible_conditions = ["temp", "pressure", "humidity"]
        if v not in possible_conditions:
            raise ValueError(f"{v} must be one of {possible_conditions}")
        return v


class Subscription(BaseModel):
    """
    Represents a given Subscription to weather alerting

    Parameters
    ----------
    email
        The email of the user
    city
        The city to alert for
    country_code
        The country to alert for as a 2-digit country code
    conditions
        A list of subscribed AlertConditions
    """

    email: EmailStr
    city: str
    country_code: str
    conditions: list[AlertCondition]

    @validator("country_code")
    def country_code_must_be_2_chars(cls, v):
        if len(v) != 2:
            raise ValueError("Country code must be exactly 2 chars")
        return v


class WeatherConditions(BaseModel):
    """
    Represents the actual weather conditions of a location
    """

    temp: float
    pressure: float
    humidity: float

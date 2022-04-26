from pydantic import BaseModel, EmailStr


class Condition(BaseModel):
    op: str
    threshold: float
    condition: str


class Subscription(BaseModel):
    email: EmailStr
    city: str
    country_code: str
    conditions: list[Condition]


class WeatherConditions(BaseModel):
    temp: float
    pressure: float
    humidity: float


class Weather(BaseModel):
    main: list[WeatherConditions]

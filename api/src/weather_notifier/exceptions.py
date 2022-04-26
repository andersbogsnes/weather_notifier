class WeatherNotifierException(Exception):
    def __init__(self, message: str, code=500):
        self.code = code
        super().__init__(message)


class EntityNotFoundException(WeatherNotifierException):
    def __init__(self, entity_name: str):
        super().__init__(f"{entity_name} not found", code=404)

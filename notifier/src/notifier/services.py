from notifier.client import ApiClient
from notifier.schemas import Subscription


def fetch_subscriptions(client: ApiClient) -> list[Subscription]:
    subscription_data = client.get("/subscriptions")
    return [Subscription.parse_obj(data) for data in subscription_data]

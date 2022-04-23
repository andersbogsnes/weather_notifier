from unittest.mock import MagicMock, ANY

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from requests import Response

from weather_notifier.subscriptions import services
from weather_notifier.subscriptions.models import Subscription, Condition
from weather_notifier.subscriptions.schemas import SubscriptionInSchema


@pytest.fixture()
def data() -> dict:
    return {
        "email": "test@test.com",
        "city": "Copenhagen",
        "country": "DK",
        "conditions": [{
            "condition": "temp",
            "op": "gt",
            "threshold": 0
        }]
    }


@pytest.fixture()
def subscription(data: dict) -> Subscription:
    return Subscription(
        subscription_uuid="dded2381-fb90-41dc-8f10-115cd1ee95dc",
        email=data["email"],
        city=data["city"],
        country=data["country"],
        conditions=[Condition(**c) for c in data["conditions"]]
    )


class TestCreateSubscription:
    @pytest.fixture()
    def mock_service(self, mocker: MockerFixture, subscription: Subscription):
        return mocker.patch.object(services, "create_subscription",
                                   return_value=subscription)

    @pytest.fixture()
    def response(self, data: dict, client: TestClient, mock_service) -> Response:
        return client.post("/subscriptions", json=data)

    def test_returns_correct_status_code(self, response: Response):
        assert response.status_code == status.HTTP_201_CREATED

    def test_returns_correct_data(self, response: Response, data: dict):
        response_data = response.json()
        del response_data["subscription_uuid"]
        assert response_data == data

    def test_calls_service_with_correct_data(self,
                                             response: Response,
                                             mock_service: MagicMock,
                                             data: dict):
        mock_service.assert_called_once_with(ANY, SubscriptionInSchema(**data))


class TestGetAllSubscription:
    @pytest.fixture()
    def mock_service(self, mocker: MockerFixture,
                     subscription: Subscription) -> MagicMock:
        return mocker.patch.object(services, "get_all_subscriptions",
                                   return_value=[subscription])

    @pytest.fixture()
    def response(self, client: TestClient, mock_service) -> Response:
        return client.get("/subscriptions")

    def test_returns_correctly_formatted_json(self, response: Response, subscription:
    Subscription, data: dict):
        assert response.json() == [
            {**data, 'subscription_uuid': 'dded2381-fb90-41dc-8f10-115cd1ee95dc'}
        ]

    def test_has_correct_statuscode(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_calls_service_with_correct_data(self, response: Response, mock_service: MagicMock):
        mock_service.assert_called_once_with(ANY)


class TestGetAllSubscriptionsNoSubscriptions:
    @pytest.fixture()
    def mock_service(self, mocker: MockerFixture) -> MagicMock:
        return mocker.patch.object(services, "get_all_subscriptions", return_value=[])

    @pytest.fixture()
    def response(self, client: TestClient, mock_service: MagicMock) -> Response:
        return client.get("/subscriptions")

    def test_returns_empty_when_no_subscriptions(self, response: Response):
        assert response.json() == []

    def test_is_code_200_ok_when_no_subscriptions(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_calls_service_with_correct_data(self, response: Response, mock_service: MagicMock):
        mock_service.assert_called_once_with(ANY)


class TestGetSubscriptionByUUID:
    @pytest.fixture()
    def mock_service(self, mocker: MockerFixture, subscription: Subscription) -> MagicMock:
        return mocker.patch.object(services, "get_subscription_by_uuid", return_value=subscription)

    @pytest.fixture()
    def response(self, client: TestClient, subscription, mock_service: MagicMock) -> Response:
        return client.get(f"/subscription/{subscription.subscription_uuid}")

    def test_returns_200_ok(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_json(self, response: Response, data: dict, subscription: Subscription):
        assert response.json() == {**data, "subscription_uuid": subscription.subscription_uuid}


class TestGetSubscriptionByUUIDWhenDoesntExist:
    @pytest.fixture()
    def mock_service(self, class_mocker: MockerFixture) -> MagicMock:
        return class_mocker.patch.object(services, "get_subscription_by_uuid", return_value=None)

    @pytest.fixture()
    def response(self, client: TestClient, mock_service: MagicMock) -> Response:
        return client.get("/subscription/missing-uuid")

    def test_returns_404_not_found(self, response: Response):
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_correct_json(self, response: Response):
        assert response.json() == {"detail": "Subscription Not found"}

    def test_service_called_with_uuid(self, mock_service: MagicMock, response: Response):
        mock_service.assert_called_once_with(ANY, "missing-uuid")


class TestDeleteSubscription:
    @pytest.fixture()
    def mock_service(self, mocker: MockerFixture):
        return mocker.patch.object(services, "delete_subscription_by_uuid", return_value=None)

    @pytest.fixture()
    def response(self, client: TestClient, mock_service: MagicMock, subscription: Subscription):
        return client.delete(f"/subscription/{subscription.subscription_uuid}")

    def test_returns_204_no_content(self, response: Response):
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_returns_empty_body(self, response: Response):
        assert response.text == ""

    def test_service_called_with_session(self, mock_service: MagicMock, response: Response,
                                         subscription: Subscription):
        mock_service.assert_called_once_with(ANY, subscription.subscription_uuid)

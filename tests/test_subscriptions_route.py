from unittest.mock import MagicMock, ANY

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from requests import Response

from weather_notifier.subscriptions import services
from weather_notifier.subscriptions import models
from weather_notifier.subscriptions import schemas


@pytest.fixture(scope="session")
def data() -> dict:
    return {
        "email": "test@test.com",
        "city": "Copenhagen",
        "country_code": "DK",
        "conditions": [{"condition": "temp", "op": "gt", "threshold": 0}],
    }


@pytest.fixture(scope="session")
def out_data(data: dict) -> dict:
    return {
        **data,
        "subscription_uuid": "dded2381-fb90-41dc-8f10-115cd1ee95dc",
        "conditions": [
            {
                **data["conditions"][0],
                "condition_uuid": "9dcce4f1-cfb5-431f-aadd-2fc7e9c7ed57",
            }
        ],
    }


@pytest.fixture(scope="session")
def subscription(out_data: dict) -> models.Subscription:
    return models.Subscription(
        subscription_uuid=out_data["subscription_uuid"],
        email=out_data["email"],
        city=out_data["city"],
        country_code=out_data["country_code"],
        conditions=[models.Condition(**c) for c in out_data["conditions"]],
    )


class TestCreateSubscription:
    @pytest.fixture(scope="class")
    def mock_service(
        self, class_mocker: MockerFixture, subscription: models.Subscription
    ):
        return class_mocker.patch.object(
            services, "create_subscription", return_value=subscription
        )

    @pytest.fixture(scope="class")
    def response(self, data: dict, client: TestClient, mock_service) -> Response:
        return client.post("/subscriptions", json=data)

    def test_returns_correct_status_code(self, response: Response):
        assert response.status_code == status.HTTP_201_CREATED

    def test_returns_correct_data(self, response: Response, out_data: dict):
        response_data = response.json()
        assert response_data == out_data

    def test_calls_service_with_correct_data(
        self, response: Response, mock_service: MagicMock, data: dict
    ):
        mock_service.assert_called_once_with(ANY, schemas.SubscriptionInSchema(**data))


class TestGetAllSubscription:
    @pytest.fixture(scope="class")
    def mock_service(
        self, class_mocker: MockerFixture, subscription: models.Subscription
    ) -> MagicMock:
        return class_mocker.patch.object(
            services, "get_all_subscriptions", return_value=[subscription]
        )

    @pytest.fixture(scope="class")
    def response(self, client: TestClient, mock_service: MagicMock) -> Response:
        return client.get("/subscriptions")

    def test_returns_correctly_formatted_json(
        self, response: Response, subscription: models.Subscription, out_data: dict
    ):
        assert response.json() == [out_data]

    def test_has_correct_statuscode(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_calls_service_with_correct_data(
        self, response: Response, mock_service: MagicMock
    ):
        mock_service.assert_called_once_with(ANY)


class TestGetAllSubscriptionsNoSubscriptions:
    @pytest.fixture(scope="class")
    def mock_service(self, class_mocker: MockerFixture) -> MagicMock:
        return class_mocker.patch.object(
            services, "get_all_subscriptions", return_value=[]
        )

    @pytest.fixture(scope="class")
    def response(self, client: TestClient, mock_service: MagicMock) -> Response:
        return client.get("/subscriptions")

    def test_returns_empty_when_no_subscriptions(self, response: Response):
        assert response.json() == []

    def test_is_code_200_ok_when_no_subscriptions(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_calls_service_with_session(
        self, response: Response, mock_service: MagicMock
    ):
        mock_service.assert_called_once_with(ANY)


class TestGetSubscriptionByUUID:
    @pytest.fixture(scope="class")
    def mock_service(
        self, class_mocker: MockerFixture, subscription: models.Subscription
    ) -> MagicMock:
        return class_mocker.patch.object(
            services, "get_subscription_by_uuid", return_value=subscription
        )

    @pytest.fixture(scope="class")
    def response(
        self, client: TestClient, subscription, mock_service: MagicMock
    ) -> Response:
        return client.get(f"/subscription/{subscription.subscription_uuid}")

    def test_returns_200_ok(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_json(
        self, response: Response, out_data: dict, subscription: models.Subscription
    ):
        assert response.json() == out_data

    def test_service_called_with_uuid_and_session(
        self,
        subscription: models.Subscription,
        mock_service: MagicMock,
        response: Response,
    ):
        mock_service.assert_called_once_with(ANY, subscription.subscription_uuid)


class TestGetSubscriptionByUUIDWhenDoesntExist:
    @pytest.fixture(scope="class")
    def mock_service(self, class_mocker: MockerFixture) -> MagicMock:
        return class_mocker.patch.object(
            services, "get_subscription_by_uuid", return_value=None
        )

    @pytest.fixture(scope="class")
    def response(self, client: TestClient, mock_service: MagicMock) -> Response:
        return client.get("/subscription/missing-uuid")

    def test_returns_404_not_found(self, response: Response):
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_correct_json(self, response: Response):
        assert response.json() == {"detail": "Subscription Not found"}

    def test_service_called_with_uuid(
        self, mock_service: MagicMock, response: Response
    ):
        mock_service.assert_called_once_with(ANY, "missing-uuid")


class TestDeleteSubscription:
    @pytest.fixture(scope="class")
    def mock_service(self, class_mocker: MockerFixture):
        return class_mocker.patch.object(
            services, "delete_subscription_by_uuid", return_value=None
        )

    @pytest.fixture(scope="class")
    def response(
        self,
        client: TestClient,
        mock_service: MagicMock,
        subscription: models.Subscription,
    ):
        return client.delete(f"/subscription/{subscription.subscription_uuid}")

    def test_returns_204_no_content(self, response: Response):
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_returns_empty_body(self, response: Response):
        assert response.text == ""

    def test_service_called_with_session(
        self,
        mock_service: MagicMock,
        response: Response,
        subscription: models.Subscription,
    ):
        mock_service.assert_called_once_with(ANY, subscription.subscription_uuid)


class TestDeleteMissingSubscription:
    @pytest.fixture(scope="class")
    def mock_service(self, class_mocker: MockerFixture) -> MagicMock:
        return class_mocker.patch.object(
            services, "delete_subscription_by_uuid", return_value=None
        )

    @pytest.fixture(scope="class")
    def response(
        self,
        subscription: models.Subscription,
        mock_service: MagicMock,
        client: TestClient,
    ) -> Response:
        return client.delete(f"/subscription/{subscription.subscription_uuid}")

    def test_returns_204_no_content(self, response: Response):
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_returns_no_body(self, response: Response):
        assert response.text == ""

    def test_service_called_with_session_and_uuid(
        self,
        response: Response,
        mock_service: MagicMock,
        subscription: models.Subscription,
    ):
        mock_service.assert_called_once_with(ANY, subscription.subscription_uuid)


class TestUpdateSubscription:
    @pytest.fixture(scope="class")
    def updated_data(self, out_data: dict) -> dict:
        return {**out_data, "email": "testperson2@test.com"}

    @pytest.fixture(scope="class")
    def updated_subscription(self, updated_data: dict) -> models.Subscription:
        return models.Subscription(
            **{
                **updated_data,
                "conditions": [
                    models.Condition(**condition)
                    for condition in updated_data["conditions"]
                ],
            }
        )

    @pytest.fixture(scope="class")
    def mock_service(
        self, class_mocker: MockerFixture, updated_subscription: models.Subscription
    ):
        return class_mocker.patch.object(
            services, "update_subscription_by_uuid", return_value=updated_subscription
        )

    @pytest.fixture(scope="class")
    def response(
        self, client: TestClient, updated_data: dict, mock_service: MagicMock
    ) -> Response:
        return client.put(
            f"/subscription/{updated_data['subscription_uuid']}",
            json={k: v for k, v in updated_data.items() if k != "subscription_uuid"},
        )

    def test_has_response_200_ok(self, response: Response):
        assert response.status_code == status.HTTP_200_OK

    def test_has_updated_data_in_body(self, response: Response, updated_data: dict):
        assert response.json() == updated_data

    @pytest.mark.usefixtures("response")
    def test_service_is_called_with_session_uuid_and_updated_data(
        self, mock_service: MagicMock, updated_data: dict
    ):
        mock_service.assert_called_once_with(
            ANY,
            updated_data["subscription_uuid"],
            schemas.SubscriptionUpdateInSchema.parse_obj(updated_data),
        )

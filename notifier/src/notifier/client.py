import email
import smtplib
from typing import Optional, Any

import attr
import httpx
from typing import Protocol


@attr.s(auto_attribs=True)
class Auth:
    api_key: str = attr.field(repr=False)


JsonResponseType = dict[str, Any] | list[dict[str, Any]]


class ApiClientInterface(Protocol):
    auth: Auth

    def get(self, endpoint: str, params: Optional[dict] = None) -> JsonResponseType:
        ...


class EmailClientInterface(Protocol):
    def send_email(self, to: str, subject: str, body: str) -> None:
        ...


@attr.s(auto_attribs=True)
class EmailClient:
    smtp: smtplib.SMTP
    sender: str = "noreply@weather-notifier.com"

    def send_email(self, to: str, subject: str, body: str) -> None:
        email_message = email.message.EmailMessage()
        email_message.set_content(body)
        email_message["From"] = self.sender
        email_message["To"] = to
        email_message["Subject"] = subject

        self.smtp.send_message(email_message)


@attr.s(auto_attribs=True)
class ApiClient:
    base_url: str
    auth: Auth = None

    def _client(self) -> httpx.Client:
        return httpx.Client(base_url=self.base_url)

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        params = {} if params is None else params
        with self._client() as c:
            r = c.get(endpoint, params=params)
        r.raise_for_status()
        return r.json()

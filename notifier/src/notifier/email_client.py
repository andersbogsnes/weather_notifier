import email
import smtplib
from typing import Protocol

import attr


class EmailClientInterface(Protocol):
    """
    An interface defining an EmailClient
    """

    def send_email(self, to: str, subject: str, body: str) -> None:
        """Should send an email to the 'to' subject"""
        ...


@attr.define()
class EmailClient:
    """
    Implementation of an email client

    Parameters
    ----------
    smtp_host:
        The full hostname of the SMTP server to use

    sender:
        The sender to attach to the email
    """

    smtp_host: str
    sender: str = "noreply@weather-notifier.com"

    @property
    def smtp(self) -> smtplib.SMTP:
        """Return an instance of the SMTP client"""
        return smtplib.SMTP(self.smtp_host)

    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Send an email message to the 'to' email

        Parameters
        ----------
        to: str
            The recipient email
        subject: str
            The subject line of the email
        body: str
            The contents of the email

        Returns
        -------
        None
        """
        email_message = email.message.EmailMessage()
        email_message.set_content(body)
        email_message["From"] = self.sender
        email_message["To"] = to
        email_message["Subject"] = subject

        self.smtp.send_message(email_message)

import os
from typing import cast

from sendgrid import SendGridAPIClient

from emailer.abstractions import IEmailer
from emailer.models.email import Email


class SendGrid(IEmailer):
    def __init__(self) -> None:
        """Create a new instance of the SendGrid wrapper.

        This will try to read the `SENDGRID_API_KEY` environment varaible
        """
        self.client = SendGridAPIClient(
            api_key=os.environ.get("SENDGRID_API_KEY")
        )

    def send(self, aEmail: Email) -> bool:
        """Send out the given email

        Arguments:
            aEmail {Email} -- The email to send

        Returns:
            bool -- True if successful
        """
        lResult = self.client.send(aEmail.to_sendgrid_email())

        return cast(int, lResult.status_code) == 200

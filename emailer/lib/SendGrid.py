import os
from typing import cast

from google.cloud import secretmanager
from sendgrid import SendGridAPIClient

from lib.abstractions import IEmailer
from lib.models.email import Email


class SendGrid(IEmailer):
    def __init__(self) -> None:
        """Create a new instance of the SendGrid wrapper.

        This will try to read the `SENDGRID_API_KEY` environment varaible
        """

        lSecretClient = secretmanager.SecretManagerServiceClient()
        lSecretName = lSecretClient.secret_version_path(
            project=os.environ.get("GCP_PROJECT"), secret="sendgrid-api-key", secret_version="latest"
        )
        lApiKey = lSecretClient.access_secret_version(lSecretName)

        self.client = SendGridAPIClient(api_key=lApiKey.payload.data.decode("UTF-8"))

    def send(self, aEmail: Email) -> bool:
        """Send out the given email

        Arguments:
            aEmail {Email} -- The email to send

        Returns:
            bool -- True if successful
        """
        lResult = self.client.send(aEmail.to_sendgrid_email())

        return cast(int, lResult.status_code) == 202

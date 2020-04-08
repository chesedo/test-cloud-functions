from unittest.mock import MagicMock, patch

from emailer.models.email import Email
from emailer.SendEmail import SendEmail


class TestSendEmail:
    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    def test_sending_fails(self, aEmailerMock: MagicMock, aLoggingMock: MagicMock):
        aEmailerMock.send.return_value = False

        SendEmail(aEmailerMock)

        aLoggingMock.info.assert_called_with("Failed to send email")

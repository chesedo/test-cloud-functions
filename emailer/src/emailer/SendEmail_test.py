from unittest.mock import MagicMock, patch

from emailer.models.email import Attachment, Email
from emailer.models.file_event import FileEvent
from emailer.SendEmail import SendEmail


class TestSendEmail:
    def setup_method(self) -> None:
        self.Email: FileEvent = {
            "name": "FileName.txt",
            "metageneration": "1",
            "contentType": "fake/text",
            "bucket": "stub",
            "metadata": {
                "from": "from@domain.com",
                "to": "john@doe.com",
                "subject": "Subject",
                "text": "Plain text",
                "html": "Rich text",
                "categories": "cat1",
            },
        }

    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    @patch("emailer.abstractions.IBucketReader")
    def test_file_was_not_created(
        self,
        aBucketReaderMock: MagicMock,
        aEmailerMock: MagicMock,
        aLoggingMock: MagicMock,
    ) -> None:
        self.Email["metageneration"] = "0"

        SendEmail(
            self.Email, aEmailerMock, aBucketReaderMock,
        )

        aLoggingMock.info.assert_called_with(
            "FileName.txt was not created. Will skip it."
        )
        aLoggingMock.info.called_times(1)

    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    @patch("emailer.abstractions.IBucketReader")
    def test_file_missing_email_metadata(
        self,
        aBucketReaderMock: MagicMock,
        aEmailerMock: MagicMock,
        aLoggingMock: MagicMock,
    ) -> None:
        del self.Email["metadata"]["to"]  # type: ignore

        SendEmail(
            self.Email, aEmailerMock, aBucketReaderMock,
        )

        aLoggingMock.info.assert_called_with(
            "FileName.txt does not contain the full email fields needed for"
            + " emailing. It will be skipped."
        )
        aLoggingMock.info.called_times(1)

    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    @patch("emailer.abstractions.IBucketReader")
    def test_failed_to_fetch_file(
        self,
        aBucketReaderMock: MagicMock,
        aEmailerMock: MagicMock,
        aLoggingMock: MagicMock,
    ) -> None:
        aBucketReaderMock.get_content.return_value = b""

        SendEmail(
            self.Email, aEmailerMock, aBucketReaderMock,
        )

        aBucketReaderMock.get_content.assert_called_with(
            "stub", "FileName.txt"
        )

        aLoggingMock.info.assert_called_with(
            "FileName.txt failed to download."
        )
        aLoggingMock.info.called_times(1)

    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    @patch("emailer.abstractions.IBucketReader")
    def test_sending_fails(
        self,
        aBucketReaderMock: MagicMock,
        aEmailerMock: MagicMock,
        aLoggingMock: MagicMock,
    ) -> None:
        aBucketReaderMock.get_content.return_value = b"Some text"
        aEmailerMock.send.return_value = False

        SendEmail(self.Email, aEmailerMock, aBucketReaderMock)

        aBucketReaderMock.get_content.assert_called_with(
            "stub", "FileName.txt"
        )
        aEmailerMock.send.assert_called_with(
            Email(
                subject="Subject",
                html="Rich text",
                plain_text="Plain text",
                to=["john@doe.com"],
                from_email="from@domain.com",
                categories=["cat1", "emailer", "0.1.0"],
                attachment=Attachment(
                    content=b"Some text",
                    mime_type="fake/text",
                    name="FileName.txt",
                ),
            )
        )

        aLoggingMock.info.assert_called_with("Failed to send email")

    @patch("emailer.SendEmail.logging")
    @patch("emailer.abstractions.IEmailer")
    @patch("emailer.abstractions.IBucketReader")
    def test_sending_succeeds(
        self,
        aBucketReaderMock: MagicMock,
        aEmailerMock: MagicMock,
        aLoggingMock: MagicMock,
    ) -> None:
        aBucketReaderMock.get_content.return_value = b"Some text"
        aEmailerMock.send.return_value = True

        SendEmail(self.Email, aEmailerMock, aBucketReaderMock)

        aBucketReaderMock.get_content.assert_called_with(
            "stub", "FileName.txt"
        )
        aEmailerMock.send.assert_called_with(
            Email(
                subject="Subject",
                html="Rich text",
                plain_text="Plain text",
                to=["john@doe.com"],
                from_email="from@domain.com",
                categories=["cat1", "emailer", "0.1.0"],
                attachment=Attachment(
                    content=b"Some text",
                    mime_type="fake/text",
                    name="FileName.txt",
                ),
            )
        )

        aLoggingMock.info.assert_called_with("Email send successfully")

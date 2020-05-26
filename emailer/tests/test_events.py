"""Test the file triggering events
"""

import os
from imaplib import IMAP4
from pathlib import Path

from google.cloud.storage.bucket import Bucket

from .utils import Random, get_subject, wait_for_email


class TestEvents:
    def setup_class(self) -> None:
        self.ExpectedSubject = Random.string(aMin=5, aMax=15)

    def test_upload(self, aImap: IMAP4, aBucket: Bucket) -> None:
        """Uploading a new file should cause an email to be send
        """

        lBlob = aBucket.blob("Pipeline/Report.pdf")

        lBlob.metadata = {
            "subject": self.ExpectedSubject,
            "to": os.environ.get("EMAIL_ADDRESS"),
            "text": "Plain text",
            "html": "Html text",
        }

        lBlob.upload_from_filename(Path(__file__).resolve().parent.joinpath("resources", "Report.pdf"))

        lRecent = wait_for_email(aImap)

        assert get_subject(aImap, lRecent) == self.ExpectedSubject

    def test_rename(self, aImap: IMAP4, aBucket: Bucket) -> None:
        """Renaming a file should cause an email to be send
        """

        lBlob = aBucket.blob("Pipeline/Report.pdf")
        aBucket.rename_blob(lBlob, "Pipeline/Report_Renamed.pdf")

        lRecent = wait_for_email(aImap)

        assert get_subject(aImap, lRecent) == self.ExpectedSubject

import os
from imaplib import IMAP4

from flask import Flask, request

from emailer import __version__
from main import emailer

from .utils import Random, get_subject, wait_for_email


def test_full(aApp: Flask, aImap: IMAP4) -> None:
    lSubjectExp = Random.string(aMin=5, aMax=15)

    with aApp.test_request_context(
        json={
            "bucket": "eta-testing-bucket",
            "contentType": "application/pdf",
            "crc32c": "n1FYKg==",
            "etag": "CLyS0+SX/OgCEAE=",
            "generation": "1587563736647996",
            "id": "eta-testing-bucket/Emails/Tshepong Operations Monthly "
            + "engineering review data_2020-04-21.pdf/1587563736647996",
            "kind": "storage#object",
            "md5Hash": "u4oiWrnpBp2edLgU6cJzVA==",
            "mediaLink": "https://www.googleapis.com/download/storage/v1/b/"
            + "eta-testing-bucket/o/Emails%2FTshepong%20Operations%20Monthly"
            + "%20engineering%20review%20data_2020-04-21.pdf?generation"
            + "=1587563736647996&alt=media",
            "metadata": {
                "to": os.environ.get("EMAIL_ADDRESS"),
                "text": "Plain text",
                "html": "Html text",
                "subject": lSubjectExp,
            },
            "metageneration": "1",
            "name": "Emails/Tshepong Operations Monthly engineering review "
            + "data_2020-04-21.pdf",
            "selfLink": "https://www.googleapis.com/storage/v1/b/eta-testing-"
            + "bucket/o/Emails%2FTshepong%20Operations%20Monthly%20engineering"
            + "%20review%20data_2020-04-21.pdf",
            "size": "436760",
            "storageClass": "REGIONAL",
            "timeCreated": "2020-04-22T13:55:36.647Z",
            "timeStorageClassUpdated": "2020-04-22T13:55:36.647Z",
            "updated": "2020-04-22T13:55:36.647Z",
        }
    ):
        emailer(request.get_json(), {})

        lRecent = wait_for_email(aImap)

        assert (
            get_subject(aImap, lRecent) == f"Subject: {lSubjectExp}".encode()
        )


def test_version() -> None:
    assert __version__ == "0.1.0"

import os
import random
import string
import time
from imaplib import IMAP4, IMAP4_SSL

import pytest
from flask import Flask, request

from emailer import __version__
from main import emailer


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def aApp():
    return Flask(__name__)


# Create a POP3 client
@pytest.fixture(scope="module")
def aImap():
    lImap = IMAP4_SSL(os.environ.get("EMAIL_SERVER"))
    lImap.login(
        os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_PASSWORD")
    )

    # Prepare inbox
    lImap.select("INBOX")
    clear_imap(lImap)

    # Capture current updates
    lImap.recent()

    yield lImap

    clear_imap(lImap)
    lImap.close()
    lImap.logout()


def clear_imap(aImap: IMAP4):
    """Clear the selected IMAP folder

    Arguments:
        aImap {IMAP4} -- IMAP with selected folder to clear
    """
    _, lMsgNums = aImap.search(None, "ALL")

    for lMsgNum in lMsgNums[0].split():
        aImap.store(lMsgNum, "+FLAGS", "\\Deleted")

    aImap.expunge()


def wait_for_email(aImap: IMAP4) -> str:
    """Wait for new email to arrive on IMAP connection

    Arguments:
        aImap {IMAP4} -- The IMAP connection to wait on

    Returns:
        str -- ID of the new email
    """
    __tracebackhide__ = True

    # Set 30 seconds timeout
    lEnd = time.time() + 30

    while time.time() < lEnd:
        lRecent = aImap.recent()[1][0]

        if lRecent is not None:
            return lRecent

    pytest.fail("Timed out waiting for email")
    return ""


def get_subject(aImap: IMAP4, aId: str) -> bytes:
    """Get the subject of a specific message id

    Arguments:
        aImap {IMAP4} -- The IMAP connection to use
        aId {str} -- Id of message whose subject will be fetched

    Returns:
        bytes -- The message's subject
    """
    __tracebackhide__ = True

    lType, lSubject = aImap.fetch(aId, "(body[header.fields (subject)])")
    assert lType == "OK"

    if isinstance(lSubject[0], tuple):
        return lSubject[0][1].strip()

    pytest.fail("Failed to get email subject")
    return b""


def test_full(aApp: Flask, aImap: IMAP4):
    lSubjectExp = "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(5, 15))
    )

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
        emailer(request.get_json(), {})  # type: ignore

        lRecent = wait_for_email(aImap)

        assert (
            get_subject(aImap, lRecent) == f"Subject: {lSubjectExp}".encode()
        )


def test_version() -> None:
    assert __version__ == "0.1.0"

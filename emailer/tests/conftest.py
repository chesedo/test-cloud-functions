"""Contains fixtures used by all IT
"""

import os
from imaplib import IMAP4, IMAP4_SSL
from typing import Iterator

import pytest
from flask import Flask
from google.cloud import storage
from google.cloud.storage.bucket import Bucket

from .utils import clear_bucket, clear_imap


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def aApp() -> Flask:
    return Flask(__name__)


# Create a POP3 client
@pytest.fixture(scope="module")
def aImap() -> Iterator[IMAP4]:
    lServer = os.environ.get("EMAIL_SERVER")
    lUsername = os.environ.get("EMAIL_USERNAME")
    lPassword = os.environ.get("EMAIL_PASSWORD")

    assert (
        lServer is not None
    ), "'EMAIL_SERVER' environment variable should be set for email test"
    assert (
        lUsername is not None
    ), "'EMAIL_USERNAME' environment variable should be set for email test"
    assert (
        lPassword is not None
    ), "'EMAIL_PASSWORD' environment variable should be set for email test"

    lImap = IMAP4_SSL(lServer)
    lImap.login(lUsername, lPassword)

    # Prepare inbox
    lImap.select("INBOX")
    clear_imap(lImap)

    # Capture current updates
    lImap.recent()

    yield lImap

    clear_imap(lImap)
    lImap.close()
    lImap.logout()


# Create a bucket to test against
@pytest.fixture(scope="module")
def aBucket() -> Iterator[Bucket]:
    lBucket = storage.Client().bucket("eta-testing-bucket")
    clear_bucket(lBucket)

    yield lBucket

    clear_bucket(lBucket)

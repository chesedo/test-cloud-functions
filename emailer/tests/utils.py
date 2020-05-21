import random
import string
import time
from imaplib import IMAP4
from typing import Optional

import pytest
from google.cloud.storage.bucket import Bucket


def clear_imap(aImap: IMAP4) -> None:
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
        lRecent: Optional[str] = aImap.recent()[1][0]

        if lRecent is not None:
            return lRecent

    pytest.fail("Timed out waiting for email")
    return ""


def get_subject(aImap: IMAP4, aId: str) -> str:
    """Get the subject of a specific message id

    Arguments:
        aImap {IMAP4} -- The IMAP connection to use
        aId {str} -- Id of message whose subject will be fetched

    Returns:
        str -- The message's subject
    """
    __tracebackhide__ = True

    lType, lSubject = aImap.fetch(aId, "(body[header.fields (subject)])")
    assert lType == "OK"

    if isinstance(lSubject[0], tuple):
        return lSubject[0][1].lstrip(b"Subject: ").rstrip().decode()

    pytest.fail("Failed to get email subject")
    return ""


def clear_bucket(aBucket: Bucket) -> None:
    """Clear the bucket from all testing files

    Arguments:
        aBucket {Bucket} -- The bucket to clear
    """
    for lBlob in aBucket.list_blobs(prefix="Pipeline/"):
        lBlob.delete()


class Random:
    @staticmethod
    def string(aMax: int, aMin: int = 0) -> str:
        """Generate a random string in a length range

        Arguments:
            aMax {int} -- Max length

        Keyword Arguments:
            aMin {int} -- Minimum length (default: {0})

        Returns:
            str -- The randomly created string
        """
        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(random.randint(aMin, aMax))
        )

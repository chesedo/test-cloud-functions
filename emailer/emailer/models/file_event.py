import logging
from typing import Any, Mapping, Optional

from mypy_extensions import TypedDict

"""Expected metadata for file to be emailed
"""
EmailMeta = TypedDict(
    "EmailMeta",
    {
        "from": str,
        "to": str,
        "subject": str,
        "text": str,
        "html": str,
        "categories": str,
    },
)

"""Expected dictionary for storage event
"""
FileEvent = TypedDict(
    "FileEvent",
    {
        "metageneration": str,
        "contentType": str,
        "name": str,
        "metadata": Optional[EmailMeta],
        "bucket": str,
    },
)


def IsEmailMeta(aMeta: Mapping[str, Any]) -> bool:
    """Verify if the metadata dictionary has the metadata to qualify as an email

    Arguments:
        aMeta {dict} -- The metadata dictionary

    Returns:
        bool -- True if the matadata has complete email information
    """
    lResult = True

    if "to" not in aMeta:
        logging.info("Missing 'to' field to be considered for emailing")
        lResult = False

    if "text" not in aMeta:
        logging.info("Missing 'text' field to be considered for emailing")
        lResult = False

    if "html" not in aMeta:
        logging.info("Missing 'html' field to be considered for emailing")
        lResult = False

    return lResult


def IsFileCreated(aFile: FileEvent) -> bool:
    """Check if the file event is for a file that was created

    Arguments:
        aFile {FileEvent} -- The file event

    Returns:
        bool -- True if the event is for a created file
    """
    return "metageneration" in aFile and aFile["metageneration"] == "1"

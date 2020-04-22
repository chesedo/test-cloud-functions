import logging
from typing import Any

from emailer.CloudStorage import CloudStorage
from emailer.models.file_event import FileEvent
from emailer.SendEmail import SendEmail
from emailer.SendGrid import SendGrid

# Cold run code
SendGridClient = SendGrid()
CloudStorageClient = CloudStorage()


def emailer(aData: FileEvent, aContext: Any) -> None:
    """HTTP end-point for send email from files uploaded to cloud storage

    Arguments:
        aData {FileEvent} -- The file event that triggered this function
        aContext {Context} -- The context
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"Processing {aData}")

    # SendEmail(aData, SendGridClient, CloudStorageClient)

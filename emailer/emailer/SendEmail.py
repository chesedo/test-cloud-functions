import logging
from typing import Optional

import emailer.models.file_event as fe
from emailer import __version__
from emailer.abstractions import IBucketReader, IEmailer
from emailer.models.email import Attachment, Email


def SendEmail(aEvent: fe.FileEvent, aEmailer: IEmailer, aBucketReader: IBucketReader) -> None:
    """Send an email using a specific emailer

    Arguments:
        aEvent {FileEvent} -- The event that triggered this function
        aEmailer {IEmailer} -- The emailer to use
        aBucketReader {IBucketReader} -- The bucket reader to use
    """
    # Run some prechecks on the event
    if not fe.IsFileCreated(aEvent):
        logging.info(f"{aEvent['name']} was not created. Will skip it.")
        return

    if "metadata" not in aEvent or aEvent["metadata"] is None:
        logging.info(f"{aEvent['name']} does not contain any metadata. It will be skipped.")
        return

    if not fe.IsEmailMeta(aEvent["metadata"]):
        logging.info(
            f"{aEvent['name']} does not contain the full email fields needed for emailing. It will be skipped."
        )
        return

    # Get file
    lAttachmentContent: Optional[bytes] = aBucketReader.get_content(aEvent["bucket"], aEvent["name"])

    if lAttachmentContent is None or len(lAttachmentContent) == 0:
        logging.info(f"{aEvent['name']} failed to download.")
        return

    # Build email
    lEmail: Email = Email.from_email_metadata(aEvent["metadata"])
    lEmail.attachment = Attachment(content=lAttachmentContent, mime_type=aEvent["contentType"], name=aEvent["name"],)

    # Add extra details for tracking
    lEmail.categories.append("emailer")
    lEmail.categories.append(__version__)

    # Finally, send the email
    if not aEmailer.send(lEmail):
        logging.info("Failed to send email")
        return

    logging.info("Email send successfully")

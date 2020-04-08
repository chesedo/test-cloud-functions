import logging

from emailer.abstractions import IEmailer
from emailer.models.email import Email


def SendEmail(aEmailer: IEmailer):
    """Sends an email using a specific emailer
    
    Arguments:
        aEmailer {IEmailer} -- The emailer to use
    """
    if not aEmailer.send(Email(subject="Test")):
        logging.info("Failed to send email")
        return

    logging.info("Email send successfully")

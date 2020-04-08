from dataclasses import dataclass


@dataclass
class Email:
    """Data structure that holds email details
    """

    """The email subject
    """
    subject: str

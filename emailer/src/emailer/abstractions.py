"""This file contains interface definitions
"""

import abc

from .models.email import Email


class IEmailer(abc.ABC):
    """Interface for anything that can send an email
    """

    @abc.abstractmethod
    def send(self, aEmail: Email) -> bool:
        """Sends out the given email
        
        Arguments:
            aEmail {Email} -- The email to send
        
        Returns:
            bool -- True if successful
        """
        pass

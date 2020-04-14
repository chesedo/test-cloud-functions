"""This file contains interface definitions
"""

import abc

from .models.email import Email


class IEmailer(abc.ABC):
    """Interface for anything that can send an email
    """

    @abc.abstractmethod
    def send(self, aEmail: Email) -> bool:
        """Send out the given email
        
        Arguments:
            aEmail {Email} -- The email to send
        
        Returns:
            bool -- True if successful
        """
        pass


class IBucketReader(abc.ABC):
    """Interface for reading a file's content from a bucket
    """

    @abc.abstractmethod
    def get_content(self, aBucket: str, aFile: str) -> bytes:
        """Get a file's content from a bucket
        
        Arguments:
            aBucket {str} -- Bucket to get the content from
            aFile {str} -- File's content to get
        
        Returns:
            bytes -- Content of file
        """
        pass

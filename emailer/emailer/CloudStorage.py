from typing import Optional, cast

from google.cloud import storage

from emailer.abstractions import IBucketReader


class CloudStorage(IBucketReader):
    def __init__(self) -> None:
        """Create a new instance of the Cloud Storage wrapper.
        """
        self.client = storage.Client()

    def get_content(self, aBucket: str, aFile: str) -> Optional[bytes]:
        """Get a file's content from a bucket

        Arguments:
            aBucket {str} -- Bucket to get the content from
            aFile {str} -- File's content to get

        Returns:
            bytes -- Content of file
        """
        return cast(
            bytes, self.client.bucket(aBucket).blob(aFile).download_as_string()
        )

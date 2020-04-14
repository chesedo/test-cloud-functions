from unittest.mock import MagicMock, patch

from emailer.models.file_event import IsEmailMeta, IsFileCreated


class TestIsEmailMeta:
    Meta = {"to": "to@domain.com", "text": "Plain text", "html": "Html value"}

    @patch("emailer.models.file_event.logging")
    def test_missing_to_field(self, aLoggingMock: MagicMock):
        """Test when the "to" field is missing in the metadata
        To fail check
        """

        lTmp = dict(self.Meta)
        del lTmp["to"]
        assert IsEmailMeta(lTmp) == False

        aLoggingMock.info.assert_called_with(
            "Missing 'to' field to be considered for emailing"
        )

    @patch("emailer.models.file_event.logging")
    def test_missing_text_field(self, aLoggingMock: MagicMock):
        """Test when the "text" field is missing in the metadata
        To fail check
        """

        lTmp = dict(self.Meta)
        del lTmp["text"]
        assert IsEmailMeta(lTmp) == False

        aLoggingMock.info.assert_called_with(
            "Missing 'text' field to be considered for emailing"
        )

    @patch("emailer.models.file_event.logging")
    def test_missing_html_field(self, aLoggingMock: MagicMock):
        """Test when the "html" field is missing in the metadata
        To fail check
        """

        lTmp = dict(self.Meta)
        del lTmp["html"]
        assert IsEmailMeta(lTmp) == False

        aLoggingMock.info.assert_called_with(
            "Missing 'html' field to be considered for emailing"
        )

    @patch("emailer.models.file_event.logging")
    def test_no_missing_fields(self, aLoggingMock: MagicMock):
        """Test when no fields are missing in the metadata
        To pass check
        """

        assert IsEmailMeta(self.Meta) == True

        aLoggingMock.info.called_times(0)


class TestIsFileCreated:
    def test_when_file_is_created(self):
        """Test when the event is for a created file
        """

        assert IsFileCreated({"metageneration": "1"}) == True

    def test_when_file_is_not_created(self):
        """Test when the event is not for a created file
        """

        assert IsFileCreated({"metageneration": "0"}) == False

    def test_when_type_is_wrong(self):
        """Test when the event has an unexpected type
        """

        assert IsFileCreated({"metageneration": False}) == False

    def test_when_key_is_missing(self):
        """Test when the event has the wrong keys
        """

        assert IsFileCreated({"otherKey": True}) == False

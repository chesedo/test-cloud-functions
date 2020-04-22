from __future__ import annotations

from base64 import b64encode
from dataclasses import dataclass, field
from typing import List, Optional

from sendgrid.helpers.mail import Attachment as SGAttachment
from sendgrid.helpers.mail import Category, Mail

from emailer.models.file_event import EmailMeta


@dataclass
class Attachment:
    """Structure to hold email attachment details

    Attribute:
        content {bytes} -- The content of the attachment
        mime_type {str} -- The mime of the content
        name {str} -- The name for this attachment
    """

    content: bytes
    mime_type: str
    name: str

    def to_sendgrid_attachment(self) -> SGAttachment:
        """Transform into a SendGrid attachment

        Returns:
            SGAttachment -- SendGrid attachment version of this attachment
        """
        return SGAttachment(
            file_content=b64encode(self.content).decode(),
            file_name=self.name,
            file_type=self.mime_type,
            disposition="attachment",
        )


@dataclass
class Email:
    """Data structure that holds email details

    Attributes:
        subject {str} -- The email subject
        html {str} -- The email in HTML format
        plain_text {str} -- The email in plain text
        to {List[str]} -- List of recipient that should receive the email
        from_email {str} -- The address of the sender
        categories {List[str]} -- List of categories for this email
        attachment {Optional[Attachment]} -- The file to attach to this email
            if one is needed
    """

    subject: str
    html: str
    plain_text: str
    to: List[str]
    from_email: str
    categories: List[str] = field(default_factory=list)
    attachment: Optional[Attachment] = None

    def to_sendgrid_email(self) -> Mail:
        """Transform into a SendGrid email

        Returns:
            Mail -- SendGrid version of this email
        """
        lMail: Mail = Mail(
            from_email=self.from_email,
            to_emails=self.to,
            subject=self.subject,
            html_content=self.html,
            plain_text_content=self.plain_text,
        )

        for c in self.categories:
            lMail.add_category(Category(c))

        if self.attachment:
            lMail.attachment = self.attachment.to_sendgrid_attachment()

        return lMail

    @classmethod
    def from_email_metadata(cls, aMeta: EmailMeta) -> Email:
        """Build an email from email metadata

        Arguments:
            aMeta {EmailMeta} - The metadata to build the email from

        Returns:
            Email -- The email that was build
        """

        lCategories = []

        if "categories" in aMeta:
            lCategories = aMeta["categories"].split(";")

        return Email(
            subject=aMeta.get("subject", "MTB report"),
            to=aMeta["to"].split(";"),
            from_email=aMeta.get("from", "no-reply@mtbpower.com"),
            html=aMeta["html"],
            plain_text=aMeta["text"],
            categories=lCategories,
        )

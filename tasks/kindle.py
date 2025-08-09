from loguru import logger
import os
import smtplib
import ssl
import sys

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pathlib import Path
from util.task import SimpleTask, TaskType

GMAIL_PORT = 465
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
CURRENT_PLATFORM_SEPARATOR = "\\" if sys.platform == "win32" else "/"


class Kindle(SimpleTask):
    def __init__(
        self,
        task_type: TaskType,
        name: str,
        payload: dict = {},
    ):
        super(SimpleTask, self).__init__()
        self.task_type = task_type
        self.name = name
        self.payload = payload

    async def exec(self):
        recipient = self.payload.get("recipient", "")
        subject = self.payload.get("subject", "")
        body = self.payload.get("body", "")
        attachment_list: list[Path] = self.payload.get("att_list", [])
        if not len(recipient):
            raise Exception("No recipients added")

        try:
            assert GMAIL_USERNAME is not None
            assert GMAIL_PASSWORD is not None

            message = MIMEMultipart()
            message["From"] = GMAIL_USERNAME
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            if len(attachment_list):
                for attachment in attachment_list:
                    if os.path.isdir(attachment):
                        raise Exception("Directories not allowed")
                    filename = attachment.name
                    logger.debug(filename)
                    with open(attachment, "rb") as attfile:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attfile.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition", f"attachment; filename= {filename}"
                        )
                        message.attach(part)
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                "smtp.gmail.com", GMAIL_PORT, context=context
            ) as server:
                server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
                server.sendmail(GMAIL_USERNAME, recipient, text)
        except AssertionError as ase:
            logger.exception(f"Failed assertion: {str(ase)}")
        except Exception as exc:
            logger.exception(f"Email send failed: {str(exc)}")
        return None

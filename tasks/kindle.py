import logging
import os
import smtplib
import ssl
import sys

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from util.task import Task, TaskType

GMAIL_PORT = 465
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
CURRENT_PLATFORM_SEPARATOR = "\\" if sys.platform == "win32" else "/"


class SendFeedToKindle(Task):
    def __init__(
        self,
        task_type: TaskType,
        name: str,
        payload: dict = {},
    ):
        super(Task, self).__init__(task_type, name)
        self.payload = payload

    async def exec(self):
        recipient = self.payload.get("recipient", "")
        subject = self.payload.get("subject", "")
        body = self.payload.get("body", "")
        att_list = self.payload.get("att_list", [])
        if not len(recipient):
            raise Exception("No recipients added")

        try:
            message = MIMEMultipart()
            message["From"] = GMAIL_USERNAME
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            attachment_list = att_list
            if len(attachment_list):
                for attachment in attachment_list:
                    if os.path.isdir(attachment):
                        raise Exception("Directories not allowed")
                    filename = attachment.split(CURRENT_PLATFORM_SEPARATOR)[-1]
                    print(filename)
                    with open(attachment, "rb") as attfile:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attfile.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                        )
                        message.attach(part)
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                "smtp.gmail.com", GMAIL_PORT, context=context
                    ) as server:
                server.login(
                    GMAIL_USERNAME, GMAIL_PASSWORD
                    )
                server.sendmail(GMAIL_USERNAME, recipient, text)
        except Exception as exc:
            print("Count not send email, reason:")
            logging.exception(exc)
        return None

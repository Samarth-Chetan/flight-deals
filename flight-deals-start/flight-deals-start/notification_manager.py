from pyexpat.errors import messages
from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.smtp_address = os.environ["SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        self.connection = smtplib.SMTP(os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"])
        self._account_sid = os.environ["TWILIO_SID"]
        self._auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(self._account_sid, self._auth_token)

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_ = f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body = message_body,
            to = f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}',
            content_sid = os.environ["TWILIO_CONTENT_SID"]
        )
        print(message.sid)

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
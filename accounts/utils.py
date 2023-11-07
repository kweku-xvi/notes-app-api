import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_AUTH_KEY'))

def send_password_reset_email(link, email, username):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "8467Q64S1TM50KHMCRWVDZFDJ5XA",
            "data": {
            "username": username,
            "email_verication_link": link,
            },
        }
    )
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv("EMAIL")
test_email = os.getenv("TEST_EMAIL")
password = os.getenv("SMTP_PASS")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = (int)(os.getenv("SMTP_PORT"))

def send_test_email():
    msg = EmailMessage()
    body = "Hi there, this is a test message."
    msg['Subject'] = f'The contents of test-message.txt'
    msg['From'] = email
    msg['To'] = test_email

    with open("templates/signature.html", "r") as f:
        signature_html = f.read()

        msg.add_alternative(f"""
        <html>
        <body>
            <p>{body}</p>
            <br>
            {signature_html}
        </body>
        </html>
        """, subtype="html")

    try:
        # For TLS (most common, port 587)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls() 
        server.login(email, password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit() 
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

def send_email(subject, recipients, body, event):
    msg = EmailMessage()
    msg_head = f"This email is regarding: {event["eventName"]} on {event["eventDate"]}"
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email
    msg['Bcc'] = ", ".join(recipients)

    with open("templates/signature.html", "r") as f:
        signature_html = f.read()
        msg.add_alternative(f"""
        <html>
        <body>
            <p><b>{msg_head}</b></p>
            {body}
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

def send_cancel_email(recipients, event):
    msg = EmailMessage()
    msg_head = f"This email is regarding: {event["eventName"]} on {event["eventDate"]}"
    msg['Subject'] = "An Event you RSVP'd for was Canceled"
    msg['From'] = email
    msg['To'] = email
    msg['Bcc'] = ", ".join(recipients)

    with open("templates/signature.html", "r") as f:
        signature_html = f.read()
        msg.add_alternative(f"""
        <html>
        <body>
            <p><b>{msg_head}</b></p>
            <p>This is an automated email to inform you that an event you RSVP'd to was canceled. </p>
            <p>For any other questions, you can reach out to the event coordinator</p>
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


def send_account_delete_email(recipient):
    msg = EmailMessage()
    msg_head = f"This email is regarding your Event Tracker Account"
    msg['Subject'] = "Your Account has Been Deleted"
    msg['From'] = email
    msg['To'] = email
    msg['Bcc'] = recipient

    with open("templates/signature.html", "r") as f:
        signature_html = f.read()
        msg.add_alternative(f"""
        <html>
        <body>
            <p><b>{msg_head}</b></p>
            <p>This is an automated email to inform you that your account has been sucessfully deleted.</p>
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


def send_welcome_email(recipient):
    msg = EmailMessage()
    msg_head = f"This email is regarding your Event Tracker Account"
    msg['Subject'] = "Welcome to Event Tracker!"
    msg['From'] = email
    msg['To'] = email
    msg['Bcc'] = recipient

    with open("templates/signature.html", "r") as f:
        signature_html = f.read()
        msg.add_alternative(f"""
        <html>
        <body>
            <p><b>{msg_head}</b></p>
            <p><b>Welcome to Event Tracker!</b><br><br>The easy to use platform for your event tracking needs</p>
            <ul>
                <li>Create, update, and track events</li>
                <li>Collect RSVP's</li>
                <li>Easily contact attendees</li>
            </ul>
            <p>If you notice any problems, please feel free to submit an issue on the github repository below!</p>
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
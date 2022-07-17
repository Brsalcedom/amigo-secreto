#!/usr/bin/python3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from termcolor import colored, cprint
import smtplib, ssl, textwrap, config

def sendmail(sender_name, sender_email, recipient_name, recipient_email):

    msg = MIMEMultipart()       
    html_message = textwrap.dedent("""\
    <html>
        <body>
            <p>
                Hola {},<br>
                {}<br>
                Tu amigo secreto es: <strong>{}</strong>
            </p>
        </body>
    </html>
    """).format(sender_name, config.EMAIL_BODY, recipient_name)

    msg['From']= config.EMAIL_SENDER
    msg['To']= sender_email
    msg['Subject']= config.SUBJECT
    msg.attach(MIMEText(html_message, "html"))
    text = msg.as_string()
    SSLcontext = ssl.create_default_context()
    try:
        with smtplib.SMTP(config.EMAIL_SERVER, config.EMAIL_PORT) as server:
            server.starttls(context=SSLcontext)
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.sendmail(config.EMAIL_SENDER, sender_email, text)
            cprint("\n[*] Email enviado a {}".format(sender_email), "yellow")
    except exception as e:
        cprint("\n[!] Error: {}".format(e), "red")
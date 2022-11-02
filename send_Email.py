#import os
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


def sendmail(emailSender, passwordsender, emailReciever, subject, body, server, files=None, port=465):
    try:
        em = MIMEMultipart()
        em['From'] = emailSender
        em['To'] = emailReciever
        em['Subject'] = subject
        em.attach(MIMEText(body))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                    #basenavn tager filnavn af sti
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            em.attach(part)
    except Exception as e:
        return [False, f'could not create email message, {e}']
    try:
        # send email secure
        smtp = smtplib.SMTP(server, port)
        smtp.login(emailSender, passwordsender)
        smtp.sendmail(emailSender, emailReciever, em.as_string())
        smtp.close()
        return [True, f'email succesfully send']
    except Exception as e:
        return [False, f'could not send emailmessage, {e}']

#2 faktor slåes fra
#aktivere allow other apps.
#Username and Password not accepted

#https://stackoverflow.com/questions/3362600/how-to-send-email-attachments

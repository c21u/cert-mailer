import sendgrid
import os
import urllib.request as urllib
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def send(config, body, img, row):

    content = Content("text/html", body)

    attachment = Attachment()
    attachment.content = img
    attachment.type = "image/jpeg"
    attachment.filename = "qrcode.jpg"
    attachment.disposition = "inline"
    attachment.content_id = "qrcode"

    mail = Mail(Email(config.from_email), config.cert_email_subject, Email(row['email']), content)
    mail.add_attachment(attachment)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as err:
        print(err.read())
        exit()

    print(response.status_code)
    print(response.body)
    print(response.headers)
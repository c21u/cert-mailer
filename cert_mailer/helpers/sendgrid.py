import sendgrid
import os
import urllib.request as urllib
from sendgrid.helpers.mail import Content, Attachment, Mail, Email


class Mailer:
    def __init__(self):
        key = os.environ.get('SENDGRID_API_KEY')
        self.sg = sendgrid.SendGridAPIClient(apikey=key)

    def send(self, config, subject, body, img, row):

        content = Content("text/html", body)

        attachment = Attachment()
        attachment.content = img
        attachment.type = "image/jpeg"
        attachment.filename = "qrcode.jpg"
        attachment.disposition = "inline"
        attachment.content_id = "qrcode"

        fromaddr = Email(config.from_email)
        toaddr = Email(row['email'])

        mail = Mail(fromaddr, subject, toaddr, content)
        mail.add_attachment(attachment)
        try:
            response = self.sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as err:
            print(err.read())
            exit()

        print(response.status_code)
        print(response.body)
        print(response.headers)

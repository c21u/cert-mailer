import mandrill
import os


class Mailer:
    def __init__(self):
        key = os.environ.get('MANDRILL_API_KEY')
        self.mandrill_client = mandrill.Mandrill(key)

    def send(self, config, subject, body, img, row):
        message = {
            'from_email': config.from_email,
            'subject': subject,
            'html': body,
            'auto_text': True,
            'images': [
                {
                    'type': 'image/jpeg',
                    'name': 'qrcode',
                    'content': img
                }
            ],
            'to': [{'email': row['email']}]
        }
        result = self.mandrill_client.messages.send(message=message,
                                                    asynchronous=False)
        return result

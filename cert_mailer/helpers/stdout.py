class Mailer:
    def send(self, config, subject, body, img, row):
        message = {
            'from_email': config.from_email,
            'subject': subject,
            'html': body,
            'to': [{'email': row['email']}]
        }
        print(message)
        return

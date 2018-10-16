#!/usr/bin/env python

import base64
import csv
import qrcode
import sendgrid
import io
import os
from sendgrid.helpers.mail import *
import urllib.request as urllib

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

from_email = Email("noreply@blockcerts.gatech.edu")

subject = "Blockchain Credentials from C21U"

with open('distributionlist.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        introUrl = "https://wallet.blockcerts.org/#/introduce-recipient/https:%2F%2Fissuer.blockcerts.gatech.edu%2F{}".format(row['nonce'])

        imgFile = io.BytesIO()
        qrcode.make(introUrl).get_image().save(imgFile, 'JPEG')

        attachment = Attachment()
        attachment.content = base64.b64encode(imgFile.getvalue()).decode()
        attachment.type = "image/jpeg"
        attachment.filename = "qrcode.jpg"
        attachment.disposition = "inline"
        attachment.content_id = "qrcode"

        body = """<p>During Thursday’s Vice Provost Leadership meeting, Rich Demillo mentioned that C21U has been working on the idea of issuing blockchain-based academic credentials. As described in the CNE report, these are “new decentralized transcripts based on blockchain technology that allows students to combine evidence of learning and achievements into credentials that are relevant to potential employers.”</p>
        <br>
        <p>Specifically, we’ve been experimenting with Blockcerts. Blockcerts is an open standard for creating, issuing, viewing, and verifying blockchain-based credentials.</p>
        <br>
        <p>In order to give everyone a sense of how Blockcerts works, C21U would like to issue you a Blockcerts credential. Before we can do that, you must add us as an issuer in your Blockcerts wallet.</p>
        <br>
        <p><b>Step 1: Install the app</b></p>
        <p>Install the “Blockcerts Wallet” app on your phone (available on the iOS or Android app stores).</p>
        <br>
        <p><b>Step 2: Add issuer</b></p>
        <p>There are two ways to add us as an issuer:</p>
        <ul>
            <li>If you’re reading this email on your mobile device, <a clicktracking=off href="{}">Click this link to add C21U as an issuer</a>.</li>
            <li>If you’re reading this email on your desktop, scan the QR code below using your mobile device.</li>
        </ul>

        <img src="cid:qrcode" alt="Scannable barcode for use with mobile devices"> 

        <p>Please note: it’s important to complete these steps in this order. After you have added us as an issuer, you will be notified within 4-5 days when your credential is ready. If you have any issue or questions, please email Matt Lisle at <a href="mailto:matt@c21u.gatech.edu">matt@c21u.gatech.edu</a>.</p>""".format(introUrl)

        content = Content("text/html", body)

        mail = Mail(from_email, subject, Email(row['email']), content)
        mail.add_attachment(attachment)
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as err:
            print(err.read())
            exit()

        print(response.status_code)
        print(response.body)
        print(response.headers)

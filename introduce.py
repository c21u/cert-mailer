#!/usr/bin/env python

import base64
import configargparse
import csv
import qrcode
import io
import os
import urllib.request as urllib
from importlib import import_module
from string import Template


def send_email(config, row):
    intro_url = urllib.quote(config.introduction_url, safe=':')
    row['introduction_url'] = (
        "https://wallet.blockcerts.org/#/introduce-recipient/{}/{}"
        .format(intro_url, row['nonce']))

    imgFile = io.BytesIO()
    qrcode.make(row['introduction_url']).get_image().save(imgFile,
                                                          'JPEG')
    img = base64.b64encode(imgFile.getvalue()).decode()

    row['qrcode'] = ('<img src="cid:qrcode" alt="Scannable barcode '
                     'for use with mobile devices">')

    body = Template(config.introduction_email_body).safe_substitute(row)

    mailer = import_module('helpers.{}'.format(config.mailer)).Mailer()
    mailer.send(config, config.introduction_email_subject, body, img, row)


def send_emails(config):
    with open(config.distribution_list) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            send_email(config, row)


def get_config():
    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, 'conf.ini')
    p = configargparse.getArgumentParser(
            default_config_files=[config_file_path])

    p.add('-c', '--my-config', required=False, is_config_file=True,
          help='config file path')

    p.add_argument('--from_email', required=True, type=str,
                   help='from email address')
    p.add_argument('--distribution_list', required=True, type=str,
                   help='csv file with emails and substitutions')
    p.add_argument('--introduction_url', required=True, type=str,
                   help='url for introducing the wallet to the issuer')
    p.add_argument('--introduction_email_subject', required=True, type=str,
                   help='subject of the email')
    p.add_argument('--introduction_email_body', required=True, type=str,
                   help='body of the email')
    p.add_argument('--mailer', required=True, type=str,
                   help='the mail api to use')

    args, _ = p.parse_known_args()

    return args


def main():
    conf = get_config()
    send_emails(conf)
    print('Sent!')


if __name__ == "__main__":
    main()

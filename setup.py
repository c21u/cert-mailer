import os

from setuptools import setup, find_packages

from cert_mailer import __version__

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-mailer',
    version=__version__,
    description='mails blockchain certificates and introductions',
    author='D. Stuart Freeman',
    tests_require=['tox'],
    url='https://github.com/stuartf/cert-mailer',
    license='MIT',
    author_email='stuart.freeman@c21u.gatech.edu',
    long_description=long_description,
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'introduce = cert_mailer.introduce:main',
            'sendcert = cert_mailer.sendcert:main'
        ]}
)

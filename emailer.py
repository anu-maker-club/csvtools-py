#!/usr/bin/python

__author__ = 'jay'

import argparse
import sys
import reader
from subprocess import call


def main():
    p = argparse.ArgumentParser(description='Receives a file containing email addresses and sends messages to them')
    p.add_argument('-i', '--input', metavar='input', type=str, help='The file containing all the information')
    p.add_argument('-s', '--subject', metavar='subject', type=str, help='The subject line for the email')

    args = p.parse_args()
    filename = args.input
    subject_line = args.subject
    # Saves the message into a single string
    std_input = ''
    for line in sys.stdin:
        std_input += line

    emails = []
    if reader.file_exists(filename):
        readings = reader.open_csv_file(filename)

        for row in readings:
            emails.append(generate_email_data(row, std_input, subject_line))

        for email in emails:
            print("email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message'))
            # call(["email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message')])
    else:
        raise IOError('Please point to an existing file')


def generate_email_data(row, message, subject):
    """
    Creates all the data we need to send an email. Specific values can be inserted with tags. eg to insert the
    persons name use {name} in the plaintext email to insert the name, use {email} to insert their email address etc.
    :param row: A dict containing information about the user we are sending the email to.
    :param message: String representing the message to be sent by email.
    :param subject: String representing the subject line for the email.
    :return: Dict containing all information needed to send an email.
    """
    if 'name' not in row or row.get('name') == '':  # User has not inserted their name into database yet use uid again
        message = message.format(uid=row.get('uid'), code=row.get('code'), name=row.get('uid'))
        subject = subject.format(uid=row.get('uid'), code=row.get('code'), name=row.get('uid'))
    else:
        message = message.format(uid=row.get('uid'), code=row.get('code'), name=row.get('name'))
        subject = subject.format(uid=row.get('uid'), code=row.get('code'), name=row.get('name'))

    return {'message': message, 'email': row.get('email'), 'subject': subject}


if __name__ == '__main__':
    main()

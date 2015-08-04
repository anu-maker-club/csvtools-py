#!/usr/bin/python

__author__ = 'jay'

import os.path
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
    if file_exists(filename):
        readings = reader.open_csv_file(filename)

        for row in readings:
            emails.append(generate_email_data(row, std_input, subject_line))

        for email in emails:
            print("email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message'))
            # call(["email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message')])
    else:
        raise IOError('Please point to an existing file')


def generate_email_data(row, message, subject):
    if 'name' not in row or row.get('name') == '':  # User has not inserted their name into database yet use uid again
        message = message.format(uid=row.get('uid'), code=row.get('code'), name=row.get('uid'))
        subject = subject.format(uid=row.get('uid'), code=row.get('code'), name=row.get('uid'))
    else:
        message = message.format(uid=row.get('uid'), code=row.get('code'), name=row.get('name'))
        subject = subject.format(uid=row.get('uid'), code=row.get('code'), name=row.get('name'))

    return {'message': message, 'email': row.get('email'), 'subject': subject}


def file_exists(filename):
    if os.path.isfile(filename):
        return True
    return False


if __name__ == '__main__':
    main()

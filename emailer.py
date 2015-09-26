#!/usr/bin/python

__author__ = 'jay'

import argparse
import sys
import reader
from subprocess import call
import smtplib


def main():
    p = argparse.ArgumentParser(description='Receives a file containing email addresses and sends messages to them')
    p.add_argument('-i', '--input', metavar='input', type=str, help='The file containing all user information')
    p.add_argument('-m', '--message', metavar='msg', dest='msg', type=str, help='The file containing the email message')
    p.add_argument('-s', '--subject', metavar='subject', type=str, help='The subject line for the email')

    args = p.parse_args()
    #filename = args.input
    subject_line = args.subject
    # Saves the message into a single string
    #print("Please enter the message:")
    #std_input = ''
    #for line in sys.stdin:
    #    std_input += line

    if args.msg:
        msg_file = args.msg
    else:
        msg_file = "message"

    if args.input:
        filename = args.input
    else:
        filename = "datafile"

    with open(msg_file) as mf:
        msg = mf.read()

    emails = []
    if reader.file_exists(filename):
        readings = reader.open_csv_file(filename)

        for row in readings:
            print(row)
            emails.append(generate_email_data(row, msg, subject_line))

        # test case
        #emails.append({'email': "u5490127@anu.edu.au", 'message': "test message", 'subject': "Test Subtitle"})

        print("Emails generated:")

        count = 0
        for email in emails:
            # print("email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message'))
            # call(["email", "-s", email.get('subject'), email.get('email'), "<<<", email.get('message')])
            print("#", count, "    ", "Email: ", email.get('email'), "Title: ", email.get('subject'))
            print("Message:")
            print(email.get('message'))
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
        message = message.format(uid=row.get('uid'), id=row.get('id'), name=row.get('uid'))
        subject = subject.format(uid=row.get('uid'), id=row.get('id'), name=row.get('uid'))
    else:
        message = message.format(uid=row.get('uid'), id=row.get('id'), name=row.get('name'))
        subject = subject.format(uid=row.get('uid'), id=row.get('id'), name=row.get('name'))

    return {'message': message, 'email': row.get('email'), 'subject': subject}

def send_email():
    pass

if __name__ == '__main__':
    main()

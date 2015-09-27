#!/usr/bin/python

__author__ = 'jay'

import argparse
import sys
import reader
from subprocess import call
import smtplib
import datetime
import os.path

smtp_server = 'smtp.gmail.com'
smtp_port = 587


def main():
    p = argparse.ArgumentParser(description='Receives a file containing email addresses and sends messages to them')
    p.add_argument('-d', '--datafile', metavar='datafile', type=str, help='The file containing all user information')
    p.add_argument('-m', '--message', metavar='msg', dest='msg', type=str, help='The file containing the email message')
    p.add_argument('-s', '--subject', metavar='subject', type=str, help='The subject line for the email')
    p.add_argument('-l', '--login', metavar='login', dest='smtp_login', type=str, help='Login email address')
    p.add_argument('-p', '--pass', metavar='password', dest='smtp_pass', type=str, help='The password for login')
    p.add_argument('--mode', metavar='mode', dest='mode', type=str, help='Operation mode, options: show, send, default: show')
    p.add_argument('--log', metavar='log', dest='log', type=str, help='Log file name')

    args = p.parse_args()
    subject_line = args.subject

    if args.mode:
        mode = args.mode
    else:
        mode = 'show'

    if args.msg:
        msg_file = args.msg
    else:
        msg_file = "message"

    if args.datafile:
        filename = args.datafile
    else:
        filename = "datafile"
    if mode == 'send':
        if not args.smtp_login:
            print("Missing info: ", "Please provide login")
            return
        smtp_login = args.smtp_login

        if not args.smtp_pass:
            print("Missing info: ", "Please provide password")
            return
        smtp_pass = args.smtp_pass

    if args.log:
        logfile = args.log
    else:
        logfile = "emailerlog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(msg_file) as mf:
        msg = mf.read()

    emails = []
    if reader.file_exists(filename):
        readings = reader.open_csv_file(filename, ['name', 'email'])
        if readings == None:
            print("Error encountered during reading of csv data file")
            return

        for row in readings:
            email_data = generate_email_data(row, msg, subject_line)
            if email_data == None:
                print("Erorr encountered while generating emails")
                return
            emails.append(email_data)

        if mode == 'show':
            count = 0
            for email in emails:
                print("#", count, "    ", "Email: ", email.get('email'))
                print("Title: ", email.get('subject'))
                print("Message:")
                print(email.get('message'))
                count += 1
                input("Press enter to continue...")
            print("")
            print("End of all emails")
        elif mode == 'send':
            # setup logging
            interrupted_sends = []  # operate like a stack in below code
            confirmed_sends = []
            if os.path.isfile(logfile):
                logfh = open(logfile, 'r')
                logstr = logfh.read()
                logentries = logstr.split('\n')
                for entry in logentries:    # go through to find entries that indicate interrupted sending
                    fields = entry.replace(' ', '').split(',')   # format : line, start/end
                    if fields == ['']:
                        continue
                    if fields[1] == 'start':
                        interrupted_sends.append(int(fields[0]))
                    else:
                        if interrupted_sends[len(interrupted_sends)-1] == int(fields[0]):
                            interrupted_sends.remove(int(fields[0]))
                            confirmed_sends.append(int(fields[0]))
                logfh.close()
                logfh = open(logfile, 'a')
            else:
                logfh = open(logfile, 'w')

            # setup mailing client
            print("Logging in")
            mail_client = setup_mailer(smtp_login, smtp_pass)

            if not mail_client:
                print('Error encoutnered during emailer setup')
                return

            count = 0
            for email in emails:
                if count in confirmed_sends:
                    continue
                print(">Sending out email : ", count)
                logfh.write(str(count) + ',' + "start" + "\n")
                send_email(mail_client, smtp_login, email)
                logfh.write(str(count) + ',' + "end" + "\n")
                print("<Email sent")
                count += 1
            logfh.close()
            print("")
            print("All emails sent")
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

    if 'email' not in row or row.get('email') == '':
        print("Missing email")
        print("Row : ", row)
        return None

    if 'name' not in row or row.get('name') == '':  # User has not inserted their name into database yet use uid again
        message = message.format(uid=row.get('uid'), id=row.get('id'), name=row.get('uid'))
        subject = subject.format(uid=row.get('uid'), id=row.get('id'), name=row.get('uid'))
    else:
        message = message.format(uid=row.get('uid'), id=row.get('id'), name=row.get('name'))
        subject = subject.format(uid=row.get('uid'), id=row.get('id'), name=row.get('name'))

    return {'message': message, 'email': row.get('email'), 'subject': subject}


def setup_mailer(smtp_login, smtp_pass):
    global smtp_server
    global smtp_port
    #print(smtp_server, smtp_login, smtp_pass)
    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.ehlo()

    try:
        smtp_client.starttls()
    except smtplib.SMTPHeloError:
        print("SMTP starttls failed, error : ", "SMTPHeloError")
        print("Detail : ", "The server didn't reply properly to the HELO greeting")
        return None
    except smtplib.SMTPException:
        print("SMTP starttls failed, error : ", "SMTPException")
        print("Detail : ", "The server does not support the STARTTLS extension")
        return None
    except RuntimeError:
        print("SMTP starttls failed, error : ", "SMTPException")
        print("Detail : ", "SSL/TLS support is not available to your Python interpreter")
        return None

    smtp_client.ehlo()

    try:
        smtp_client.login(smtp_login, smtp_pass)
    except smtplib.SMTPHeloError:
        print("SMTP login failed, error : ", "SMTPHeloError")
        print("Detail : ", "The server didn't reply properly to the HELO greeting")
        return None
    except smtplib.SMTPAuthenticationError:
        print("SMTP login failed, error : ", "SMTPAuthenticationError")
        print("Detail : ", "The server didn't accept the username/password combination")
        return None
    except smtplib.SMTPException:
        print("SMTP login failed, error : ", "SMTPException")
        print("Detail : ", "No suitable authentication method was found")
        return None

    return smtp_client


def send_email(smtp_client, smtp_login, email):
    header = 'To: ' + email.get('email') + '\n' + 'From: ' + smtp_login + '\n' + 'Subject:' + email.get('subject') + '\n'
    try:
        smtp_client.sendmail(smtp_login, email.get('email'), header + email.get('message'))
    except smtplib.SMTPRecipientsRefused:
        print("SMTP send failed, error : ", "SMTPRecipientRefused")
        print("Detailed : ", "All recipients were refused, no one got the email")


if __name__ == '__main__':
    main()

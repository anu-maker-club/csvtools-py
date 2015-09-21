#!/usr/bin/python

__author__ = 'jay'

import argparse
import reader
import sys
import re


def main():
    p = argparse.ArgumentParser(description="Inserts information into CSV files, will overwrite information!")
    p.add_argument('-n', '--name', metavar='name', default='', type=str, help='The name to insert.')
    p.add_argument('-e', '--email', metavar='email', default='', type=str, help='The email address to insert.')
    p.add_argument('-u', '--user', metavar='user', default='', type=str, help='Add user mode[update, add].')
    p.add_argument('-i', '--input', metavar='input', help='The csv file')
    p.add_argument('-c', '--id', metavar='id', default='', type=str, help='id uniquely identifies user, '
                                                                              'use when inserting or updating '
                                                                              'new information.')

    args = p.parse_args()

    if args.user == 'update':
        mode = False
        if args.id == '':
            print('You must specify a id when updating.')
            sys.exit(2)
        else:
            id = args.id
    elif args.user == 'add':
        mode = True
        if args.name == '' and args.email == '':
            print('At least 1 of name or email must be specified when creating a new member.')
            sys.exit(2)
    elif not (args.user == 'add' or args.user == 'update'):
        print('You must specify a single mode with -u [update, add].')
        sys.exit(2)
    else:
        print('You must specify a single mode with -u [update, add].')
        sys.exit(2)

    if (args.input == '') or not reader.file_exists(args.input):
        print('File does not exist.')
        sys.exit(2)
    else:
        filename = args.input

    if args.name != '':
        name = args.name
    else:
        name = ''
    if args.email != '':
        email = args.email
    else:
        email = ''

    details = reader.open_csv_file(filename)

    if mode:
        details = add_user(name, email, details)
    else:
        details = update_user(name, email, id, details)

    reader.write_csv_file(details, filename)

    sys.exit(0)


def add_user(name, email, details):
    id = reader.generate_unique_id(details)
    new_user = {}

    if name != '':
        new_user['name'] = name
    else:
        new_user['name'] = ''

    if email != '':
        new_user['email'] = email
    else:
        new_user['email'] = ''

    if re.match("^u[\d][\d][\d][\d][\d][\d][\d]@", email):
        new_user['uid'] = email.split('@')[0]

    new_user['id'] = id

    details.append(new_user)
    return details


def update_user(name, email, id, details):
    for line in details:
        if id == line.get('id'):
            if email != '':
                line['email'] = email
            if name != '':
                line['name'] = name
            if line.get('uid') == '' and re.match('^u[\d][\d][\d][\d][\d][\d][\d]@', email):
                line['uid'] = email.split('@')[0]
    return details


if __name__ == '__main__':
    main()

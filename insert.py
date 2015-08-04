#!/usr/bin/python

__author__ = 'jay'

import argparse
import reader


def main():
    p = argparse.ArgumentParser(description="Inserts information into CSV files, will overwrite information!")
    p.add_argument('-n', '--name', metavar='name', default='', type=str, help='The name to insert.')
    p.add_argument('-e', '--email', metavar='email', default='', type=str, help='The email address to insert.')
    p.add_argument('-u', '--user', metavar='user', type=str, default='', help='Add user mode.')
    p.add_argument('-i', '--input', metavar='input', help='The csv file')
    p.add_argument('-c', '--code', metavar='code', type=str, help='Code uniquely identifies user, use when inserting'
                                                                  ' or updating new information.')

    args = p.parse_args()

    if args.code == '':
        raise IOError("You must specify a code to update details")
    else:
        code = args.code

    if args.user == 'update':
        mode = False
    elif args.user == 'add':
        mode = True
    elif not (args.user == 'add' or args.user == 'update'):
        raise IOError('Please specify a mode')
    else:
        raise IOError('Only specify add or update mode.')

    if (args.input == '') or not reader.file_exists(args.input):
        raise IOError('Please point to a csv file')
    else:
        filename = args.input

    if args.name != '':
        name = args.name
    else:
        name = None
    if args.email != '':
        email = args.email
    else:
        email = None

    print(name)
    print(email)
    details = reader.open_csv_file(filename)

    if mode:
        details = add_user(name, email, details)
    else:
        details = update_user(name, email, code, details)

    reader.write_csv_file(details, filename)


def add_user(name, email, details):
    code = reader.generate_unique_code(details)
    new_user = {}
    if name != None:
        new_user['name'] = name
    else:
        new_user['name'] = None
    if email != None:
        new_user['email'] = email
    else:
        new_user['email'] = None
    new_user['code'] = code
    new_user['uid'] = None

    details.append(new_user)
    return details


def update_user(name, email, code, details):
    for line in details:
        if code == line.get('code'):
            if email != None:
                line['email'] = email
            if name != None:
                line['name'] = name
    return details


if __name__ == '__main__':
    main()

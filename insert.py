#!/usr/bin/python

__author__ = 'jay'

import argparse
import reader


def main():
    p = argparse.ArgumentParser(description="Inserts information into CSV files, will overwrite information!")
    p.add_argument('-n', '--name', metavar='name', default='', type=str, help='The name to insert.')
    p.add_argument('-e', '--email', metavar='email', default='', type=str, help='The email address to insert.')
    p.add_argument('-d', '--details', metavar='details', type=bool, default=False, help='Update details mode.')
    p.add_argument('-u', '--user', metavar='user', type=bool, default=False, help='Add user mode.')
    p.add_argument('-i', '--input', metavar='input', help='The csv file')
    p.add_argument('-c', '--code', metavar='code', type=str, help='Code uniquely identifies user, use when inserting'
                                                                  ' or updating new information.')

    args = p.parse_args()

    if not (args.add and args.update):
        raise IOError("Only specify one mode")
    elif args.add and args.update:
        raise IOError("Only specify whether insert mode or add mode.")
    elif args.user:
        mode = True
    elif args.details:
        if args.code == '':
            raise IOError("You must specify a code to update details")
        mode = False
    else:
        raise IOError("Only specify add or update mode.")

    if (args.input == '') or not reader.file_exists(args.input):
        raise IOError("Please point to a csv file")
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

    if mode == True:
        add_user(name, email, details)
    else:
        update_user(name, email, details)


def add_user(name, email, details):
    if name != '':
        add_name(name, details)
    elif email != '':
        add_email(email, details)
    create_unique_code(details)


def update_user(name, email, details):
    if name != '':
        update_name(name, details)
    elif email != '':
        update_email(email, details)


def add_name(name, details):
    pass
    # TODO: Insert someones name


def add_email(email, details):
    pass
    # TODO: Insert someones email


def update_name(name, details):
    pass
    # TODO: Insert someones name


def update_email(email, details):
    pass
    # TODO: Insert someones email     


def create_unique_code(details):
    pass
    # TODO: Create a unique ID


if __name__ == '__main__':
    main()

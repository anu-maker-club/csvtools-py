#!/usr/bin/python

__author__ = 'jay'

import argparse
import csv
import os.path

def main():
    p = argparse.ArgumentParser(description="Inserts information into CSV files, will overwrite information!")
    p.add_argument('-n', '--name', metavar='name', default='', type=str, help='The name to insert.')
    p.add_argument('-e', '--email', metavar='email', default='', type=str, help='The email address to insert.')
    p.add_argument('-a', '--add', metavar='add', type=bool, default=False, help='Add user mode.')
    p.add_argument('-u', '--update', metavar='update', type=bool, default=False, help='Update mode.')
    p.add_argument('-i', '--input', metavar='input', help='The csv file')

    args = p.parse_args()

    if args.add and args.update:
        raise IOError("Only specify whether insert mode or add mode.")
    elif args.add:
        mode = True
    elif args.update:
        mode = False
    else:
        raise IOError("Only specify add or update mode.")

    if (args.input == '') or not os.path.exists(args.input):
        raise IOError("Please point to a csv file")
    else:
        filename = args.input

    if args.name != '':
        name = args.name
    if args.email != '':
        email = args.email


if __name__ == '__main__':
    main()
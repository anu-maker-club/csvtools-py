#!/usr/bin/python

__author__ = 'jay'

import csv
import argparse
import os.path
import random
import string


def main():
    p = argparse.ArgumentParser(description='Takes in a csv file of UID\'s and generates '
                                            'corresponding emails and a random string representing '
                                            'their ID within the organisation, if a csv file that '
                                            'has all that information already exists then this '
                                            'program will ignore those and only append new information')
    p.add_argument('-i', '--input', metavar='input', type=str, help='The file containing all the information')
    p.add_argument('-o', '--output', metavar='output', default='out.csv', help='The output files name, defaults to'
                                                                               '\'out.csv\'')
    args = p.parse_args()
    filename = args.input
    output = args.output
    if file_exists(filename):
        student_details = open_csv_file(filename)
        student_details = add_email(student_details)
        student_details = add_code(student_details)
        student_details = set_name(student_details)
        write_csv_file(student_details, output)
    else:
        raise IOError("please point to a csv file containing uid's on newlines")


def file_exists(filename):
    if os.path.isfile(filename):
        return True
    return False


def set_name(details):
    for entry in details:
        if 'name' not in entry or entry.get('name') == '':
            entry['name'] = ''
    return details


def add_code(details):
    for entry in details:
        if 'code' not in entry or entry.get('code') == '':  # If they have a code already skip them
            entry['code'] = generate_unique_code(details)
    return details


def generate_unique_code(details):
    code = code_generator()  # Go through the entries to verify the code is
    for entry in details:  # truly unique, we cant trust the randomness.
        if 'code' in entry:  # If code exists.
            while code == entry.get('code'):  # Check if it is the same.
                code = code_generator()
    return code


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_email(details):
    for entry in details:
        if 'email' not in entry or entry.get('email') == '':
            entry['email'] = generate_email_from_uid(entry.get('uid'))
    return details


def generate_email_from_uid(uid):
    return uid + '@anu.edu.au'


def open_csv_file(filename):
    """
    opens and reads in a csv file

    :type filename: string name of the file
    :returns: list of dictionaries with headers as keys to the dict
    """
    readings = []
    with open(filename, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            readings.append(row)
    return readings


def write_csv_file(content, output_name):
    with open(output_name, 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=['code', 'email', 'name', 'uid'])
        writer.writeheader()
        for row in content:
            writer.writerow(row)


if __name__ == "__main__":
    main()

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
        student_details = add_id(student_details)
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


def add_id(details):
    for entry in details:
        if 'id' not in entry or entry.get('id') == '':  # If they have a id already skip them
            entry['id'] = generate_unique_id(details)
    return details


def generate_unique_id(details):
    id = id_generator()  # Go through the entries to verify the id is
    for entry in details:  # truly unique, we cant trust the randomness.
        if 'id' in entry:  # If id exists.
            while id == entry.get('id'):  # Check if it is the same.
                id = id_generator()
    return id


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_email(details):
    for entry in details:
        if 'email' not in entry or entry.get('email') == '':
            if 'uid' in entry and entry.get('uid') != '':
                entry['email'] = generate_email_from_uid(entry.get('uid'))
            else:
                print("Missing email address")
                return None
    return details


def generate_email_from_uid(uid):
    return uid + '@anu.edu.au'


def open_csv_file(filename, enforced_fields):
    """
    opens and reads in a csv file

    :type filename: string name of the file
    :returns: list of dictionaries with headers as keys to the dict
    """
    readings = []
    line = 1
    fields = []
    with open(filename, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if line == 1:   # gather available fields from header
                for field in row:
                    fields.append(''.join(filter(lambda x: x not in '"\'', field.strip())))
                for enforced_field in enforced_fields:
                    if enforced_field not in fields:
                        print("datafile missing required fields")
                        print("field missing :", enforced_field)
                        return None
                line += 1
                continue
            dict_row = {}
            for i in range(len(fields)):
                row_str = ''.join(filter(lambda x: x not in '"\'', row[i].strip()))
                if fields[i] == 'name':
                    row_str = row_str.title()
                    if '/' in row_str:
                        row_str2 = ""
                        for c in row_str:
                            if c == '/':
                                break
                            row_str2 += c
                        row_str = row_str2.strip()
                dict_row.update({fields[i]: row_str})
            readings.append(dict_row)
    return readings


def write_csv_file(content, output_name):
    with open(output_name, 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=['id', 'email', 'name', 'uid'])
        writer.writeheader()
        for row in content:
            writer.writerow(row)


if __name__ == "__main__":
    main()

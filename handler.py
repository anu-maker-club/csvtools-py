#!/usr/bin/python

# Author : Darren (ANUMC_InfoSec)
# Credit : Jay (ANUMC_InfoSec), original author of reader.py and insert.py
#          The two scripts are used as basis to handler.py

# This script aims to be assistance based, rather than fully automated

import csv
import argparse
import os.path
import random
import string
import re

def main():

    file_opened = False
    current_file_name = ""

    config_header = []
    regex_obj_arr = []
    config_settings = {}
    data_rows = []

    # main terminal based interface
    while True:
        input_buffer = input("> ")
        words = input_buffer.split()

        if len(words) == 0:
            continue

        if words[0] == "?":
            print("quit")
            print("open")
            print("add")
            print("show")
            print("find")
            print("modify")
            print("verify")
            continue

        if words[0] == "quit":
            input_buffer = input("Quit? Y/n ")
            if input_buffer == "n":
                continue
            else:
                return

        if words[0] == "open":
            config_header = []
            regex_obj_arr = []
            config_settings = {}
            data_rows = []
            if len(words) == 1:
                print("open : too few arguments")
                continue
            if len(words) > 2:
                print("open : too many arguments")
                continue
            if words[1] == "?":
                print("[FILE]")
                continue
            if not check_file_exist(words[1]):
                print("open : file does not exist")
                continue
            result = open_csv_file(words[1])
            if result == None:
                continue
            config_header = result[0]
            regex_obj_arr = result[1]
            config_settings = result[2]
            data_rows = result[3]

            #default of "open"
            file_opened = True
            current_file_name = words[1]
            print("open : file opened successfully")
            continue

        if words[0] == "add":
            if not file_opened:
                print("add : no file opened yet")
                continue
            if len(words) < 2:
                print("add : too few arguments")
                continue
            if words[1] == "?":
                print("entry")
                print("field")
                continue
            if words[1] == "entry":
                interface_add_entry(config_header, regex_obj_arr, config_settings)
                if entry_result == None:
                    print("add : entry not added")
                else:
                    data_rows.append(entry_result)
                # default of "entry"
                continue
            # csv option is not used at the moment
            if words[1] == "csv":
                if len(words) < 3:
                    print("add : too few arguments")
                    continue
                if not check_file_exist(words[2]):
                    print("add : file does not exist")
                # default of "csv"
                continue
            if words[1] == "field":
                if len(words) > 2:
                    print("add : too many arguments")
                    continue
                interface_add_field(config_header, regex_obj_arr, config_settings, data_rows)
                continue
            # default of "add"
            print("add : command not recognised")
            continue

        if words[0] == "show":
            if not file_opened:
                print("show : no file opened yet")
                continue
            if len(words) == 1:
                print("show : too few arguments")
                continue
            if words[1] == "all":
                for i in range(len(data_rows)):
                    print("Entry : " + str(i))
                    show_data_row(data_rows[i])
                continue
            if words[1] == "entry":
                if len(words) < 3:
                    print("show : too few arguments")
                if len(words) > 3:
                    print("show : too many arguments")
                try:
                    entry_id = int(words[2])
                except ValueError:
                    print("show : entry id is not an integer")
                    continue
                if entry_id >= len(data_rows):
                    print("show : entry id exceeds maximum")
                    continue
                print("Entry : " + str(entry_id))
                show_data_row(data_rows[entry_id])
                continue

            # default of "show"
            print("show : command not recognised")
            continue

        if words[0] == "find":
            if not file_opened:
                print("show : no file opened yet")
                continue
            if len(words) <= 2:
                print("find : too few arguments")
                continue
            if (len(words) - 1) % 2 == 1:
                print("find : field name, pattern not in pairs")
                continue
            user_regex_obj_dict = {}
            for i in range(1, len(words), 2):
                if words[i] not in config_header:
                    print("find : match target not in header")
                    continue
                user_regex_obj_dict.update({words[i]: re.compile(re.sub(r"^\*", ".*", words[i+1]))})
            for i in range(len(data_rows)):
                row = data_rows[i]
                for usr_key in user_regex_obj_dict.keys():
                    if user_regex_obj_dict.get(usr_key).fullmatch(row.get(usr_key)):
                        print("Entry : " + str(i))
                        show_data_row(row)
            continue

            #default of "find"
            print("find : command not recognised")
            continue

        if words[0] == "modify":
            if not file_opened:
                print("modify : no file opened yet")
                continue
            if len(words) <= 2:
                print("modify : too few arguments")
                continue
            if words[1] == "entry":
                if len(words) < 3:
                    print("modify : too few arguments")
                    continue
                try:
                    entry_id = int(words[2])
                except ValueError:
                    print("modifiy : entry id is not an integer")
                    continue
                if entry_id >= len(data_rows):
                    print("modify : entry id exceeds maximum")
                    continue
                interface_modify_entry(config_header, regex_obj_arr, config_settings, data_rows[entry_id])
                continue

            # default of "modify"
            print("modify : command not recognised")
            continue

        if words[0] == "verify":
            if not file_opened:
                print("show : no file opened yet")
                continue

            # default of "verify"
            print("verify : command not recognised")
            continue

        if words[0] == "save":
            if len(words) < 2:
                print("save : too few arguments")
                continue
            if len(words) > 3:
                print("save : too many arguments")
            if words[1] == "add_config":
                if len(words) == 2:     # use current file name
                    file_name = current_file_name
                else:
                    file_name = words[2]
                if check_file_exist(file_name):
                    user_input = input("save : file already exists, do you want to replace? y/N")
            if words[1] == "no_config":
                if len(words) == 2:     # use current file name
                    file_name = current_file_name
                else:
                    file_name = words[2]
                if check_file_exist(file_name):
                    user_input = input("save : file already exists, do you want to replace? y/N")
            continue

        print("command not recognised")

def interface_add_entry(config_header, regex_obj_arr, config_settings, data_rows):
    for i in range(len(config_header)):
        empty_count = 0
        input_ok = False
        row_dict = {}
        while not input_ok:
            user_input = input(config_header[i] + " : ")
            # check if user wants to cancel
            if user_input == "":
                if empty_count == 1:
                    return False
                print("Entering empty input again will cancel adding")
                empty_count += 1
                continue
            else:
                empty_count = 0
            # check format
            if regex_obj_arr[i].fullmatch(user_input) == None:
                user_input = input("Format check failed, do you want to re-enter? Y/n")
                if (user_input == "n"):
                    input_ok = True
                else:
                    continue
            row_dict.update({config_header[i]: user_input})
    data_rows.append(row_dict)
    return True

def interface_modify_entry(config_header, regex_obj_arr, config_settings, entry):
    for i in range(len(config_header)):
        empty_count = 0
        input_ok = False
        while not input_ok:
            print("Old " + config_header[i] + " : " + entry.get(config_header[i]))
            user_input = input("Please enter new " + config_header[i] + " : ")
            if user_input == "":
                input_ok = True
                continue
            # check format
            if regex_obj_arr[i].fullmatch(user_input) == None:
                user_input = input("Format check failed, do you want to re-enter? Y/n ")
                if (user_input == "n"):
                    input_ok = True
                else:
                    continue
            entry.update({config_header[i]: user_input})
            input_ok = True
    return True

def interface_add_field(config_header, regex_obj_arr, config_settings, data_rows):
    input_ok = False
    empty_count = 0
    while not input_ok:
        user_input = input("field name : ")
        # check if user wants to cancel
        if user_input == "":
            if empty_count == 1:
                return False
            print("Entering empty input again will cancel adding")
            empty_count += 1
            continue
        else:
            empty_count = 0
        # store the name
        if user_input in config_header:
            print("Field already present")
            continue
        field_name = user_input
        user_input = input("regex format : ")
        # check if user wants to cancel
        if user_input == "":
            if empty_count == 1:
                return False
            print("Entering empty input again will cancel adding")
            empty_count += 1
            continue
        else:
            empty_count = 0
        regex_format = user_input
        user_input = input("default value : ")
        # check if user wants to cancel
        if user_input == "":
            if empty_count == 1:
                return False
            print("Entering empty input again will cancel adding")
            empty_count += 1
            continue
        else:
            empty_count = 0
        default_value = user_input
        for row in data_rows:
            row.update({field_name: default_value})
        # store the new field
        config_header.append(field_name)
        regex_obj_arr.append(re.compile(re.sub(r"^\*", ".*", regex_format)))
        input_ok = True
    return True

def interface_modify_field(config_header, regex_obj_arr, config_settings, data_rows):
    for i in range(len(config_header)):
        empty_count = 0
        input_ok = False
        old_field_name = ""
        new_field_name = ""
        while not input_ok:
            old_field_name = config_header[i]
            print("Old field name is : " + config_header[i])
            user_input = input("Please enter new field name : ")
            if user_input == "":
                input_ok = True
                continue
            new_field_name = user_input
            config_header[i] = new_field_name
            # update data row dictionaries
            for row in data_rows:
                row[new_field_name] = row.pop(old_field_name)
            input_ok = True

    return True

def show_data_row(row):
    for key in sorted(row.keys()):
        print("    " + key + " : " + row.get(key))

    return True
def check_file_exist(filename):
    if os.path.isfile(filename):
        return True
    return False

def parse_config_header(row):
    if row[0] != "config_header":
        print("parse_config_header : row is not a config_header");
        return None
    config_header = row[1:]
    return config_header

def parse_config_regex(row):
    if row[0] != "config_regex":
        print("parse_config_regex : row is not config_regex")
        return None
    config_regex = row[1:]
    regex_obj_arr = []
    for i in range(len(config_regex)):
        regex_obj_arr.append(re.compile(re.sub(r"^\*", ".*", str(config_regex[i]))))
    return regex_obj_arr

def parse_config_settings(row):
    if row[0] != "config_settings":
        print("parse_config_settings : row is not config_settings");
        return None
    config_settings = row[1:]
    if len(config_settings) == 1:
        return None
    if len(config_settings) % 2 == 1:   # the setting should be in pairs
        print("parse_config_settings : settings are invalid(not in pairs)");
        return None
    settings_dict = {}
    for i in range(0, len(config_settings), 2):   # pair them up
        settings_dict.update({config_settings[i]: config_settings[i+1]})
    return settings_dict

def parse_entry_row(header, row):   # excess fields are ignored completely
    row_dict = {}
    for i in range(len(header)):
        if i < len(row):
            # adjustment to lower/upper case
            if header[i].lower() == 'name':     # if this field of row is the name
                field_str = row[i].title()
            else:
                field_str = row[i]
            row_dict.update({header[i]: field_str})
        else:
            row_dict.update({header[i]: "N/A"})
    return row_dict

def open_csv_file(filename):
    line = 1;

    config_header = None
    regex_obj_arr = None
    config_settings = None

    data_rows = []

    with open(filename, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for raw_row in reader:
            row = []
            for field in raw_row:
                # remove double and single quotes
                row.append(''.join(filter(lambda x: x not in '"\'', field.strip())))
            if len(row) == 0:   # empty row
                continue
            if row[0] == "config_header":
                config_header = parse_config_header(row)
                if regex_obj_arr != None:
                    if len(config_header) != len(regex_obj_arr):
                        print("open : length of config_header is not consistent with config_regex")
            elif row[0] == "config_regex":
                regex_obj_arr = parse_config_regex(row)
                if config_header != None:
                    if len(regex_obj_arr) != len(config_header):
                        print("open : length of config_regex is not consistent with config_regex")
            elif row[0] == "config_settings":
                config_settings = parse_config_settings(row)
            else:   # processing data rows, all three configs must be present
                if (config_header == None):
                    print("open_csv_file : missing config_header")
                    return None
                if (regex_obj_arr == None):
                    print("open_csv_file : missing config_regex")
                    return None
                if (config_settings == None):
                    print("open_csv_file : missing config_settings")
                    return None
                row_dict = parse_entry_row(config_header, row)
                data_rows.append(row_dict)

    return (config_header, regex_obj_arr, config_settings, data_rows)


if __name__ == "__main__":
    main()

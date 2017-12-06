#!/usr/bin/python3

"""
This script anonymize student submissions, it requires tab-separated file with
student IDs and names. It looks up in a specific directory and renames the
file containing the name, replacing it with the student's ID.

After grading, you can invert and rename back from ID to name.

It also support multiple tests, if you specify so, it prepends the test ID
before the file name.
"""


import os
import argparse
from unidecode import unidecode


def run(database, file_list, invert):

    # regular: name to number
    # inverted: number to name
    conversion = {}
    print(database)
    for line in open(database).readlines():
        data = line.strip().split('\t')

        # indexes name or number depending on inversion or not
        key_index, value_index = (0, 1)
        if invert:
            key_index, value_index = 1, 0

        # creates dict as name to number
        if isinstance(data[key_index], int):
            conversion[data[value_index]] = data[key_index]
        else:
            conversion[data[key_index]] = data[value_index]

    # now, do the conversion
    for key, value in conversion.items():
        found = False
        for f in file_list:
            # uses unidecode to strip accents and ç
            if unidecode(key.lower()) in f.lower():
                # found, convert
                old_name, extension = os.path.splitext(f)

                # sets the new name (preserves extension)
                new_name = value + extension

                # sets the new path (same dir as old_name)
                new_path = os.path.join(os.path.dirname(old_name), new_name)
                os.rename(f, new_path)
                # print('%s -> %s' % (f, new_path))
                found = True
                break
        if not found:
            print('Warning! Key %s not found in files!' % key)


def run_multiple_tests(database, file_list, invert):
    # regular: name to number
    # inverted: number to name
    conversion = {}
    print(database)
    exam_types = {}
    for line in open(database).readlines():

        print(line)

        # ignores comments
        if line[0] == '#':
            continue

        data = line.strip().split('\t')

        # indexes name or number depending on inversion or not
        key_index, value_index = (1, 2)
        if invert:
            key_index, value_index = 2, 1

        # creates dict as name to number
        # also fills the exam type
        if isinstance(data[key_index], int):
            conversion[data[value_index]] = data[key_index]
            exam_types[data[value_index]] = data[0]
        else:
            conversion[data[key_index]] = data[value_index]
            exam_types[data[key_index]] = data[0]

    print(
        "Found %d names in database" %
        (len(conversion))
    )

    print(
        "File list has %d files" %
        (len(file_list))
    )

    # now, do the conversion
    for key, value in conversion.items():
        found = False
        for f in file_list:
            # uses unidecode to strip accents and ç
            if unidecode(key.lower()) in unidecode(f.lower()):
                # found, convert
                old_name, extension = os.path.splitext(f)

                # sets the new name (preserves extension)
                new_name = '%s_%s%s' % (exam_types[key], value, extension)

                # sets the new path (same dir as old_name)
                new_path = os.path.join(os.path.dirname(old_name), new_name)
                os.rename(f, new_path)
                # print('%s -> %s' % (f, new_path))
                found = True
                break
        if not found:
            print('Warning! Key %s not found in files!' % key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Anonymizer. Transforms file names.')

    parser.add_argument(
        'database', type=str,
        help='File with name-to-number correspondence'
    )

    parser.add_argument(
        'input', nargs='+',
        help='File(s) to be analyzed',
    )

    parser.add_argument(
        '-i', '--invert', action='store_true',
        help='Invert operation (if file is number-to-name, the program converts name-to-number)'
    )

    parser.add_argument(
        '-m', '--multiple', action='store_true',
        help='Are there multiple types of tests? (they are indicated in the first file column)',
    )

    args = parser.parse_args()
    if args.multiple:
        run_multiple_tests(args.database, args.input, args.invert)

    else:
        run(args.database, args.input, args.invert)

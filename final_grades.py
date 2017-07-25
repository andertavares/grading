"""
Makes a summary, showing a list of students and their grades
"""

import argparse


def analyse(file_list):
    for f in file_list:
        for line in open(f).readlines():
            if 'Total' in line:
                # print(f, line)
                grade = float(line.split(' ')[1])
                print("%.2f %s" % (grade, f))
                break

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Final programming grades')

    parser.add_argument(
        'input', nargs='+',
        help='File(s) to be analyzed',
    )

    args = vars(parser.parse_args())

    analyse(args['input'])
    #print('Done')

import re
import argparse


def analyse(file_list, scale=0):
    for file_name in file_list:
        final_grade = 0
        max_grade = 0
        new_lines = []

        f = open(file_name)
        for line in f.readlines():
            match = re.search('(\d+\.*\d*) de (\d+\.*\d*)', line)

            if match:
                # attained grade is in group 1
                final_grade += float(match.group(1))

                # max grade is in group 2
                max_grade += float(match.group(2))

            # replaces the line with 'Total' with 'Total' + the grades
            if 'Total:' in line:
                line = 'Total: %.2f de %.2f ' % (final_grade, max_grade)

                if scale > 0:
                    line += '(%.2f de %.2f)' % \
                            (round(final_grade*scale, 2), round(max_grade*scale, 2))

                line += '\n'
            # will write a file with new total
            new_lines.append(line)
        f.close()

        # now, write updated file
        f = open(file_name, 'w')
        f.writelines(new_lines)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Sum grades, show and adjust the file')

    parser.add_argument(
        'input', nargs='+',
        help='File(s) to be analyzed',
    )

    parser.add_argument(
        '-s', '--scale', type=float, default=0,
        help='Scaling factor for the grades'
    )

    args = parser.parse_args()

    analyse(args.input, args.scale)
    #print('Done')

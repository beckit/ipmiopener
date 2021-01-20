#!/usr/bin/env python3

"""
Access ipmi with broken firmware that returns a bogus .jnlp file
Specifically the BMC firmware on the Tyan S5512 Motherboard,
tested with firmware version R3.15

Original Version 2021/01/20

Note:  If you're having troubles downloading the .jnlp file,
       try the seamonkey browser
"""
import argparse
import re
import subprocess


def get_args():
    """
    Get arguments, return a parser object
    """
    parser = argparse.ArgumentParser(description="Fix a .jnlp to run with javaws")

    parser.add_argument("filename", nargs='?', type=str,
                        default="jviewer.jnlp",
                        help="The .jnlp file to fix")
    parser.add_argument("--editonly", "--eo", action='store_true',
                        help="dont run javaws, just edit the .jnlp")
    parser.add_argument("--javaws", type=str, default="javaws",
                        help="where is the javaws binary? Path is default.")
    return parser.parse_args()


def main():
    """
    This opens a .jnlp, fixes it up, writes it, and runs
    javaws with the fixed .jnlp
    """
    args = get_args()

    with open(args.filename, 'r') as file_handle:
        file_data = file_handle.readlines()

    new_data = ''
    for line in file_data:
        result = re.search('<argument>(.+)<argument>(.+)</argument>', line)
        if result:
            # if true, this is the line that needs fixing
            new_data += '        <argument>%s</argument>\n' % result.group(1)
            new_data += '        <argument>%s</argument>\n' % result.group(2)
        else:
            # otherwise, discard the line with </argument> on its own
            if line != '</argument>\n':
                # and simply add the regular lines in the file:
                new_data += line

    try:
        # overwrite the bad .jnlp:
        with open(args.filename, 'w') as file_handle:
            file_handle.write(new_data)
            print("Saved new version: %s" % args.filename)
    except Exception as exception:
        raise exception

    if not args.editonly:
        # run javaws with the .jnlp:
        runtime = subprocess.Popen(args='%s %s' % (args.javaws, args.filename),
                                   shell=True)
        runtime.communicate()


if __name__ == "__main__":
    main()

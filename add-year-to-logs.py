import argparse
import datetime
import fileinput
import glob
import os
import re
import sys
import subprocess

def get_files():
    results = []
    path = '../logs/**/sos_commands/logs/*'
    for file in glob.glob(path):
        results.append(file)
    return results

def convert_date(old_date):
    return datetime.datetime.strptime(old_date, "%b %d %H:%M:%S %Y").strftime('%Y-%m-%dT%H:%M:%SZ')

def add_year_to_log(filename, year):
    with fileinput.FileInput(filename, inplace = True) as f:
        pattern = "^(?P<time>\D{3} \d{2} \d{2}:\d{2}:\d{2}) (?P<log>.*)"
        for line in f:
            result = re.search(pattern, line)
            if result:
                if "Logs begin" in line:
                    continue
                else:
                    time = result.group(1)
                    log = result.group(2)
                    print(line.replace(line, convert_date(time + " " + year) + " " + log), end ='\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="Year to add to log files", required = True)
    args = parser.parse_args()

    files = get_files()
 
    for f in files:
        add_year_to_log(f, args.year)

if __name__ == '__main__':
    main()

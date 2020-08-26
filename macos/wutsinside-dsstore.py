#!/usr/bin/env python3

# What is inside .DS_Store?
# Found a .DS_Store in one of the servers from $work, but not a Mac user... so what's
# inside that file anyway?

import argparse
import sys

from ds_store import DSStore

parser = argparse.ArgumentParser(description='See inside a .DS_Store file')
parser.add_argument('--file', help='File absolute location', required=True)

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def main():
    args       = parser.parse_args()
    file_in    = args.file

    logging.info("Opening .DS_Store file %s" % file_in)

    with DSStore.open(file_in) as dsfile:
        for elem in dsfile:
            logging.info("- File [%s] %s bytes, %s => [%s]" % (elem.filename, elem.byte_length(), elem.type, elem.value))

    logging.info("All done!")
    sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# coding=utf-8


import sys
import tempfile

# hack until setup.py is done and we are installing it via pip/setuptools
sys.path.append("/home/kinow/Development/python/workspace/cylc/lib/")
from eralchemy import render_er

from cylc.rundb import CylcSuiteDAO


def main():
    """Create cylc public database, then run diagram creation tool."""
    with tempfile.NamedTemporaryFile() as tf:
        # is_public=False triggers the creation of tables
        CylcSuiteDAO(db_file_name=tf.name, is_public=False)
        db_name = "sqlite:///{}".format(tf.name)
        render_er(db_name, "cylc-database.png")


if __name__ == '__main__':
    main()
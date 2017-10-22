#!/usr/bin/env python3

"""
Recursively iterates the given path, looking for .java files. For
each file found, it parses the javadoc, and spell checks it, producing
an HTML file with the final report.
"""

import glob, sys, os
# For displaying the overall progress
from tqdm import tqdm
import contextlib
from time import sleep
# For parsing Java files
import javalang
# For cleaning up text
import re
import string
# For sentence tokenizing
import enchant.tokenize
# For HTML clean-up
from bs4 import BeautifulSoup
# For running mwic
import subprocess
# Document store
from tinydb import TinyDB, Query
# To convert mwic colored output to HTML
#from ansi2html import Ansi2HTMLConverter

from pprint import pprint as pp

# For using print with tqdm progress bar in progress...
class DummyTqdmFile(object):
    """Dummy file-like that will write to tqdm"""
    file = None
    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()

@contextlib.contextmanager
def std_out_err_redirect_tqdm():
    orig_out_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
        yield orig_out_err[0]
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout/err if necessary
    finally:
        sys.stdout, sys.stderr = orig_out_err

# Which files to discard
REGEXES = [
    re.compile("^Test.*\.java$"),
    re.compile("^.*Test\.java$"),
    re.compile("^TS_.*\.java"),
    re.compile("^IT_.*\.java")
]

# Tokenizer
split_words = None
try:
    split_words = enchant.tokenize.get_tokenizer("en")
except enchant.errors.TokenizerNotFoundError:
    split_words = enchant.tokenize.get_tokenizer(None)

def spellcheck_javadocs(entry):
    filename = entry['file_name']
    contents = entry['text']

    contents = [x.strip(string.punctuation) for x in contents.split('\n')]
    contents = [x for x in contents if x not in ['/**', '*', '*/']]
    #contents = [x for x in contents if has_more_than_one_upper_case_or_camel_case(x) or x in ['.', ',', '-', '|', '']]
    contents = [re.sub('^\*\s*', '', x) for x in contents]
    contents = [re.sub('@param\s+([a-zA-Z0-9_]+)', '', x) for x in contents]
    contents = [re.sub('@return\s+([a-zA-Z0-9_]+)', '', x) for x in contents]
    contents = [re.sub('@author\s+([a-zA-Z0-9_]+)', '', x) for x in contents]
    contents = [re.sub('\{@[a-zA-Z]+\s+([^\}]*)\}', r'\1', x) for x in contents]
    soup = BeautifulSoup("<p>%s</p>" % contents, "lxml")
    contents = '\n'.join(soup.findAll(text=True))
    # will create a colored output, and then convert to HTML
    result = subprocess.run(
        ['mwic', '--language', 'en', '--input-encoding', '"ISO-8859-1"', '--camel-case', '--compact', '--suggest', '3', '--output-format', 'color'],
        stdout=subprocess.PIPE,
        input=contents.encode('iso-8859-1')
    )
    output = result.stdout.decode('iso-8859-1')
    # output = Ansi2HTMLConverter().convert(output)
    if output != None and output != '':
        print(output)
        print("File: %s" % filename)
        input("Press Enter to continue...")
    

def add_javadoc(javadoc, contents):
    if javadoc != None and javadoc != '':
        contents.append(javadoc)

def load_file_contents(filename, db):
    abs_file_path = os.path.abspath(filename)
    with open(abs_file_path) as f:
        tree = javalang.parse.parse(f.read())
        contents = []
        for class_decl in tree.types:
            #class_name = class_decl.name
            add_javadoc(class_decl.documentation, contents)
            for constructor in class_decl.constructors:
                add_javadoc(constructor.documentation, contents)
                
            for method in class_decl.methods:
                add_javadoc(method.documentation, contents)

            if len(contents) < 1:
                continue
            file_contents = '\n'.join(contents)
            db.insert({'file_name': abs_file_path, 'text': file_contents})

def main():
    files = []
    db_location = '/tmp/spell.json'
    for filename in glob.iglob("**/*.java", recursive=True):
        basename = os.path.basename(filename)
        if any(regex.match(basename) for regex in REGEXES):
            #print("Ignoring %s" % filename)
            continue
        files.append(filename)

    total_files = len(files)

    with std_out_err_redirect_tqdm() as orig_stdout:
        db_exists = os.path.isfile(db_location)
        db = TinyDB(db_location)
        if not db_exists:
            db = TinyDB(db_location)
            print("Loading %d files" % total_files)
            pbar = tqdm(total=total_files, file=orig_stdout, dynamic_ncols=True)
            for filename in files:
                try:
                    load_file_contents(filename, db)
                    pbar.update(1)
                except Exception as e:
                    print(e)
                    pbar.update(1)
            print("Database created and loaded!")
            pbar.close()

        total_files = len(db)
        print("Spell Checking %d entries in the document database" % total_files)
        pbar = tqdm(total=total_files, file=orig_stdout, dynamic_ncols=True)
        for entry in db:
            try:
                spellcheck_javadocs(entry)
                pbar.update(1)
            except Exception as e:
                print(e)
                pbar.update(1)
        pbar.close()

    sys.exit(0)

if __name__ == '__main__':
    main()

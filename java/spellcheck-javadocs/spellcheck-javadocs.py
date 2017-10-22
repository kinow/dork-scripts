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
# To convert mwic colored output to HTML
#from ansi2html import Ansi2HTMLConverter

from pprint import pprint as pp

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

REGEXES = [
    re.compile("^Test.*\.java$"),
    re.compile("^.*Test\.java$")
]

split_words = None
try:
    split_words = enchant.tokenize.get_tokenizer("en")
except enchant.errors.TokenizerNotFoundError:
    split_words = enchant.tokenize.get_tokenizer(None)

def process_javadoc(javadoc):
    output = ''
    if javadoc != None and javadoc != '':
        javadoc = [x.strip(string.punctuation) for x in javadoc.split('\n')]
        javadoc = [x for x in javadoc if x not in ['/**', '*', '*/']]
        #javadoc = [x for x in javadoc if has_more_than_one_upper_case_or_camel_case(x) or x in ['.', ',', '-', '|', '']]
        javadoc = [re.sub('^\*\s*', '', x) for x in javadoc]
        javadoc = [re.sub('\{@[a-zA-Z]+\s+([^\}]*)\}', r'\1', x) for x in javadoc]
        soup = BeautifulSoup("<p>%s</p>" % javadoc, "lxml")
        javadoc = ' '.join(soup.findAll(text=True))
        # will create a colored output, and then convert to HTML
        result = subprocess.run(
            ['mwic', '--language', 'en', '--input-encoding', '"ISO-8859-1"', '--camel-case', '--compact', '--suggest', '3', '--output-format', 'color'],
            stdout=subprocess.PIPE,
            input=javadoc.encode('iso-8859-1')
        )
        output = result.stdout.decode('iso-8859-1')
        # if output != None and output != '':
        #     output = Ansi2HTMLConverter().convert(output)
    return output

def spellcheck_javadocs(filename):
    tqdm.write("Processing %s" % filename)
    abs_file_path = os.path.abspath(filename)
    with open(abs_file_path) as f:
        tree = javalang.parse.parse(f.read())
        reports = []

        for class_decl in tree.types:
            class_name = class_decl.name
            javadoc = class_decl.documentation
            output = process_javadoc(javadoc)
            if output != None and output != '':
                reports.append(output)
            for constructor in class_decl.constructors:
                javadoc = constructor.documentation
                output = process_javadoc(javadoc)
                if output != None and output != '':
                    reports.append(output)

            for method in class_decl.methods:
                javadoc = method.documentation
                output = process_javadoc(javadoc)
                if output != None and output != '':
                    reports.append(output)
        if len(reports) > 0:
            print('\n'.join(reports))
            print("File: %s" % filename)
            input("Press Enter to continue...")
            print("\n\n\033[92m========================================\033[0m\n\n")

def main():
    files = []
    for filename in glob.iglob("**/*.java", recursive=True):
        basename = os.path.basename(filename)
        if any(regex.match(basename) for regex in REGEXES):
            #print("Ignoring %s" % filename)
            continue
        files.append(filename)

    with std_out_err_redirect_tqdm() as orig_stdout:
        pbar = tqdm(total=len(files), file=orig_stdout, dynamic_ncols=True)
        for filename in files:
            try:
                spellcheck_javadocs(filename)
                pbar.update(1)
            except Exception as e:
                #print("Unexpected error parsing [%s]: %s" % (filename, sys.exc_info()[0]))
                pp(e)
                #sys.exit(1)
                pbar.update(1)
        pbar.close()

    sys.exit(0)

if __name__ == '__main__':
    main()

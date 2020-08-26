#!/usr/bin/env python3

# requirements: javalang, tabulate

import os, sys, glob
from pprint import pprint as pp

import javalang
from tabulate import tabulate

def find_entity(filename):
    """
    Parse a class, look for the @Entity annotation. If found, tries to locate
    the table name. If none was given, then assumes the class name matches the
    table name.
    """
    table_name = None
    entity_found = False
    abs_file_path = os.path.abspath(filename)
    with open(abs_file_path) as f:
        tree = javalang.parse.parse(f.read())
        class_decl = tree.types[0]
        for ann in class_decl.annotations:
            if ann.name == 'Entity':
                entity_found = True
            if ann.name == 'Table':
                if ann.element is not None:
                    for elem in ann.element:
                        if elem.name == 'name':
                            table_name = elem.value.value.upper().strip().replace('"', '')

    # Only return if it has both @Entity and @Table
    if entity_found:
        return table_name
    else:
        return None

def main():
    """
    The input for the program is a FILE that contains a Java class.

    The Java class contains a Hibernate Entity.

    The program will collect the classes that are entities, and will catalogue the tables mapped.
    This can be useful for identifying when more than one entity is mapping the same table.

    It assumes each class will contain at most one entity.
    """
    # From: https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
    script_dir         = os.path.dirname(__file__)
    # abs_file_path     = os.path.join(script_dir, 'class.txt')

    #table_class = dict()
    table_class = list()

    for filename in glob.iglob("**/*.java", recursive=True):
        try:
            table_name = find_entity(filename)
            if table_name is not None:
                #if table_name not in table_class:
                #    table_class[table_name] = list()
                #table_class[table_name].append(filename)
                table_class.append([table_name, filename])
        except Exception as e:
            print("Unexpected error parsing [%s]: %s" % (filename, sys.exc_info()[0]))

    table_class.sort()
    print(tabulate(table_class))

if __name__ == '__main__':
    main()
    sys.exit(0)

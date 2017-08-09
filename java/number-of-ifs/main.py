#!/usr/bin/env python3

import glob, sys, os
import javalang


def count_ifs(filename):
	abs_file_path = os.path.abspath(filename)
	with open(abs_file_path) as f:
		tree = javalang.parse.parse(f.read())


	return 0

def main():
	"""
	Recursively iterates the given path, looking for .java files. For
	each file found, it parses and counts the number of if's found.
	"""

	sum = 0

	for filename in glob.iglob("**/*.java", recursive=True):
		try:
			sum += count_ifs(filename)
		except:
			print("Unexpected error parsing [%s]: %s" % (filename, sys.exc_info()[0]))

	print("Found %d if statements!" % sum)

	sys.exit(0)

if __name__ == '__main__':
	main()

#/usr/bin/env python3

import os, sys, re
from prettytable import PrettyTable

artifact_regex = re.compile(r"^index: (.*\.jar)(.*)", flags=re.IGNORECASE)

deleted = set()
updated_or_added = set()
t = PrettyTable(['Status', 'Artifact', 'Version', 'Action'])

def is_num(char):
	r = False
	try:
		val = int(char)
		r = True
	except ValueError:
		pass
	return r

def get_version(jar_name):
	version = ''
	last_idx = jar_name.rfind('/') + 1
	artifact_name = jar_name[last_idx:]
	last_idx = artifact_name.rfind('-')
	if last_idx > 0:
		last_idx += 1
		last_dot_idx = artifact_name.rfind('.')
		possible_version = artifact_name[last_idx:last_dot_idx]
		# for things like -hibernate
		if len(possible_version) > 0 and is_num(possible_version[0]):
			version = possible_version
	return version

with open('SVN_CHANGES.diff', 'r') as f:
	for line in f:
		stripped = line.strip()
		m = artifact_regex.match(stripped)
		if m:
			jar_name     = m.group(1)
			deleted_flag = m.group(2)
			if deleted_flag:
				if jar_name not in deleted:
					deleted.add(jar_name)
			else:
				if jar_name not in updated_or_added:
					updated_or_added.add(jar_name)

# for entry in deleted:
# 	print("{} - DELETED".format(entry))
# print('---')
# for entry in updated_or_added:
# 	print("{} - ADD/UPDATE".format(entry))

for entry in deleted:
	t.add_row(['[   ]', entry, get_version(entry), 'DELETE'])

for entry in updated_or_added:
	t.add_row(['[   ]', entry, get_version(entry), 'ADD/UPD'])

print(t)

sys.exit(0)

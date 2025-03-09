#!/bin/bash

# Print how much each inode or resource is allocating in virtual memory.
#
# Example output for `containerd` on Linux:
# ...
# ...
# Inode or lib/etc 0 (???) uses 4096 bytes (4.0K)
# Inode or lib/etc 0 (???) uses 536866816 bytes (512M)
# Inode or lib/etc 0 (???) uses 4096 bytes (4.0K)
# Inode or lib/etc 0 (???) uses 300609536 bytes (287M)
# Inode or lib/etc 0 (???) uses 4096 bytes (4.0K)
# Inode or lib/etc 0 (???) uses 37572608 bytes (36M)
# Inode or lib/etc 0 (???) uses 4096 bytes (4.0K)
# Inode or lib/etc 0 (???) uses 4165632 bytes (4.0M)
# Inode or lib/etc 0 (???) uses 1048576 bytes (1.0M)
# Inode or lib/etc 0 (???) uses 524288 bytes (512K)
# Inode or lib/etc 0 (???) uses 4096 bytes (4.0K)
# Inode or lib/etc 0 (???) uses 520192 bytes (508K)
# Inode or lib/etc 28587789 (/usr/lib/x86_64) uses 163840 bytes (160K)
# Inode or lib/etc 28587789 (/usr/lib/x86_64) uses 1662976 bytes (1.6M)
# ...
# ...

PID=$1
cat /proc/${PID}/maps | \
	awk -F" " '{ RES="???"; if($6!="") RES=$6; print $1 "-" $5 "-" RES }' | \
	tr "-" " " | \
	xargs -l bash -c 'set -e
		FROM=$0
		TO=$1
		INODE_OR_ZERO=$2
		RESOURCE=$3

		# to decimal, then calculate difference
		FROM=$(bc <<< "ibase=16;${FROM^^}")
		TO=$(bc <<< "ibase=16;${TO^^}")
		DIFF=$((TO-FROM))
		DIFF_HUMAN=$(numfmt --to=iec $DIFF)

		echo "Inode or lib/etc $INODE_OR_ZERO ($RESOURCE) uses $DIFF bytes ($DIFF_HUMAN)"
	'

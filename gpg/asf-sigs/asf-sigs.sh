#!/usr/bin/env bash

# This script has been written for Bash, to work on Linux Ubuntu.
# It utilizes mktemp, pushd/popd, wget, and gpg.
# Author: Bruno P. Kinoshita
# 2017-10 - Auckland/New Zealand
# Licensed under GPL

url=""

# From: https://blog.mafr.de/2007/08/05/cmdline-options-in-shell-scripts/
USAGE="Usage: `basename $0` [-hv] https://repository.apache.org/.../commons/commons-configuration/2.2/"

# Parse command line options.
while getopts hv: OPT; do
    case "$OPT" in
        h)
            echo $USAGE
            exit 0
            ;;
        v)
            echo "`basename $0` version 0.0.1"
            exit 0
            ;;
        \?)
            # getopts issues an error message
            echo $USAGE >&2
            exit 1
            ;;
    esac
done

# Remove the switches we parsed above.
shift `expr $OPTIND - 1`

# We want at least one non-option argument. 
# Remove this block if you don't need it.
if [ $# -eq 0 ]; then
    echo $USAGE >&2
    exit 1
fi

# Access additional arguments as usual through 
# variables $@, $*, $1, $2, etc. or using this loop:
URL=$1

echo "url: ${URL}"

# Use a local temporary directory
BUILD_DIR=$(mktemp -d)
pushd "$BUILD_DIR"

echo "build dir: ${BUILD_DIR}"

# Download KEYS file
KEYS_URL=https://www.apache.org/dist/commons/KEYS

echo "importing KEYS from: ${KEYS_URL}"

wget "$KEYS_URL"
gpg --import KEYS

# Download JARs and signature files

echo "downloading all jars and signature files..."

wget -r -nd -np -e robots=off --wait 1 -R "index.html*" "${URL}"

# Check the files
for x in *.jar; do gpg --verify "${x}".asc; done

# EOF

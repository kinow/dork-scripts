#!/bin/bash
# From: https://superuser.com/questions/36645/how-to-rotate-images-automatically-based-on-exif-data

JHEAD=jhead
SED=sed
CONVERT=convert

for f in *.jpg
do
        orientation=$("$JHEAD" -v "$f" | "$SED" -nr 's:.*Orientation = ([0-9]+).*:\1:p' | uniq)

        if [ -z "$orientation" ]
        then
                orientation=0
        fi

        if [ 1 -lt $orientation ]
        then
                echo "Rotating $f..."
                mv "$f" "$f.bak"
                $CONVERT -auto-orient "$f.bak" "$f"
        fi
done


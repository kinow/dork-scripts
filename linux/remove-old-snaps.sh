#!/bin/bash

sudo snap list --all | awk '/disabled/{print $1, $3}' | \
while read snapname revision; do
  sudo snap remove "$snapname" --revision="$revision"
done

sudo snap set system refresh.retain=2

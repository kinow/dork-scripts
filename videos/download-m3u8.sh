#!/bin/bash

$ youtube-dl --list-formats $URL
# 0 is the format returned/chosen
$ youtube-dl -f 0 --hls-prefer-native $URL

#!/bin/bash

find . -iname '*.pdf' -exec pdfgrep -i '$1' {} +

#!/bin/bash

docker run --rm -it -v "$PWD:/app" -w /app node:20-alpine npm install --ignore-scripts

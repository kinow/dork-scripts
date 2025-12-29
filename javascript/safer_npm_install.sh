#!/bin/bash

docker run --user "$(id -u):$(id -g)" --rm -it -v "$PWD:/app" -w /app node:20-alpine npm install --ignore-scripts
docker run --user "$(id -u):$(id -g)" --rm -it -v "$PWD:/app" -w /app node:20-alpine npm run build --ignore-scripts

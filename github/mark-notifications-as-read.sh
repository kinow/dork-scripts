#!/bin/bash

curl -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token blabla" \
  https://api.github.com/notifications -d "{'last_read_at': '$(date '+%Y-%m-%dT%H:%M:%S')'}"

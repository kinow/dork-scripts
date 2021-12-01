#!/bin/bash

PR=1;git fetch upstream pull/$PR/head:pr-$PR;git checkout pr-$PR

#!/bin/bash

# To go away with some annoying messages that clutter the logs.

# ASF PyCharm license check
# https://youtrack.jetbrains.com/issue/IDEA-161844/PyCharm-sending-unwanted-multicast-packets
ufw deny from 192.168.1.1 to 230.230.230.230

# Router multicast
ufw deny from 192.168.1.1 to 224.0.0.1

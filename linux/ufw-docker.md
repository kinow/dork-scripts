1. Update after rules for UFW

```
# file: /etc/ufw/before.rules

# ok icmp code for FORWARD
-A ufw-before-forward -p icmp --icmp-type destination-unreachable -j ACCEPT
-A ufw-before-forward -p icmp --icmp-type time-exceeded -j ACCEPT
-A ufw-before-forward -p icmp --icmp-type parameter-problem -j ACCEPT
-A ufw-before-forward -p icmp --icmp-type echo-request -j ACCEPT

# # Allow Docker container traffic
-A ufw-before-forward -i docker0 -j ACCEPT
-A ufw-before-forward -o docker0 -j ACCEPT
```

NOTE: the Docker rules MUST come after the icmp rules, or it will fail anyway.

Fixing that, you will get an apparmor error… :sigh:

2. Force Docker to pass UFW rules (UFW was supposed to work integrated with Docker? :shrug:)

```bash
$ sudo ufw allow in on docker0
$ sudo ufw allow out on docker0
```

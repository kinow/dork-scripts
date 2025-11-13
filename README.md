# Dork scripts

You probably don't need these scripts.

But in case you do, all licensed under CC 4.0 International.

## Other tips

* The [Quick and Dirty Port Forwarder](http://home.bawue.de/~john/software/qdpf/) is a great and simple tool!
* Another way to mimic qpdf is through `socat`: `socat -v TCP-LISTEN:1234 TCP:localhost:9999` is from & to, with the `-v` being verbose to print request-response
* Testing SMTP made easy: `sudo python -m smtpd -n -c DebuggingServer localhost:25`
* Checking out pull requests locally: `PR=4410; git fetch upstream && git fetch upstream pull/${PR}/head:pr-${PR} && git checkout pr-${PR}`
* To inspect files created/open/etc. try `inotifywait -m --format '%f' -e create,open ~`

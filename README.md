# Dork scripts

You probably don't need these scripts.

But in case you do, all licensed under CC 4.0 International.

## Other tips

* The [Quick and Dirty Port Forwarder](http://home.bawue.de/~john/software/qdpf/) is a great and simple tool!
* Another way to mimic qpdf is through `socat`: `socat -v TCP-LISTEN:1234 TCP:localhost:9999` is from & to, with the `-v` being verbose to print request-response
* Testing SMTP made easy: `sudo python -m smtpd -n -c DebuggingServer localhost:25`
* Checking out pull requests locally: `PR=4410; git fetch upstream && git fetch upstream pull/${PR}/head:pr-${PR} && git checkout pr-${PR}`
* To inspect files created/open/etc. try `inotifywait -m --format '%f' -e create,open ~`

### perf

- `perf`: linux command line for profiling tools
- `iperf`: for networking perf test
- `jperf`: gui for `iperf`
- `qperf`: like iperf but for RDMA
- `stream`: for memory
- 'valgrind': runs in a runtime, slow, but give a lot of info (useless if your program is a large openmp, may take forever)
- `vtune`: part of oneAPI, predecessor to advisor, identifies hotsposts, bottlenecks, memory issues
- `advisor`: part of oneAPI, helps to optimize code, add or improve vectorization
- `nsight`: part of NVIDIA systems, replaces deprecated NVIDIA visual profiler
- `npb`: from NASA, for parallel benchmarks with different algorithms (some memory intensive, others cpu, disk, etc.)
- `mpi-benchmarks`: from Intel, contains several MPI tests like alltoall, allreduce, broadcast, etc.
- `perftest`: from NVIDIA, useful to test InfiniBand bandwidth (read/write)
- `hpl`: used for TOP500 for benchmarking and reporting stats on systems
- `inotify`: can be used to show number of files used
- `mprof`: part of Python `memory_profiler`
- 

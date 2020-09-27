# glancesQ
To make glances repo compatible with kdb+

### Instructions

1) Add glances_kdb.py to the following glances monitoring repo to ensure glances mechanism can publish to specified kdb+ processes:
```
https://github.com/nicolargo/glances/tree/develop/glances/exports
```

2) Add the example config to /etc/glances/glances.conf, or specify relevant args to use the glances.conf provided in the repo
```
[kdb]
host=localhost
port=5050
```

3) In case debugging is required, one can find the log file paths with the following command:
```
glances -V
```

4) Note that the associated libraries are all required:
```
qpython
glances
bottle
```

5) Example:
```
Glances Server Side:

glances --export kdb
```

```
kdb+ Client Side:

>> q -p 5050
KDB+ 4.0 2020.05.04 Copyright (C) 1993-2020 Kx Systems
l64/ 4(16)core 5797MB hming hming 127.0.1.1 EXPIRE 2021.09.16 KOD #4172901

q)tables[]
`glancesCpu`glancesDiskio`glancesFs`glancesIp`glancesLoad`glancesMem`glancesMemswap`glancesNetwork`glancesPercpu`glancesProcesscount`glancesSystem`glancesUptime
q)glancesCpu
time         total user system idle nice iowait irq softirq steal guest guest_nice ctx_switches interrupts soft_interrupts syscalls time_since_update cpucore history_size cpu_user_careful cpu_user_..
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------..
10:27:25.375 65.3  65.2 14.2   19.1 0    0      0   1.5     0     0     0          2154         1593       1519            0        0.5016096         4       28800        50               70       ..
10:27:28.420 51.2  35.8 8.9    53.6 0    0      0   1.7     0     0     0          17021        12076      8062            0        3.067954          4       28800        50               70       ..
10:27:31.498 29.4  22.4 5.5    70.5 0    0.1    0   1.5     0     0     0          13114        8764       6511            0        3.081875          4       28800        50               70       ..
```


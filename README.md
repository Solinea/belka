# Belka

Belka is your tool to explore your OpenStack based cloud and return valuable machine readable statistics.


## Usage

Belka can be used as follows:

    $ belka -h
    usage: belka [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
   
    belka
   
    optional arguments:
      --version            show program's version number and exit
      -v, --verbose        Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE  Specify a file to log output. Disabled by default.
      -q, --quiet          suppress output except warnings and errors
      -h, --help           show this help message and exit
      --debug              show tracebacks on errors
   
    Commands:
      compute        Query compute nodes for statistics
      help           print detailed help for another command


The compute subcommand provides further options:

    $ belka help compute
    usage: belka compute [-h] [--noheader] [--noindividual] [--noaggregate]
                         [--syslog] [--identifier IDENTIFIER]

    Query compute nodes for statistics

    optional arguments:
      -h, --help            show this help message and exit
      --noheader, -r        Do not print header line
      --noindividual, -i    Do not print individual hypervisor stats
      --noaggregate, -a     Do not summarize hypervisor stats
      --syslog, -s          Send to syslog instead of stdout
      --identifier IDENTIFIER, -d IDENTIFIER
                            identifier string to be included in output


## Features

### Compute

Belka will query your Nova cluster to find the following stats per hypervisor:

* memory_mb
* current_workload
* vcpus
* running_vms
* vcpus_used
* memory_mb_used
* hypervisor_hostname

It can also summarize this information.

Here is an example run of belka:

    $ belka compute
    2013-03-26 05:59:37.166783,memory_mb,current_workload,vcpus,running_vms,vcpus_used,memory_mb_used,hypervisor_hostname
    2013-03-26 05:59:37.604805,128916,0,32,1,1,10752,c13.b0.z1
    2013-03-26 05:59:37.604881,128916,0,32,1,1,4772,c10.b0.z1
    2013-03-26 05:59:37.604951,128915,0,32,0,0,3072,c9.b0.z1
    2013-03-26 05:59:37.605020,128915,0,32,1,2,10752,c12.b0.z1
    2013-03-26 05:59:37.605089,128916,0,32,0,0,3072,c11.b0.z1
    2013-03-26 05:59:37.666876,644578,0,160,3,4,32420,AllHosts

### Storage

Storage requires a user that has the keystone "ResellerAdmin" role. You can add this to your "admin" user with the following command:

    $ keystone user-role-add --user admin --role ResellerAdmin --tenant admin




## Usage

Belka can be used as follows:

    $ belka -h
    usage: belka [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
   
    belka
   
    optional arguments:
      --version            show program's version number and exit
      -v, --verbose        Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE  Specify a file to log output. Disabled by default.
      -q, --quiet          suppress output except warnings and errors
      -h, --help           show this help message and exit
      --debug              show tracebacks on errors
   
    Commands:
      compute        Query compute nodes for statistics
      help           print detailed help for another command


The compute subcommand provides further options:

    $ belka help compute
    usage: belka compute [-h] [--noheader] [--noindividual] [--noaggregate]
                         [--syslog] [--identifier IDENTIFIER]

    Query compute nodes for statistics

    optional arguments:
      -h, --help            show this help message and exit
      --noheader, -r        Do not print header line
      --noindividual, -i    Do not print individual hypervisor stats
      --noaggregate, -a     Do not summarize hypervisor stats
      --syslog, -s          Send to syslog instead of stdout
      --identifier IDENTIFIER, -d IDENTIFIER
                            identifier string to be included in output

## License

Copyright (c) 2013 Solinea, Inc. (code@solinea.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

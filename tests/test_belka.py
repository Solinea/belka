# Copyright (c) 2013 Solinea, Inc. (code@solinea.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from cliff.app import App
# from cliff.command import Command
# from cliff.commandmanager import CommandManager

# from belka.compute import Compute as compute
#
# import unittest2
# import unittest

# import mock


# http://10.11.191.253:8774/v1.1/07ab2eda41f944c2a7a90c5708831450/os-hypervisors
# REQ: curl -i http://10.11.191.253:8774/v1.1/07ab2eda41f944c2a7a90c5708831450/os-hypervisors -X GET -H "X-Auth-Project-Id: CTP" -H "User-Agent: python-novaclient" -H "Accept: application/json" -H "X-Auth-Token: 4cec36f3ef6c452ba61c8c61f0424afd"
# compute_hosts = "{"hypervisors": [{"id": 1, "hypervisor_hostname": "c13.b0.z1"},
#     {"id": 2, "hypervisor_hostname": "c10.b0.z1"},
#     {"id": 3, "hypervisor_hostname": "c9.b0.z1"},
#     {"id": 4, "hypervisor_hostname": "c12.b0.z1"},
#     {"id": 5, "hypervisor_hostname": "c11.b0.z1"}
#     ]}"
#
# http://10.11.191.253:8774/v1.1/07ab2eda41f944c2a7a90c5708831450/os-hypervisors/1
#
# individual_host = '{"hypervisor":
#     {"service":
#         {"host": "10.11.128.23", "id": 12},
#         "vcpus_used": 4,
#         "hypervisor_type": "QEMU",
#         "local_gb_used": 3400,
#         "hypervisor_hostname": "c13.b0.z1",
#         "memory_mb_used": 18432,
#         "memory_mb": 128916,
#         "current_workload": 0,
#         "vcpus": 32,
#         "cpu_info": "{\"vendor\": \"Intel\", \"model\": \"SandyBridge\", \"arch\": \"x86_64\", \"features\": [\"pdpe1gb\", \"osxsave\", \"dca\", \"pdcm\", \"xtpr\", \"tm2\", \"est\", \"smx\", \"vmx\", \"ds_cpl\", \"monitor\", \"dtes64\", \"pbe\", \"tm\", \"ht\", \"ss\", \"acpi\", \"ds\", \"vme\"], \"topology\": {\"cores\": 8, \"threads\": 2, \"sockets\": 1}}",
#         "running_vms": 2,
#         "free_disk_gb": 17081,
#         "hypervisor_version": 1000000,
#         "disk_available_least": 16213,
#         "local_gb": 20481,
#         "free_ram_mb": 110484,
#         "id": 1}
#     }'

# class TestCompute(unittest.TestCase):
#     """Description of command."""
#     pass
#
#
    # def test_headers(self):
    #     x = {"X-Auth-Token": "abcdefghijkl", "X-Auth-Project-Id": "abcdefghijkl",
    #          "User-Agent": "belka", "Accept": "application/json"}
    #     y = compute()
    #     assert y._headers(self,"abcdefghijkl","abcdefghijkl") == x

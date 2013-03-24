import os
import logging
import requests
import sys

from keystoneclient.v2_0 import client

from cliff.lister import Lister


class Compute(Lister):

    log = logging.getLogger(__name__)

    def _hypervisor_list(self,tenant_id, compute_endpoint, token, tenant_name):
        '''Return a list of hypervisor ids in the compute environment'''
        url = ("%s/os-hypervisors" % compute_endpoint)
        hdr = {"X-Auth-Token": token, "X-Auth-Project-Id": tenant_id,
            "User-Agent": "belka", "Accept": "application/json"}
        r = requests.get(url, headers=hdr)
        self.log.debug(r.json())
        hid = [h['id'] for h in r.json()['hypervisors']]
        return hid

    def _hypervisor_detail(self,tenant_id, compute_endpoint, token, tenant_name, hid):
        '''Return dict of a specific hypervisor details'''
        url = ("%s/os-hypervisors/%s" % (compute_endpoint,str(hid)))
        hdr = {"X-Auth-Token": token, "X-Auth-Project-Id": tenant_id,
            "User-Agent": "belka", "Accept": "application/json"}
        r = requests.get(url, headers=hdr)
        stat = r.json()['hypervisor']
        return dict(memory_mb_used=stat['memory_mb_used'], memory_mb=stat['memory_mb'],
            running_vms=stat['running_vms'], vcpus=stat['vcpus'],
            vcpus_used=stat['vcpus_used'], hypervisor_hostname=stat['hypervisor_hostname'],
            current_workload=stat['current_workload'])

    def hypervisors(self, tenant_id, compute_endpoint, token, tenant_name):
        host_stats = []
        hypervisors = self._hypervisor_list(tenant_id, compute_endpoint, token, tenant_name)
        for h in hypervisors:
            host_stats.append(self._hypervisor_detail(tenant_id, compute_endpoint, token, tenant_name, h))
        return host_stats

    def take_action(self, parsed_args):
        keystone = client.Client(username=os.environ.get("OS_USERNAME"),
            password=os.environ.get("OS_PASSWORD"),
            tenant_name=os.environ.get("OS_TENANT_NAME"),
            auth_url=os.environ.get("OS_AUTH_URL"))
        for serv in keystone.service_catalog.catalog["serviceCatalog"]:
            if serv["type"] == 'compute':
                self.compute_endpoint = serv["endpoints"][0]['adminURL']
                break
        for serv in keystone.service_catalog.catalog["serviceCatalog"]:
            if serv["type"] == 'object-store':
                self.object_storage_endpoint = serv["endpoints"][0]['adminURL']
                break
        self.token = keystone.auth_token
        self.tenant_id = keystone.tenant_id
        self.tenant_name = os.environ.get("OS_TENANT_NAME")
        stats = self.hypervisors(self.tenant_id,self.compute_endpoint,self.token,self.tenant_name)
        self.log.debug(stats)
        return (('Stat', 'Value'),
                (stats[0].items())
                )

from datetime import datetime
import os
import logging
import requests
import syslog

from keystoneclient.v2_0 import client

from cliff.command import Command


class Compute(Command):
    '''Query compute nodes for statistics'''

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Compute, self).get_parser(prog_name)
        parser.add_argument('--noheader', '-r', action='store_true',
                            default=False,
                            help="Do not print header line")
        parser.add_argument('--noindividual', '-i', action='store_true',
                            default=False,
                            help="Do not print individual hypervisor stats")
        parser.add_argument('--noaggregate', '-a', action='store_true',
                            default=False,
                            help="Do not summarize hypervisor stats")
        parser.add_argument('--syslog', '-s', action='store_true',
                            default=False,
                            help="Send to syslog instead of stdout")
        parser.add_argument('--identifier', '-d', action='store',
                            default=None,
                            help="identifier string to be included in output")
        return parser

    def _headers(self, token, tenant_id):
        return {"X-Auth-Token": token, "X-Auth-Project-Id": tenant_id,
                "User-Agent": "belka", "Accept": "application/json"}

    def _individual_hypervisor_stats(self, stats):
        for s in stats:
            self.app.stdout.write(str(datetime.now()) + ",")
            self.app.stdout.write(",".join([str(x) for x in s.values()]))
            self.app.stdout.write("\n")

    def _print_line(self, data, use_syslog, idstring):
        if use_syslog is True:
            if os.uname()[0] == "Darwin":
                syslog.openlog("Python")
            message = ("%s,%s,%s,%s,%s,%s,%s" % (
                       data['memory_mb'], data['current_workload'],
                       data['vcpus'], data['running_vms'],
                       data['vcpus'], data['memory_mb_used'],
                       data['hypervisor_hostname']))
            if idstring is not None:
                message = ("%s,%s" % (idstring, message))
            syslog.syslog(syslog.LOG_ALERT, message)
        else:
            self.app.stdout.write(str(datetime.now()) + ",")
            if idstring is not None:
                self.app.stdout.write(idstring + ",")
            self.app.stdout.write(str(data['memory_mb']) + ",")
            self.app.stdout.write(str(data['current_workload']) + ",")
            self.app.stdout.write(str(data['vcpus']) + ",")
            self.app.stdout.write(str(data['running_vms']) + ",")
            self.app.stdout.write(str(data['vcpus']) + ",")
            self.app.stdout.write(str(data['memory_mb_used']) + ",")
            self.app.stdout.write(str(data['hypervisor_hostname']) + "\n")

    def aggregate_hypervisor(self, tenant_id, compute_endpoint,
                             token, tenant_name):
        url = ("%s/os-hypervisors/statistics" % compute_endpoint)
        hdr = self._headers(token, tenant_id)
        r = requests.get(url, headers=hdr)
        stat = r.json()['hypervisor_statistics']
        stat['hypervisor_hostname'] = "AllHosts"
        return stat

    def _hypervisor_list(self, tenant_id, compute_endpoint,
                         token, tenant_name):
        '''Return a list of hypervisor ids in the compute environment'''
        url = ("%s/os-hypervisors" % compute_endpoint)
        hdr = self._headers(token, tenant_id)
        r = requests.get(url, headers=hdr)
        self.log.debug(r.json())
        hid = [h['id'] for h in r.json()['hypervisors']]
        return hid

    def _hypervisor_detail(self, tenant_id, compute_endpoint,
                           token, tenant_name, hid):
        '''Return dict of a specific hypervisor details'''
        url = ("%s/os-hypervisors/%s" % (compute_endpoint, str(hid)))
        hdr = self._headers(token, tenant_id)
        r = requests.get(url, headers=hdr)
        stat = r.json()['hypervisor']
        return dict(memory_mb_used=stat['memory_mb_used'],
                    memory_mb=stat['memory_mb'],
                    running_vms=stat['running_vms'],
                    vcpus=stat['vcpus'], vcpus_used=stat['vcpus_used'],
                    hypervisor_hostname=stat['hypervisor_hostname'],
                    current_workload=stat['current_workload'])

    def hypervisors(self, tenant_id, compute_endpoint, token, tenant_name):
        '''Return a list of hypervisor stat dictionaries'''
        host_stats = []
        hypervisors = self._hypervisor_list(tenant_id, compute_endpoint,
                                            token, tenant_name)
        for h in hypervisors:
            host_stats.append(self._hypervisor_detail(tenant_id,
                              compute_endpoint, token, tenant_name, h))
        return host_stats

    def take_action(self, parsed_args):
        try:
            keystone = client.Client(username=os.environ.get("OS_USERNAME"),
                                     password=os.environ.get("OS_PASSWORD"),
                                     tenant_name=os.environ.get(
                                     "OS_TENANT_NAME"),
                                     auth_url=os.environ.get("OS_AUTH_URL"))
        except Exception, err:
            raise RuntimeError(err)
        for serv in keystone.service_catalog.catalog["serviceCatalog"]:
            if serv["type"] == 'compute':
                self.compute_endpoint = serv["endpoints"][0]['adminURL']
                break
        self.token = keystone.auth_token
        self.tenant_id = keystone.tenant_id
        self.tenant_name = os.environ.get("OS_TENANT_NAME")
        use_syslog = parsed_args.syslog
        if parsed_args.noheader is False:
            h = dict(memory_mb_used="memory_mb_used",
                     memory_mb="memory_mb",
                     running_vms="running_vms",
                     vcpus="vcpus", vcpus_used="vcpus_used",
                     hypervisor_hostname="hypervisor_hostname",
                     current_workload="current_workload")
            self._print_line(h, use_syslog, parsed_args.identifier)
        if parsed_args.noindividual is False:
            stats = self.hypervisors(self.tenant_id, self.compute_endpoint,
                                     self.token, self.tenant_name)
            self.log.debug(stats)
            for s in stats:
                self._print_line(s, use_syslog, parsed_args.identifier)
        if parsed_args.noaggregate is False:
            stat = self.aggregate_hypervisor(self.tenant_id,
                                             self.compute_endpoint,
                                             self.token, self.tenant_name)
            self._print_line(stat, use_syslog, parsed_args.identifier)

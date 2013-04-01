from datetime import datetime
import os
import logging
import requests
import syslog

from cliff.command import Command

import token as conn


class Objectstorage(Command):
    '''Query object storage for usage statistics'''

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Objectstorage, self).get_parser(prog_name)
        parser.add_argument('--noheader', '-r', action='store_true',
                            default=False,
                            help="Do not print header line")
        parser.add_argument('--noindividual', '-i', action='store_true',
                            default=False,
                            help="Do not print individual hypervisor stats")
        parser.add_argument('--syslog', '-s', action='store_true',
                            default=False,
                            help="Send to syslog instead of stdout")
        parser.add_argument('--splunk', '-k', action='store_true',
                            default=False,
                            help="Print values in key=value format\
                                  (useful for splunk)")
        parser.add_argument('--identifier', '-d', action='store',
                            default=None,
                            help="identifier string to be included in output")
        parser.add_argument('--config', '-c', action='store',
                            default=None,
                            help="configuration file to be used")
        return parser

    def _print_line(self, data, use_syslog, splunk, idstring):
        self.log.debug("data is %s" % data)
        if use_syslog is True:
            if os.uname()[0] == "Darwin":
                syslog.openlog("Python")
            if splunk is True:
                message = ("containers=%s,object=%s,bytes=%s,"
                           "name=%s,account=%s," % (
                           data['containers'], data['objects'],
                           data['bytes'], data['name'], data['tenant']))
            else:
                message = ("%s,%s,%s,%s,%s,%s" % (
                           data['containers'], data['objects'],
                           data['bytes'], data['name'], data['tenant']))
            if idstring is not None:
                message = ("%s,%s" % (idstring, message))
            syslog.syslog(syslog.LOG_ALERT, message)
        else:
            self.app.stdout.write(str(datetime.now()) + ",")
            if idstring is not None:
                self.app.stdout.write(idstring + ",")
            self.app.stdout.write(data['containers'] + ",")
            self.app.stdout.write(data['objects'] + ",")
            self.app.stdout.write(data['bytes'] + ",")
            self.app.stdout.write(data['name'] + ",")
            self.app.stdout.write(data['tenant'] + "\n")

    def storage_per_tenant(self, config_file, tenant_id, endpoint,
                           token, tenant_name):
        tenant = conn.get_tenants(config_file)
        self.log.debug("tenants are %s" % tenant)
        self.log.debug("endpoint is %s" % endpoint)
        stats = []
        for t in tenant:
            url = ("%s/v1/AUTH_%s" % (endpoint, t.id))
            self.log.debug(url)
            hdr = conn.headers(token, None)
            r = requests.head(url, headers=hdr)
            self.log.debug(r.status_code)
            self.log.debug(r.headers)
            self.log.debug(r.text)
            if r.status_code is 204:
                stats.append(dict(containers=
                                  r.headers['x-account-container-count'],
                                  objects=r.headers['x-account-object-count'],
                                  bytes=r.headers['x-account-bytes-used'],
                                  tenant=t.id,
                                  name=t.name))
        self.log.debug("stat list is %s" % stats)
        return stats

    def take_action(self, parsed_args):
        cloud = conn.get_token(parsed_args.config)
        if parsed_args.noheader is False:
            h = dict(containers="containers",
                     objects="objects",
                     bytes="bytes",
                     name="name",
                     tenant="tenant")
            self._print_line(h, parsed_args.syslog, parsed_args.splunk,
                             parsed_args.identifier)
        if parsed_args.noindividual is False:
            stats = self.storage_per_tenant(parsed_args.config,
                                            cloud["tenant_id"],
                                            cloud["storage_endpoint"],
                                            cloud["token"],
                                            cloud["tenant_name"])
            self.log.debug(stats)
            for s in stats:
                self._print_line(s, parsed_args.syslog, parsed_args.splunk,
                                 parsed_args.identifier)

import ConfigParser
import logging
import os

from keystoneclient.v2_0 import client

log = logging.getLogger(__name__)


def _headers(self, token, tenant_id):
    return {"X-Auth-Token": token, "X-Auth-Project-Id": tenant_id,
            "User-Agent": "belka", "Accept": "application/json"}


def _get_credentials(self, config_file):
    if config_file is None:
        username = os.environ.get("OS_USERNAME")
        password = os.environ.get("OS_PASSWORD")
        tenant_name = os.environ.get("OS_TENANT_NAME")
        auth_url = os.environ.get("OS_AUTH_URL")
    else:
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        username = config.get('Default', 'OS_USERNAME')
        password = config.get('Default', 'OS_PASSWORD')
        tenant_name = config.get('Default', 'OS_TENANT_NAME')
        auth_url = config.get('Default', 'OS_AUTH_URL')
    return dict(username=username, password=password,
                tenant_name=tenant_name, auth_url=auth_url)


def get_token(self, config_file):
    creds = self._get_credentials(config_file)
    self.log.debug(creds)
    keystone = client.Client(username=creds["username"],
                             password=creds["password"],
                             tenant_name=creds["tenant_name"],
                             auth_url=creds["auth_url"])
    for serv in keystone.service_catalog.catalog["serviceCatalog"]:
        if serv["type"] == 'compute':
            self.compute_endpoint = serv["endpoints"][0]['adminURL']
            break
    for serv in keystone.service_catalog.catalog["serviceCatalog"]:
        if serv["type"] == 'storage':
            self.storage_endpoint = serv["endpoints"][0]['adminURL']
            break
    return dict(token=keystone.auth_token, tenant=keystone.tenant_id,
                tenant_name=creds["tenant_name"],
                compute_endpoint=self.compute_endpoint,
                storage_endpoint=self.storage_endpoint)

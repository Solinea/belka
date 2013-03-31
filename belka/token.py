import ConfigParser
import exception
import logging
import os

from keystoneclient.v2_0 import client

log = logging.getLogger(__name__)


def headers(token, tenant_id):
    if token is None:
        raise exception.MissingTokenError()
    else:
        return {"X-Auth-Token": token, "X-Auth-Project-Id": tenant_id,
                "User-Agent": "belka", "Accept": "application/json"}


def get_credentials(config_file):
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


def get_token(config_file):
    creds = get_credentials(config_file)
    log.debug(creds)
    keystone = client.Client(username=creds["username"],
                             password=creds["password"],
                             tenant_name=creds["tenant_name"],
                             auth_url=creds["auth_url"])
    compute_endpoint = None
    for serv in keystone.service_catalog.catalog["serviceCatalog"]:
        if serv["type"] == 'compute':
            compute_endpoint = serv["endpoints"][0]['adminURL']
            break
    storage_endpoint = None
    for serv in keystone.service_catalog.catalog["serviceCatalog"]:
        if serv["type"] == 'storage':
            storage_endpoint = serv["endpoints"][0]['adminURL']
            break
    return dict(token=keystone.auth_token, tenant_id=keystone.tenant_id,
                tenant_name=creds["tenant_name"],
                compute_endpoint=compute_endpoint,
                storage_endpoint=storage_endpoint)

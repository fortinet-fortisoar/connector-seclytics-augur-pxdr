"""Operations module defines the actions of Seclytics Connector.

Copyright (C) 2014 - 2022 Seclytics Inc. All rights reserved.
"""
import validators
from connectors.core.connector import get_logger, ConnectorError # pylint: disable=E0401
from .utils import Seclytics            # pylint: disable=E0402
from .constants import LOGGER_NAME      # pylint: disable=E0402

logger = get_logger(LOGGER_NAME)


def query_ip(config, params):
    """Get Seclytics api for ip context."""
    ip_addr = params.get('ip')
    if isinstance(ip_addr, bytes):
        ip_addr = ip_addr.decode('utf-8')
    if not validators.ipv4(str(ip_addr)):
        raise ConnectorError(f'Invalid IP Address {ip_addr}')

    endpoint = '/ips/' + ip_addr
    # sample code below to add a custom key
    # api_response.update({'my_custom_response_key': 'my_custom_value'})
    return Seclytics(config).api_get(endpoint)


def query_domain(config, params):
    """Get Seclytics api for domain context."""
    domain = params.get('domain')
    if isinstance(domain, bytes):
        domain = domain.decode('utf-8')
    if not validators.domain(str(domain)):
        raise ConnectorError(f'Invalid domain {domain}')

    endpoint = '/domains/' + domain
    return Seclytics(config).api_get(endpoint)


def query_host(config, params):
    """Get Seclytics api for domain context."""
    host = params.get('host')
    if isinstance(host, bytes):
        host = host.decode('utf-8')
    if not host:
        raise ConnectorError('Missing host input')

    endpoint = '/hosts/' + host
    return Seclytics(config).api_get(endpoint)


def query_file(config, params):
    """Get Seclytics api for file hash context."""
    file_hash = params.get('file_hash')
    if isinstance(file_hash, bytes):
        file_hash = file_hash.decode('utf-8')
    if not file_hash:
        raise ConnectorError('Missing file_hash input')

    endpoint = '/files/' + file_hash
    return Seclytics(config).api_get(endpoint)


def download_predictions(config, params):
    """Download Seclytics prediction data."""
    file_name = params.get('file_name')
    if not file_name:
        file_name = 'fortisoar_predictions.json'
    endpoint = '/bulk/private/' + file_name

    return Seclytics(config).api_get(endpoint)


def check_api_health(config):
    """Check Seclytics api access."""
    auth_endpoint = '/status'
    # Raises an exception on unsuccessful responses
    Seclytics(config).api_get(auth_endpoint)

    # No exceptions, we're good!
    return True

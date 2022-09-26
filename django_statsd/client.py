from django.conf import settings
from datadog import DogStatsd
from django_statsd.exception import DjangoStatsdConfigurationMissingException

"""
# StatsD configuration in Django settings
# ----------------------------------------

STATSD_IGNORED_IPS = ['127.0.0.1']      # optional - ignore metrics from requests from listed ips
STATSD_REQUEST_META_IP_PRECEDENCE_ORDER = ('HTTP_X_ORIGINAL_FORWARDED_FOR', 'REMOTE_ADDR') # optional - default request meta precedence order for ip address

# required | `HOST` and `PORT` must be configured for `default` exporter. Additional exporters are optional, but if configured `HOST` and `PORT` must be specified.
STATSD_EXPORTERS = {
    # default exporter | required
    'default': {
        'HOST': 'localhost',                # required
        'PORT': '9125',                     # required
        'SERVICE_NAME': 'service-name',     # optional - adds a dimension to all your metrics
        'PREFIX': 'service_prefix'          # optional - adds prefix to all metrics
    },
    # secondary exporter | optional
    'exporter_1': {
        'HOST': 'statsd.host',
        'PORT': '9125',
        'SERVICE_NAME': 'service-name',
        'PREFIX': 'service-prefix'
    },
}
"""

_clients = dict()
_default_client = None
_ignored_ips = None
_request_meta_ip_precedence_order = None


def _get(key, default=None):
    return getattr(settings, key, default)


def get_client(exporter_alias: str = 'default'):
    if exporter_alias in _clients:
        return _clients[exporter_alias]

    statsd_exporters: dict = _get('STATSD_EXPORTERS', {})
    exporter_config = statsd_exporters.get(exporter_alias, {})

    host = exporter_config.get('HOST')
    port = exporter_config.get('PORT')
    service_name = exporter_config.get('STATSD_SERVICE_NAME')
    prefix = exporter_config.get('STATSD_PREFIX', None)

    if not (host and port):
        raise DjangoStatsdConfigurationMissingException(exporter_alias)

    constant_tags = []

    if service_name:
        constant_tags.append(f'service:{service_name}')

    client = DogStatsd(host=host, port=port, namespace=prefix, constant_tags=constant_tags)
    _clients[exporter_alias] = client
    return client


if not _default_client:
    _default_client = get_client('default')

if _ignored_ips is None:
    _ignored_ips = _get('STATSD_IGNORED_IPS', [])

if _request_meta_ip_precedence_order is None:
    _request_meta_ip_precedence_order = _get('STATSD_REQUEST_META_IP_PRECEDENCE_ORDER', (
        'HTTP_X_ORIGINAL_FORWARDED_FOR',
        'X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED',
        'HTTP_FORWARDED_FOR',
        'REMOTE_ADDR'
    ))

client = _default_client
IGNORED_IPS = _ignored_ips
REQUEST_META_IP_PRECEDENCE_ORDER = _request_meta_ip_precedence_order

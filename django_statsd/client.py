from django.conf import settings
from datadog import DogStatsd

_client = None
_ignored_ips = None
_request_meta_ip_precedence_order = None


class DjangoStatsdConfigurationMissingException(Exception):

    def __str__(self):
        return 'STATSD_HOST, STATSD_PORT configuration is missing in django settings. ' \
               'Django-Statsd cannot work without these settings.'


def _get(key, default=None):
    return getattr(settings, key, default)


def get_client():
    host = _get('STATSD_HOST')
    port = _get('STATSD_PORT')
    service_name = _get('STATSD_SERVICE_NAME')
    prefix = _get('STATSD_PREFIX', None)

    if not host or not port:
        raise DjangoStatsdConfigurationMissingException()

    constant_tags = []

    if service_name:
        constant_tags.append(f'service:{service_name}')

    return DogStatsd(host=host, port=port, namespace=prefix, constant_tags=constant_tags)


if not _client:
    _client = get_client()

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

client = _client
IGNORED_IPS = _ignored_ips
REQUEST_META_IP_PRECEDENCE_ORDER = _request_meta_ip_precedence_order

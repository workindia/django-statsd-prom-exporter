import time

from django import VERSION as DJANGO_VERSION
from django.http import HttpRequest, HttpResponse

try:
    from django.urls import Resolver404, resolve
except ModuleNotFoundError:
    # fallback for django < 2
    from django.core.urlresolvers import Resolver404, resolve

from django_statsd.client import client, IGNORED_IPS, REQUEST_META_IP_PRECEDENCE_ORDER

if DJANGO_VERSION >= (1, 10, 0):
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object

REQUEST_LATENCY_METRIC_NAME = 'django_request_latency_seconds'
REQUEST_COUNT_METRIC_NAME = 'django_request_count'
REQUEST_EXCEPTION_COUNT_METRIC_NAME = 'django_request_exception_count'


def _get_url_name(request: HttpRequest):
    try:
        return resolve(request.path_info).url_name
    except Resolver404:
        return 'resolve_not_found'


def _get_request_ip(request: HttpRequest):
    for header in REQUEST_META_IP_PRECEDENCE_ORDER:
        header_value = request.META.get(header)

        if header_value:
            return header_value.split(',')[0].strip()


def _is_ip_ignored_in_metrics(request: HttpRequest):
    return _get_request_ip(request) in IGNORED_IPS


class StatsdCountMetricMiddleware(MiddlewareMixin):

    def process_response(self, request: HttpRequest, response: HttpResponse):
        if not _is_ip_ignored_in_metrics(request):
            client.increment(REQUEST_COUNT_METRIC_NAME, tags=[
                f'method:{request.method}',
                f'endpoint:{_get_url_name(request)}',
                f'status:{response.status_code}'
            ])

        return response

    def process_exception(self, request: HttpRequest, exception: HttpResponse):
        if not _is_ip_ignored_in_metrics(request):
            client.increment(REQUEST_EXCEPTION_COUNT_METRIC_NAME, tags=[
                f'method:{request.method}',
                f'endpoint:{_get_url_name(request)}',
                f'exception:{exception.__class__.__name__}'
            ])


class StatsdLatencyMetricMiddleware(MiddlewareMixin):

    def process_request(self, request: HttpRequest):
        request._start_time = time.time()

    def process_response(self, request: HttpRequest, response: HttpResponse):
        if not _is_ip_ignored_in_metrics(request):
            if hasattr(request, '_start_time'):
                _response_time_ms = int((time.time() - request._start_time) * 1000)
                client.histogram(REQUEST_LATENCY_METRIC_NAME, _response_time_ms, tags=[
                    f'method:{request.method}',
                    f'endpoint:{_get_url_name(request)}',
                    f'status:{response.status_code}'
                ])

        return response

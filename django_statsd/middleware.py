import time

from django import VERSION as DJANGO_VERSION
try:
    from django.urls import Resolver404, resolve
except ModuleNotFoundError:
    # fallback for django < 2
    from django.core.urlresolvers import Resolver404, resolve

from django_statsd.client import client

if DJANGO_VERSION >= (1, 10, 0):
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object

REQUEST_LATENCY_METRIC_NAME = 'django_request_latency_seconds'
REQUEST_COUNT_METRIC_NAME = 'django_request_count'
REQUEST_EXCEPTION_COUNT_METRIC_NAME = 'django_request_exception_count'


def _get_url_name(request):
    try:
        return resolve(request.path_info).url_name
    except Resolver404:
        return 'resolve_not_found'


class StatsdCountMetricMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        client.increment(REQUEST_COUNT_METRIC_NAME, tags=[
            f'method:{request.method}',
            f'endpoint:{_get_url_name(request)}',
            f'status:{response.status_code}'
        ])

        return response

    def process_exception(self, request, exception):
        client.increment(REQUEST_EXCEPTION_COUNT_METRIC_NAME, tags=[
            f'method:{request.method}',
            f'endpoint:{_get_url_name(request)}',
            f'exception:{exception.__class__.__name__}'
        ])


class StatsdLatencyMetricMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            _response_time_ms = int((time.time() - request._start_time) * 1000)
            client.histogram(REQUEST_LATENCY_METRIC_NAME, _response_time_ms, tags=[
                f'method:{request.method}',
                f'endpoint:{_get_url_name(request)}',
                f'status:{response.status_code}'
            ])

        return response

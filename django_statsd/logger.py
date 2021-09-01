from django_statsd.client import client

DJANGO_STATSD_METRIC_COUNT = "django_statsd_metric_count_{}"


class StatsdLogger:

    @staticmethod
    def incr(metric_name):
        client.increment(DJANGO_STATSD_METRIC_COUNT.format(metric_name))

    @staticmethod
    def decr(metric_name):
        client.decrement(DJANGO_STATSD_METRIC_COUNT.format(metric_name))

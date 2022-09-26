from typing import List, Optional
from django_statsd.client import get_client

DJANGO_STATSD_METRIC_COUNT = "django_statsd_{}_total"
DJANGO_STATSD_METRIC_HISTOGRAM = "django_statsd_{}_bucket"
DJANGO_STATSD_METRIC_GAUGE = "django_statsd_{}"


class StatsdLogger:
    def __init__(self, exporter_alias: str) -> None:
        self._exporter_alias = exporter_alias
        self._client = get_client(exporter_alias)

    def incr(
        self,
        metric_name: str,
        value: float = 1,
        tags: Optional[List[str]] = None,
        sample_rate: Optional[float] = None,
    ):
        self._client.increment(
            DJANGO_STATSD_METRIC_COUNT.format(metric_name),
            value,
            tags,
            sample_rate,
        )

    def decr(
        self,
        metric_name: str,
        value: float = 1,
        tags: Optional[List[str]] = None,
        sample_rate: Optional[float] = None,
    ):
        self._client.decrement(
            DJANGO_STATSD_METRIC_COUNT.format(metric_name),
            value,
            tags,
            sample_rate,
        )

    def distribition(
        self,
        metric_name: str,
        value: float,
        tags: Optional[List[str]] = None,
        sample_rate: Optional[float] = None,
    ):
        self._client.distribution(
            DJANGO_STATSD_METRIC_HISTOGRAM.format(metric_name),
            value,
            tags,
            sample_rate,
        )

    def gauge(
        self,
        metric_name: str,
        value: float,
        tags: Optional[List[str]] = None,
        sample_rate: Optional[float] = None,
    ):
        self._client.gauge(
            DJANGO_STATSD_METRIC_GAUGE.format(metric_name),
            value,
            tags,
            sample_rate,
        )


statsd_default_logger = StatsdLogger(exporter_alias="default")

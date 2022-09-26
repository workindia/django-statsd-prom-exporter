# django-statsd-prom-exporter

A collection of django middleware to track django + WSGI service metrics accurately via [prom/statsd-exporter](https://github.com/prometheus/statsd_exporter) sidecar + [prometheus](https://prometheus.io/)

## Features
* StatsdCountMetricMiddleware - Request Count & Request Exception Count metrics
* StatsdLatencyMetricMiddleware - Request Latency metrics
* StatsdLogger - Log a custom count metric


## Installation
```
pip install -U django-statsd-prom-exporter
```


## Configuration

To configure django-statsd, you need to add below configuration to django settings

```
# settings.py
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
```


## Usage

### Middleware
Add the following to your `settings.py`
1. Add `django_statsd.middleware.StatsdCountMetricMiddleware` to the top of your `MIDDLEWARE` to get count metrics
2. Add `django_statsd.middleware.StatsdLatencyMetricMiddleware` to the top of your `MIDDLEWARE` to get latency metrics

### Logger
Used to track occurrence of a specific event
```
from django_statsd.logger import StatsdLogger

# some process ran with error
StatsdLogger.incr('process_a_error')
# process error resolved
StatsdLogger.decr('process_a_error')
```


## Build the package

### Build Requirements
- Make
- Python

### Initialise Build Environment
One time initialisation
```
make init
```

### Build and install locally
```
make dist
make install
```


## Changelog

Please find the changelog here: [CHANGELOG.md](CHANGELOG.md)


## Authors

django-statsd-prom-exporter-middleware was written by [Kshitij Nagvekar](mailto:kshitij.nagvekar@workindia.in).

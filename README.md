# django-statsd-prom-exporter-middleware

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
STATSD_HOST = '127.0.0.1'               # required
STATSD_PORT = 8045                      # required
STATSD_SERVICE_NAME = 'service_name'    # optional - adds a dimension to all your metrics
STATSD_PREFIX = ''                      # optional - adds prefix to all metrics

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

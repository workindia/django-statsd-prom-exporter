# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [Unreleased]
### Added
- Support for multiple StatsD exporters
### Changed
- Expected configuration for StatsD in Django settings
- Moved custom exception `DjangoStatsdConfigurationMissingException` to a separate module
### Breaking Changes
- Expected configuration for StatsD exporter has been changed to support multiple exporters. So config varaibles in Django settings:`STATSD_HOST`, `STATSD_PORT`, `STATSD_SERVICE_NAME`, `STATSD_PREFIX` are now deprecated. The new configuration is expected to be present in `STATSD_EXPORTERS`. For the latest configuration parameters check the doc-string in `django_statsd.client` module.
- Custom exception `DjangoStatsdConfigurationMissingException` has been moved to a separate module `django_statsd.exception` and so any existing imports will need to be updated accordingly.

## 0.3.0 (2022-08-04)
### Added
- Ability to ignore metrics from whitelisted IPs

## 0.2.0 (2021-09-02)
### Fixed
- Fixed ModuleNotFound exception raised in django < 2 due to resolve & Resolve404
- Fixed bumptoversion update

## 0.1.0 (2021-09-01)
### Added
- Add datadog statsd client
- Add count and latency middleware
- Add logger

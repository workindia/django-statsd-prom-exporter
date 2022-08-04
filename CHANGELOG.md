# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [Unreleased]
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

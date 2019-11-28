# HEM - HTTP Endpoint Monitor

[![Build Status](https://travis-ci.org/rickymoorhouse/hem.svg?branch=master)](https://travis-ci.org/rickymoorhouse/hem) [![PyPI version fury.io](https://badge.fury.io/py/hemApp.svg)](https://pypi.python.org/pypi/hemApp/) [![Coverage Status](https://coveralls.io/repos/github/rickymoorhouse/hem/badge.svg)](https://coveralls.io/github/rickymoorhouse/hem) [![Docker Build](https://img.shields.io/docker/cloud/build/rickymoorhouse/hem)](https://hub.docker.com/r/rickymoorhouse/hem)

To install hem, use:

    pip install hemApp

Command line syntax:

    Usage: hem [OPTIONS]

    Options:
    --version          Show the version and exit.
    -v, --verbose      Verbose mode, multiple -v options increase verbosity.
    -c, --config PATH  Specifies an alternative config file
    --help             Show this message and exit.

By default hem will use a config file called hem.yaml in the current directory or /etc/hem.yaml unless one is specified with the --config option.


## Config syntax

The config.yaml is made up of sections:

 - settings - general settings
 
```
    frequency: 30 // Frequency to run tests
```

 - metrics - Where to store the results of the testing e.g. graphite:

```
    type: graphite // Name of plugin to use 
    server: 127.0.0.1 // IP or hostname of server
    port: 2003 // Port to use
```

 - tests - the actual endpoints to test

```
    test-name: 
        path: Path to test
        secure: Is this using HTTPS?
        hosts: List of hosts to use 
        certificate: Path to keypair to use for mTLS - must be un-encrypted
        discovery: discovery block for this test - merged with top level block 
```

 - discovery - optional top level discovery config shared across tests

```
    type: dns // Plugin to use
```

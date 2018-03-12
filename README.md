# HEM - HTTP Endpoint Monitor

To install hem, use:

    pip install py-sample --extra-index-url http://hem.rickymoorhouse.co.uk/pypi/

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
 
    frequency: 30 // Frequency to run tests

 - metrics - Where to store the results of the testing e.g. graphite:

    type: graphite // Name of plugin to use 
    server: 127.0.0.1 // IP or hostname of server
    port: 2003 // Port to use

 - tests - the actual endpoints to test

    test-name: 
        path: Path to test
        secure: Is this using HTTPS?
        hosts: List of hosts to use 
        discovery: discovery block for this test - merged with top level block 

 - discovery - optional top level discovery config shared across tests

    type: dns // Plugin to use


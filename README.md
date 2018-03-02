# HEM - HTTP Endpoint Monitor

## Config syntax

The config.yaml is made up of three key sections:

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

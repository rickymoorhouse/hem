""" Discovery of host lists from Consul API over http"""
import requests

def hosts(**kwargs):
    """ return hosts from consul api """
    
    consul_server = kwargs.get("server","127.0.0.1")
    service = kwargs.get("service","consul")
    catalog = requests.get("http://{}:8500/v1/catalog/service/{}".format(consul_server, service)).json()
    results = []
    for node in catalog:
        results.append(node["Address"])
    return results

if __name__ == "__main__":
    print hosts(server="192.168.0.18", service="redis")

""" Discovery of host lists from DNS e.g. Round robin hosts"""
import dns.resolver

def hosts(**kwargs):
    """ return hosts for passed hostname """
    results = []
    answers = dns.resolver.query(kwargs['name'], 'A')
    for rdata in answers:
        results.append(rdata.address)
    return results

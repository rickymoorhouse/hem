""" Discovery of host lists from DNS e.g. Round robin hosts"""
import time
import logging
import dns.resolver

logger = logging.getLogger(name=__name__)


def hosts(**kwargs):
    """ return hosts for passed hostname """
    results = []
    starttime = time.time()
    answers = dns.resolver.query(kwargs['name'], 'A')
    for rdata in answers:
        results.append(rdata.address)
    elapsed = time.time() - starttime
    logger.info("Lookup of {} took {}".format(kwargs['name'], elapsed))
    if 'metrics' in kwargs and None != kwargs['metrics']:
        kwargs['metrics'].stage(
            'discovery_dns.{}.time'.format(kwargs['name'].replace('.','_')), 
            elapsed)
    return results


import dns.resolver

def hosts(*args):
    """ return hosts for passed hostname """
    results = []
    answers = dns.resolver.query(args[0], 'A')
    for rdata in answers:   
        results.append(rdata.address)
    return results

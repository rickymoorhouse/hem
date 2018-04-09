import unittest
import dns.resolver

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp
            hosts = hemApp.discover_hosts({
                "type":"dns",
                "name":"example.com"})
            self.assertEqual(type(hosts), list)
        def test_check_notfound(self):
            import hemApp
            try:
                with self.assertLogs(level='ERROR') as cm:
                    hosts = hemApp.discover_hosts({
                        "type":"dns",
                        "name":"notfound.nonexistent"})
                self.assertEqual(cm.output, ['ERROR:hemApp.drivers.discovery_dns:DNS name notfound.nonexistent not found'])
                self.assertEqual(type(hosts), list)
                self.assertEqual(hosts, [])
            except dns.resolver.NXDOMAIN:
                self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
import unittest
import dns.resolver

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp
            hosts = hemApp.discover_hosts({
                "type":"file",
                "name":"hosts.yaml"})
            self.assertEqual(type(hosts), list)
        
        def test_check_notfound(self):
            import hemApp
            try:
                with self.assertLogs(level='ERROR') as cm:
                    hosts = hemApp.discover_hosts({
                        "type":"file",
                        "name":"notfound.nonexistent"})
                self.assertEqual(cm.output, ['ERROR:hemApp.drivers.discovery_file:File not found'])
            except AttributeError:
                # self.assertLogs doesn't work in Python 2.x
                hosts = hemApp.discover_hosts({
                    "type":"file",
                    "name":"notfound.nonexistent"})
            except FileNotFoundError:
                self.assertFalse(True)
            self.assertEqual(type(hosts), list)
            self.assertEqual(hosts, [])

        def test_check_content(self):
            import hemApp
            hosts = hemApp.discover_hosts({
                "type":"file",
                "name":"tests/hosts.yaml"})
            self.assertEqual(type(hosts), list)
            print(hosts)
            assert 'hostone' in hosts
if __name__ == '__main__':
    unittest.main()
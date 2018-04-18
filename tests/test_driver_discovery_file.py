import unittest
import mock

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

        def test_check_metrics(self, capsys):
            import hemApp
            metrics = hemApp.initialise_metrics({"type":"console"})
            discovery = {
                "type":"file",
                "name":"tests/hosts.yaml",
                "metrics": metrics}
            hemApp.discover_hosts(discovery)
            try:
                captured = capsys.readouterr()
                assert "discovery_file" in captured.out
            except AttributeError:
                print("Capsys not working in python 3.3 or 3.4 - investigating")
            
if __name__ == '__main__':
    unittest.main()
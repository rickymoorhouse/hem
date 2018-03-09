import unittest

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp
            hosts = hemApp.discover_hosts({
                "type":"dns",
                "name":"example.com"})
            self.assertEqual(type(hosts), list)

if __name__ == '__main__':
    unittest.main()
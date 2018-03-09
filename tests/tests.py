import unittest

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp

            check = hemApp.Check('test', '/', secure=True, verify=True)
            self.assertEqual('https://{}/', check.url)
            self.assertTrue(check.verify)

if __name__ == '__main__':
    unittest.main()
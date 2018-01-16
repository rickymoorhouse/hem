import unittest

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hem
            check = hem.Check('http://google.com')
            self.assertEqual(check.url, 'http://google.com')

if __name__ == '__main__':
    unittest.main()
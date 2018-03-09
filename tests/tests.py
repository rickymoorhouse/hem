import unittest
import requests_mock
import datetime

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp

            check = hemApp.Check('test', '/', secure=True, verify=True)
            self.assertEqual('https://{}/', check.url)
            self.assertTrue(check.verify)

        def test_check_invoke(self):
            import hemApp
            with requests_mock.mock() as m:
                m.get('https://1.1.1.1/', text="")
                check = hemApp.Check('test', '/', secure=True, verify=True)
                results = check.test_list(["1.1.1.1"])
                (response, timing) = results[0]
                self.assertTrue(results is not None)
                self.assertEqual(response, 200)
                self.assertEqual(type(timing), datetime.timedelta)

if __name__ == '__main__':
    unittest.main()
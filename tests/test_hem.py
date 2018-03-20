import unittest
import requests_mock
import datetime

class Basics(unittest.TestCase):
        def test_check_init(self):
            import hemApp
            test = {'path':'/', 'secure':True, 'verify':True}
            check = hemApp.Check('test', test)
            assert check.url == 'https://{}/'
            assert check.verify == True

        def test_check_invoke(self):
            import hemApp
            with requests_mock.mock() as m:
                m.get('https://1.1.1.1/', text="")
                test = {'path':'/', 'secure':True, 'verify':True}
                check = hemApp.Check('test', test)
                results = check.test_list(["1.1.1.1"])
                (response, timing) = results[0]
                assert results is not None
                assert response == 200
                assert type(timing) is datetime.timedelta

if __name__ == '__main__':
    unittest.main()
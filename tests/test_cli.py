import unittest
import requests_mock
import datetime
from click.testing import CliRunner

class Basics(unittest.TestCase):
        def test_cli_version(self):
            import hemApp.cli
            runner = CliRunner()
            result = runner.invoke(hemApp.cli.main, ['--version'])
            assert "version" in result.output
        def test_cli_no_config(self):
            import hemApp
            import hemApp.cli
            runner = CliRunner()
            result = runner.invoke(hemApp.cli.main, ['--config', 'no-config.yaml'])
            assert result.exit_code == 2
            #mock_function.assert_called()
            assert "No config" in result.output
        def test_cli_config(self):
            import hemApp
            import hemApp.cli
            runner = CliRunner()
            result = runner.invoke(hemApp.cli.main, [
                '--config', 
                __file__.replace('test_cli.py','test_cli.yaml')
                ])
            assert result.exit_code == -1
            #mock_function.assert_called()
            assert "No config" not in result.output

        def test_cli_nosettings(self):
            import hemApp
            import hemApp.cli
            try:
                with unittest.assertLogs(level='ERROR') as cm:        
                    runner = CliRunner()
                    result = runner.invoke(hemApp.cli.main, [
                        '--config', 
                        __file__.replace('test_cli.py','test_nosettings.yaml'),
                        '-vv'
                        ])
                    assert 'ERROR:hemApp.drivers.discovery_file:File not found' in cm.output
            except AttributeError:
                runner = CliRunner()
                result = runner.invoke(hemApp.cli.main, [
                    '--config', 
                    __file__.replace('test_cli.py','test_nosettings.yaml'),
                    '-vv'
                    ])
            assert result.exit_code == -1
            #mock_function.assert_called()
            assert "No config" not in result.output
                



if __name__ == '__main__':
    unittest.main()
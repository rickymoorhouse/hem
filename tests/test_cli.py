import unittest
import requests_mock
import datetime
from unittest.mock import create_autospec
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
            #mock_function = create_autospec(hemApp.load_config, return_value={})
            runner = CliRunner()
            result = runner.invoke(hemApp.cli.main, ['--config', 'test_cli.yaml'])
            assert result.exit_code == 2
            #mock_function.assert_called()
            assert "No config" in result.output



if __name__ == '__main__':
    unittest.main()
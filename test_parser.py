"""Integration tests for the dockerctl parser using getopt.

This test suite verifies all valid input option combinations for the parser,
including handling of options, commands, compose names, and additional arguments.
Tests are run unprivileged and do not require access to /etc/dockerctl or /etc/docker.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO

from dockerctl.parser import main, VERSION_NR


class TestParserVersion(unittest.TestCase):
    """Tests for --version and -v options."""

    def test_version_long_option(self):
        """Test --version option prints version and exits."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as context:
                main(['--version'])
            self.assertEqual(context.exception.code, 0)
            self.assertIn("dockerctl " + str(VERSION_NR), fake_out.getvalue())

    def test_version_short_option(self):
        """Test -v option prints version and exits."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as context:
                main(['-v'])
            self.assertEqual(context.exception.code, 0)
            self.assertIn("dockerctl " + str(VERSION_NR), fake_out.getvalue())

    def test_version_ignores_other_args(self):
        """Test that --version exits immediately, ignoring other arguments."""
        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['--version', 'start', 'myapp'])
            self.assertEqual(context.exception.code, 0)


class TestParserHelp(unittest.TestCase):
    """Tests for --help and -h options."""

    def test_help_long_option(self):
        """Test --help option prints help text and exits."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as context:
                main(['--help'])
            self.assertEqual(context.exception.code, 0)
            output = fake_out.getvalue()
            self.assertIn('usage:', output)
            self.assertIn('start:', output)
            self.assertIn('stop:', output)

    def test_help_short_option(self):
        """Test -h option prints help text and exits."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as context:
                main(['-h'])
            self.assertEqual(context.exception.code, 0)
            output = fake_out.getvalue()
            self.assertIn('usage:', output)

    def test_help_ignores_other_args(self):
        """Test that --help exits immediately, ignoring other arguments."""
        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['--help', 'start', 'myapp'])
            self.assertEqual(context.exception.code, 0)


class TestParserList(unittest.TestCase):
    """Tests for --list and -l options."""

    @patch('dockerctl.executor.Commands.ls')
    def test_list_long_option(self, mock_ls):
        """Test --list option calls Commands.ls() and exits."""
        with self.assertRaises(SystemExit) as context:
            main(['--list'])
        self.assertEqual(context.exception.code, 0)
        mock_ls.assert_called_once()

    @patch('dockerctl.executor.Commands.ls')
    def test_list_short_option(self, mock_ls):
        """Test -l option calls Commands.ls() and exits."""
        with self.assertRaises(SystemExit) as context:
            main(['-l'])
        self.assertEqual(context.exception.code, 0)
        mock_ls.assert_called_once()

    @patch('dockerctl.executor.Commands.ls')
    def test_list_ignores_other_args(self, mock_ls):
        """Test that --list exits immediately, ignoring other arguments."""
        with self.assertRaises(SystemExit) as context:
            main(['--list', 'start', 'myapp'])
        self.assertEqual(context.exception.code, 0)
        mock_ls.assert_called_once()


class TestParserCommandExecution(unittest.TestCase):
    """Tests for command parsing and execution."""

    @patch('dockerctl.parser.Commands')
    def test_simple_command(self, mock_commands_class):
        """Test parsing of simple command without options."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['start', 'myapp'])

        # Verify Commands was instantiated with correct arguments
        mock_commands_class.assert_called_once_with('myapp', None, [])
        # Verify exec_cmd was called with the command
        mock_instance.exec_cmd.assert_called_once_with('start')

    @patch('dockerctl.parser.Commands')
    def test_command_with_additional_args(self, mock_commands_class):
        """Test parsing of command with additional arguments for docker-compose."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['logs', 'myapp', '-f', '--tail', '100'])

        # Verify Commands was instantiated with additional args
        mock_commands_class.assert_called_once_with('myapp', None, ['-f', '--tail', '100'])
        mock_instance.exec_cmd.assert_called_once_with('logs')

    @patch('dockerctl.parser.Commands')
    def test_command_with_path_option(self, mock_commands_class):
        """Test parsing of command with --path option."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/custom/path', 'start', 'myapp'])

        # Verify Commands was instantiated with path
        mock_commands_class.assert_called_once_with('myapp', '/custom/path', [])
        mock_instance.exec_cmd.assert_called_once_with('start')

    @patch('dockerctl.parser.Commands')
    def test_command_with_path_and_additional_args(self, mock_commands_class):
        """Test parsing with both --path option and additional arguments."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/custom/path', 'logs', 'myapp', '-f'])

        # Verify Commands was instantiated with path and additional args
        mock_commands_class.assert_called_once_with('myapp', '/custom/path', ['-f'])
        mock_instance.exec_cmd.assert_called_once_with('logs')


class TestParserAllCommands(unittest.TestCase):
    """Tests that all supported commands can be parsed."""

    commands = [
        'start', 'stop', 'restart', 'ps', 'up', 'kill', 'rm', 'top', 'logs',
        'images', 'port', 'pull', 'push', 'pause', 'unpause', 'add', 'remove',
        'exec', 'edit', 'show', 'create', 'update', 'ls', 'down'
    ]

    @patch('dockerctl.parser.Commands')
    def test_all_commands_parse_correctly(self, mock_commands_class):
        """Test that all supported commands can be parsed without errors."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        for cmd in self.commands:
            with self.subTest(command=cmd):
                main([cmd, 'testapp'])
                # Verify exec_cmd was called with the command
                calls = [c[0][0] for c in mock_instance.exec_cmd.call_args_list]
                self.assertIn(cmd, calls)


class TestParserOptionCombinations(unittest.TestCase):
    """Tests for various valid option combinations."""

    @patch('dockerctl.parser.Commands')
    def test_path_with_equals_syntax(self, mock_commands_class):
        """Test --path with = syntax (getopt style)."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path=/my/path', 'start', 'app'])

        mock_commands_class.assert_called_once_with('app', '/my/path', [])
        mock_instance.exec_cmd.assert_called_once_with('start')

    @patch('dockerctl.parser.Commands')
    def test_path_with_space_syntax(self, mock_commands_class):
        """Test --path with space syntax (standard getopt style)."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/my/path', 'restart', 'myservice'])

        mock_commands_class.assert_called_once_with('myservice', '/my/path', [])
        mock_instance.exec_cmd.assert_called_once_with('restart')

    @patch('dockerctl.parser.Commands')
    def test_multiple_additional_args(self, mock_commands_class):
        """Test command with multiple additional arguments."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['exec', 'app', 'bash', '-c', 'echo', 'hello'])

        mock_commands_class.assert_called_once_with('app', None, ['bash', '-c', 'echo', 'hello'])
        mock_instance.exec_cmd.assert_called_once_with('exec')

    @patch('dockerctl.parser.Commands')
    def test_path_with_trailing_slash(self, mock_commands_class):
        """Test --path with trailing slash."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/custom/path/', 'start', 'myapp'])

        # Path is passed as-is; executor handles normalization
        mock_commands_class.assert_called_once_with('myapp', '/custom/path/', [])

    @patch('dockerctl.parser.Commands')
    def test_compose_name_with_special_chars(self, mock_commands_class):
        """Test compose_name with special characters."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['start', 'my-app_v1.0'])

        mock_commands_class.assert_called_once_with('my-app_v1.0', None, [])
        mock_instance.exec_cmd.assert_called_once_with('start')


class TestParserErrorHandling(unittest.TestCase):
    """Tests for error handling and edge cases."""

    def test_missing_compose_name(self):
        """Test error when compose_name is missing."""
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['start'])
            self.assertEqual(context.exception.code, 1)

    def test_no_arguments(self):
        """Test error when no arguments provided."""
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main([])
            self.assertEqual(context.exception.code, 1)

    def test_invalid_option(self):
        """Test error handling for invalid options."""
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['--invalid-option', 'start', 'app'])
            self.assertEqual(context.exception.code, 1)

    def test_path_option_without_value(self):
        """Test error when --path is provided without a value."""
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['--path', 'start', 'app'])
            self.assertEqual(context.exception.code, 1)


class TestParserShortOptionCombinations(unittest.TestCase):
    """Tests for combining short options."""

    @patch('dockerctl.parser.Commands')
    def test_combined_short_options_vh(self, mock_commands_class):
        """Test combined short options: -vh (but -v exits first)."""
        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(['-vh', 'start', 'app'])
            # -v exits immediately
            self.assertEqual(context.exception.code, 0)

    @patch('sys.stdout', new=StringIO())
    @patch('dockerctl.executor.Commands.ls')
    def test_combined_short_options_vl(self, mock_ls):
        """Test combined short options: -vl (but -v exits first)."""
        with self.assertRaises(SystemExit) as context:
            main(['-vl', 'start', 'app'])
        # -v exits immediately
        self.assertEqual(context.exception.code, 0)

    @patch('sys.stdout', new=StringIO())
    @patch('dockerctl.executor.Commands.ls')
    def test_combined_short_options_hl(self, mock_ls):
        """Test combined short options: -hl (but -h exits first)."""
        with self.assertRaises(SystemExit) as context:
            main(['-hl', 'start', 'app'])
        # -h exits immediately
        self.assertEqual(context.exception.code, 0)


class TestParserPathVariations(unittest.TestCase):
    """Tests for various path argument formats."""

    @patch('dockerctl.parser.Commands')
    def test_absolute_path(self, mock_commands_class):
        """Test absolute path."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/etc/dockerctl/myapp', 'start', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', '/etc/dockerctl/myapp', [])

    @patch('dockerctl.parser.Commands')
    def test_relative_path(self, mock_commands_class):
        """Test relative path."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', './docker-compose.yml', 'start', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', './docker-compose.yml', [])

    @patch('dockerctl.parser.Commands')
    def test_path_with_spaces(self, mock_commands_class):
        """Test path containing spaces."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/path with spaces/to/compose', 'start', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', '/path with spaces/to/compose', [])

    @patch('dockerctl.parser.Commands')
    def test_path_with_dots(self, mock_commands_class):
        """Test path with dots (parent directory references)."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '../compose/docker-compose.yml', 'start', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', '../compose/docker-compose.yml', [])


class TestParserComplexScenarios(unittest.TestCase):
    """Tests for complex real-world scenarios."""

    @patch('dockerctl.parser.Commands')
    def test_logs_with_docker_compose_options(self, mock_commands_class):
        """Test logs command with docker-compose specific options."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['logs', 'myapp', '-f', '--tail', '50', 'web'])

        mock_commands_class.assert_called_once_with('myapp', None, ['-f', '--tail', '50', 'web'])
        mock_instance.exec_cmd.assert_called_once_with('logs')

    @patch('dockerctl.parser.Commands')
    def test_exec_with_bash_command(self, mock_commands_class):
        """Test exec command passing a bash command."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['exec', 'myapp', 'bash', '-c', 'ls -la'])

        mock_commands_class.assert_called_once_with('myapp', None, ['bash', '-c', 'ls -la'])
        mock_instance.exec_cmd.assert_called_once_with('exec')

    @patch('dockerctl.parser.Commands')
    def test_port_with_service_name(self, mock_commands_class):
        """Test port command with service name as additional arg."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['port', 'myapp', 'web'])

        mock_commands_class.assert_called_once_with('myapp', None, ['web'])
        mock_instance.exec_cmd.assert_called_once_with('port')

    @patch('dockerctl.parser.Commands')
    def test_add_with_path_option(self, mock_commands_class):
        """Test add command with custom path."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/home/user/my-compose', 'add', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', '/home/user/my-compose', [])
        mock_instance.exec_cmd.assert_called_once_with('add')


if __name__ == '__main__':
    unittest.main()

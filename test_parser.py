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


class TestParserMultipleComposeNames(unittest.TestCase):
    """Tests for operating on several compose names in one invocation."""

    @patch('dockerctl.parser.Commands')
    def test_multiple_compose_names_run_same_command(self, mock_commands_class):
        """A single command should apply to each compose name in order."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['start', 'app1', 'app2', 'app3'])

        self.assertEqual(mock_commands_class.call_count, 3)
        self.assertEqual(
            [call_args.args for call_args in mock_commands_class.call_args_list],
            [('app1', None, []), ('app2', None, []), ('app3', None, [])],
        )
        self.assertEqual(mock_instance.exec_cmd.call_count, 3)
        self.assertEqual([call_args[0][0] for call_args in mock_instance.exec_cmd.call_args_list], ['start', 'start', 'start'])

    @patch('dockerctl.parser.Commands')
    def test_path_option_is_retained_for_single_compose_name(self, mock_commands_class):
        """If exactly one compose name is passed, `--path` should remain effective."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['--path', '/custom/path', 'logs', 'myapp', '-f'])

        mock_commands_class.assert_called_once_with('myapp', '/custom/path', ['-f'])
        mock_instance.exec_cmd.assert_called_once_with('logs')


class TestParserUpdateSubcommands(unittest.TestCase):
    """Tests for update transaction flags."""

    @patch('dockerctl.parser.Commands')
    def test_update_backup_flag_parses_compose_name(self, mock_commands_class):
        """`dockerctl update --backup NAME` should preserve the compose name and pass the flag."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['update', '--backup', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', None, ['--backup'])
        mock_instance.exec_cmd.assert_called_once_with('update')

    @patch('dockerctl.parser.Commands')
    def test_update_rollback_flag_parses_compose_name(self, mock_commands_class):
        """`dockerctl update --rollback NAME` should preserve the compose name and pass the flag."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['update', '--rollback', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', None, ['--rollback'])
        mock_instance.exec_cmd.assert_called_once_with('update')

    @patch('dockerctl.parser.Commands')
    def test_update_commit_flag_parses_compose_name(self, mock_commands_class):
        """`dockerctl update --commit NAME` should preserve the compose name and pass the flag."""
        mock_instance = MagicMock()
        mock_commands_class.return_value = mock_instance

        main(['update', '--commit', 'myapp'])

        mock_commands_class.assert_called_once_with('myapp', None, ['--commit'])
        mock_instance.exec_cmd.assert_called_once_with('update')


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


class TestParserUpdateTransactionLifecycle(unittest.TestCase):
    """Tests for update transaction backup/rollback semantics."""

    @patch('dockerctl.executor.subprocess.run')
    def test_backup_tag_uses_backup_suffix_format(self, mock_run):
        """A backup tag should include the backup suffix and timestamp."""
        mock_run.return_value.returncode = 0
        cmd = __import__('dockerctl.executor', fromlist=['Commands']).Commands.__new__(
            __import__('dockerctl.executor', fromlist=['Commands']).Commands
        )
        tag = cmd._backup_image_tag('example/app:1.2.3')
        self.assertRegex(tag, r'^example/app:1\.2\.3-backup-\d{14}$')

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(__import__('dockerctl.executor', fromlist=['Commands']).Commands, '_backup_images')
    def test_update_backup_mode_runs_backup_then_update(self, mock_backup_images, mock_run):
        """Update backup mode must preserve the current image before pulling and recreating."""
        mock_run.return_value.returncode = 0
        cmd = __import__('dockerctl.executor', fromlist=['Commands']).Commands.__new__(
            __import__('dockerctl.executor', fromlist=['Commands']).Commands
        )
        cmd.path = '/tmp/myapp'
        cmd.append = ['backup']
        cmd.exec_cmd = MagicMock()
        cmd.update()
        mock_backup_images.assert_called_once()
        cmd.exec_cmd.assert_has_calls([call('pull'), call('up')])
        self.assertEqual(cmd.append, [])

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(__import__('dockerctl.executor', fromlist=['Commands']).Commands, '_restore_images')
    def test_update_rollback_mode_restores_previous_images(self, mock_restore_images, mock_run):
        """Rollback mode should restore the last backup before recreating the stack."""
        mock_run.return_value.returncode = 0
        cmd = __import__('dockerctl.executor', fromlist=['Commands']).Commands.__new__(
            __import__('dockerctl.executor', fromlist=['Commands']).Commands
        )
        cmd.path = '/tmp/myapp'
        cmd.append = ['rollback']
        cmd.exec_cmd = MagicMock()
        cmd.update()
        mock_restore_images.assert_called_once()
        cmd.exec_cmd.assert_called_once_with('up')
        self.assertEqual(cmd.append, ['--force-recreate'])

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_service_images',
        return_value={'web': 'example/app:1.2.3'},
    )
    def test_rollback_discovers_backup_from_a_separate_invocation(
        self, mock_service_images, mock_run
    ):
        from dockerctl.executor import Commands

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = (
            'example/app:1.2.3-backup-20261112180000\n'
            'example/app:1.2.3-backup-20261112190000\n'
        )
        cmd = Commands.__new__(Commands)

        backups = cmd._restore_images()

        self.assertEqual(
            backups['web'],
            {
                'original': 'example/app:1.2.3',
                'backup': 'example/app:1.2.3-backup-20261112190000',
            },
        )
        mock_service_images.assert_called_once()
        self.assertEqual(mock_run.call_args_list[-1].args[0], [
            'docker', 'tag',
            'example/app:1.2.3-backup-20261112190000',
            'example/app:1.2.3',
        ])

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_service_images',
        return_value={
            'web': 'example/app:1.2.3',
            'worker': 'example/worker:1.2.3',
        },
    )
    def test_rollback_fails_before_partial_restore_when_a_backup_is_missing(
        self, mock_service_images, mock_run
    ):
        from dockerctl.executor import Commands

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'example/app:1.2.3-backup-20261112190000\n'
        cmd = Commands.__new__(Commands)

        with self.assertRaisesRegex(RuntimeError, 'worker'):
            cmd._restore_images()

        mock_service_images.assert_called_once()
        mock_run.assert_called_once()

    @patch.object(__import__('dockerctl.executor', fromlist=['Commands']).Commands, '_clear_backup_state')
    def test_commit_removes_backup_state(self, mock_clear):
        """Commit mode should finalize the transaction by removing any backup state."""
        cmd = __import__('dockerctl.executor', fromlist=['Commands']).Commands.__new__(
            __import__('dockerctl.executor', fromlist=['Commands']).Commands
        )
        cmd.commit()
        mock_clear.assert_called_once()


class TestEditConfirmation(unittest.TestCase):
    """Tests that editing a compose file requires confirmation."""

    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_has_backup_images',
        return_value=True,
    )
    @patch('builtins.input', return_value='y')
    def test_edit_proceeds_when_confirmed(self, mock_input, mock_has_backup_images):
        from dockerctl.executor import Commands

        cmd = Commands.__new__(Commands)
        with patch.object(cmd, 'edit') as mock_edit:
            cmd.exec_cmd('edit')

        mock_has_backup_images.assert_called_once()
        mock_input.assert_called_once()
        mock_edit.assert_called_once()

    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_has_backup_images',
        return_value=True,
    )
    @patch('builtins.input', return_value='n')
    def test_edit_is_cancelled_when_declined(self, mock_input, mock_has_backup_images):
        from dockerctl.executor import Commands

        cmd = Commands.__new__(Commands)
        with patch.object(cmd, 'edit') as mock_edit, patch('sys.stdout', new=StringIO()) as fake_out:
            cmd.exec_cmd('edit')

        mock_has_backup_images.assert_called_once()
        mock_input.assert_called_once()
        mock_edit.assert_not_called()
        self.assertIn('Edit cancelled.', fake_out.getvalue())

    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_has_backup_images',
        return_value=False,
    )
    @patch('builtins.input')
    def test_edit_does_not_prompt_without_matching_backup(
        self, mock_input, mock_has_backup_images
    ):
        from dockerctl.executor import Commands

        cmd = Commands.__new__(Commands)
        with patch.object(cmd, 'edit') as mock_edit:
            cmd.exec_cmd('edit')

        mock_has_backup_images.assert_called_once()
        mock_input.assert_not_called()
        mock_edit.assert_called_once()

    @patch('builtins.input')
    def test_show_does_not_prompt_for_edit_confirmation(self, mock_input):
        from dockerctl.executor import Commands

        cmd = Commands.__new__(Commands)
        cmd.show = MagicMock()
        cmd.exec_cmd('show')

        mock_input.assert_not_called()
        cmd.show.assert_called_once()

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_service_images',
        return_value={'web': 'example/app:1.2.3'},
    )
    def test_backup_detection_matches_compose_image_and_timestamp(
        self, mock_service_images, mock_run
    ):
        from dockerctl.executor import Commands

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = (
            'example/app:1.2.3-backup-10-11-16-45\n'
            'example/app:1.2.3-backup-20261112180000\n'
            'unrelated/app:latest-backup-10-11-16-45\n'
        )
        cmd = Commands.__new__(Commands)

        self.assertTrue(cmd._has_backup_images())
        mock_service_images.assert_called_once()
        mock_run.assert_called_once_with(
            ['docker', 'image', 'ls', '--format', '{{.Repository}}:{{.Tag}}'],
            stdout=__import__('subprocess').PIPE,
            stderr=__import__('subprocess').PIPE,
            text=True,
            check=False,
        )

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_service_images',
        return_value={'web': 'example/app:1.2.3'},
    )
    def test_backup_detection_ignores_unrelated_or_malformed_images(
        self, mock_service_images, mock_run
    ):
        from dockerctl.executor import Commands

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = (
            'example/app:1.2.3-backup-not-a-timestamp\n'
            'example/app:other-backup-10-11-16-45\n'
        )
        cmd = Commands.__new__(Commands)

        self.assertFalse(cmd._has_backup_images())
        mock_service_images.assert_called_once()

    @patch('dockerctl.executor.subprocess.run')
    @patch.object(
        __import__('dockerctl.executor', fromlist=['Commands']).Commands,
        '_service_images',
        return_value={},
    )
    def test_backup_detection_skips_docker_lookup_without_compose_images(
        self, mock_service_images, mock_run
    ):
        from dockerctl.executor import Commands

        cmd = Commands.__new__(Commands)

        self.assertFalse(cmd._has_backup_images())
        mock_service_images.assert_called_once()
        mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()

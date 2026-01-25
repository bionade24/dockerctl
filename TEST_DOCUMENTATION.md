# Integration Tests for dockerctl Parser

## Overview
The test suite in `test_parser.py` provides comprehensive coverage of all valid input option combinations for the dockerctl parser using Python's `unittest` framework.

## Test Coverage

### 1. **TestParserVersion** (3 tests)
- `test_version_long_option`: Tests `--version` prints version and exits
- `test_version_short_option`: Tests `-v` prints version and exits
- `test_version_ignores_other_args`: Verifies `--version` exits immediately, ignoring other arguments

### 2. **TestParserHelp** (3 tests)
- `test_help_long_option`: Tests `--help` prints help text and exits
- `test_help_short_option`: Tests `-h` prints help text and exits
- `test_help_ignores_other_args`: Verifies `--help` exits immediately, ignoring other arguments

### 3. **TestParserList** (3 tests)
- `test_list_long_option`: Tests `--list` calls `Commands.ls()` and exits
- `test_list_short_option`: Tests `-l` calls `Commands.ls()` and exits
- `test_list_ignores_other_args`: Verifies `--list` exits immediately, ignoring other arguments

### 4. **TestParserCommandExecution** (4 tests)
- `test_simple_command`: Tests parsing of simple command without options
- `test_command_with_additional_args`: Tests command with additional docker-compose arguments
- `test_command_with_path_option`: Tests command with `--path` option
- `test_command_with_path_and_additional_args`: Tests combination of `--path` and additional arguments

### 5. **TestParserAllCommands** (1 test with 23 sub-tests)
- `test_all_commands_parse_correctly`: Verifies all 23 supported commands parse correctly:
  - start, stop, restart, ps, up, kill, rm, top, logs
  - images, port, pull, push, pause, unpause, add, remove
  - exec, edit, show, create, update, ls, down

### 6. **TestParserOptionCombinations** (5 tests)
- `test_path_with_equals_syntax`: Tests `--path=/my/path` syntax
- `test_path_with_space_syntax`: Tests `--path /my/path` syntax
- `test_multiple_additional_args`: Tests multiple additional arguments
- `test_path_with_trailing_slash`: Tests path normalization
- `test_compose_name_with_special_chars`: Tests compose names with hyphens and underscores

### 7. **TestParserErrorHandling** (4 tests)
- `test_missing_compose_name`: Tests error when only command provided
- `test_no_arguments`: Tests error when no arguments provided
- `test_invalid_option`: Tests error for unrecognized options
- `test_path_option_without_value`: Tests error when `--path` lacks a value

### 8. **TestParserShortOptionCombinations** (3 tests)
- `test_combined_short_options_vh`: Tests `-vh` combination
- `test_combined_short_options_vl`: Tests `-vl` combination
- `test_combined_short_options_hl`: Tests `-hl` combination

### 9. **TestParserPathVariations** (4 tests)
- `test_absolute_path`: Tests absolute path handling
- `test_relative_path`: Tests relative path handling
- `test_path_with_spaces`: Tests paths with spaces
- `test_path_with_dots`: Tests parent directory references (`../`)

### 10. **TestParserComplexScenarios** (4 tests)
- `test_logs_with_docker_compose_options`: Tests logs command with `-f`, `--tail`, and service name
- `test_exec_with_bash_command`: Tests exec with `bash -c` command
- `test_port_with_service_name`: Tests port command with service name
- `test_add_with_path_option`: Tests add command with custom path

## Key Features

### Mocking Strategy
- Uses `unittest.mock` to mock the `Commands` class and its methods
- Prevents actual file system access (no need for `/etc/dockerctl` or `/etc/docker`)
- Allows testing of unprivileged environments

### Test Independence
- All tests are independent and can run in any order
- Each test mocks necessary dependencies
- No test fixtures or setup/teardown needed

### Coverage of Valid Inputs
1. **Short options**: `-v`, `-h`, `-l`
2. **Long options**: `--version`, `--help`, `--list`, `--path`
3. **Path formats**: Absolute, relative, with spaces, with dots
4. **Option syntax variants**: `--path=value` and `--path value`
5. **All 23 supported commands**
6. **Additional arguments for docker-compose**
7. **Option combinations** (e.g., `--path` with commands and additional args)

### Error Cases
- Missing required arguments
- Invalid options
- Incomplete path option

## Running the Tests

```bash
# Run all tests
python -m unittest test_parser.py -v

# Run specific test class
python -m unittest test_parser.TestParserVersion -v

# Run single test
python -m unittest test_parser.TestParserVersion.test_version_long_option -v
```

## Test Results
All 38 tests verify that:
1. Option parsing works correctly with getopt
2. Help, version, and list options exit immediately
3. Commands are properly parsed with their compose name
4. Additional arguments are preserved and passed through
5. Path options are correctly captured and forwarded
6. Error cases are handled gracefully
7. No file system access is required

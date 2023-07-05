import subprocess

import pytest

from backup_juggler.juggler_cli import get_version
from tests.fixtures_cli import run_backup_juggler
from tests.fixtures_temp import (
    create_directories,
    create_files,
    create_subdirectories_recursively,
)


def test_runs_successfully_bj_script():
    result = subprocess.run(['poetry', 'run', 'bj'])

    assert result.returncode == 0


def test_print_successfully_app_version_message(run_backup_juggler):
    result = run_backup_juggler(options='--version')
    app_version = get_version()

    assert app_version in result.stdout


def test_print_successfully_app_help_message(run_backup_juggler):
    result = run_backup_juggler(options='--help')
    app_help = (
        'Multiple copies of files and directories simultaneously made easy'
    )
    assert app_help in result.stdout


def test_print_successfully_do_backups_help_message(run_backup_juggler):
    result = run_backup_juggler(subcommand='do-backups', options='--help')
    do_backups_help = 'Perform backups of source to destination'

    assert do_backups_help in result.stdout


def test_print_successfully_get_size_help_message(run_backup_juggler):
    result = run_backup_juggler(subcommand='get-size', options='--help')
    get_size_help = 'Calculate the total size of the specified source'

    assert get_size_help in result.stdout


@pytest.mark.parametrize(
    'source_filenames, destination_dirnames',
    [
        (['source1.txt'], ['destination1']),
        (['source1.txt'], ['destination1', 'destination2']),
        (['source1.txt', 'source2.txt'], ['destination1']),
        (['source1.txt', 'source2.txt'], ['destination1', 'destination2']),
    ],
)
def test_runs_cli_do_backups_single_or_multi_source_files_to_single_or_multi_destinations_directories(
    create_files,
    create_directories,
    run_backup_juggler,
    source_filenames,
    destination_dirnames,
):
    source_paths = create_files(source_filenames)
    destination_paths = create_directories(destination_dirnames)
    result = run_backup_juggler(
        subcommand='do-backups',
        sources=source_paths,
        destinations=destination_paths,
    )

    assert result.exit_code == 0


@pytest.mark.parametrize(
    'source_dirnames, destination_dirnames',
    [
        (['source1'], ['destination1']),
        (['source1'], ['destination1', 'destination2']),
        (['source1', 'source2'], ['destination1']),
        (['source1', 'source2'], ['destination1', 'destination2']),
    ],
)
def test_runs_cli_do_backups_single_or_multi_source_directories_to_single_or_multi_destination_directories(
    create_directories,
    run_backup_juggler,
    source_dirnames,
    destination_dirnames,
):
    source_paths = create_directories(source_dirnames)
    destination_paths = create_directories(destination_dirnames)
    result = run_backup_juggler(
        subcommand='do-backups',
        sources=source_paths,
        destinations=destination_paths,
    )

    assert result.exit_code == 0


@pytest.mark.parametrize(
    'source_names',
    [
        (['source1.txt']),
        (['source1']),
        (['source1.txt', 'source2.txt']),
        (['source1.txt', 'source2']),
        (['source1', 'source2']),
    ],
)
def test_runs_cli_get_size_single_or_multi_source_files_and_directories(
    create_files, run_backup_juggler, source_names
):
    source_paths = create_files(source_names)
    result = run_backup_juggler(subcommand='get-size', sources=source_paths)

    assert result.exit_code == 0

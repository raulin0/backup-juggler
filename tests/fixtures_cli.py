import pytest
from typer.testing import CliRunner

from backup_juggler.juggler_cli import app


@pytest.fixture
def run_backup_juggler():
    def _run_backup_juggler(
        options='', subcommand='', sources=[], destinations=[]
    ):
        source_args = []
        for source_path in sources:
            source_args += ['-s', str(source_path)]

        destination_args = []
        for destination_path in destinations:
            destination_args += ['-d', str(destination_path)]

        command = [
            *filter(None, [options, subcommand]),
            *source_args,
            *destination_args,
        ]
        runner = CliRunner()
        result = runner.invoke(app, command)

        return result

    return _run_backup_juggler

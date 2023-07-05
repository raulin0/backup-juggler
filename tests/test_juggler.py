import pytest

from backup_juggler.files_manager import (
    backup,
    calculates_size,
    parallel_backups,
)
from backup_juggler.paths_manager import Paths
from tests.fixtures_temp import (
    create_directories,
    create_files,
    create_subdirectories_recursively,
)


@pytest.mark.parametrize(
    'source_filenames, destination_dirnames',
    [
        (['source1.txt'], ['destination1']),
        (['source1.txt'], ['destination1', 'destination2']),
        (['source1.txt', 'source2.txt'], ['destination1']),
        (['source1.txt', 'source2.txt'], ['destination1', 'destination2']),
    ],
)
def test_if_single_or_multi_source_files_have_been_copied_to_the_destination(
    create_directories,
    create_files,
    source_filenames,
    destination_dirnames,
):
    source_paths = create_files(source_filenames)
    destination_paths = create_directories(destination_dirnames)

    parallel_backups(sources=source_paths, destinations=destination_paths)

    for source_path in source_paths:
        for destination_path in destination_paths:
            destination_file = (
                destination_path / source_path.stem / source_path.name
            )

            assert destination_file.is_file()


@pytest.mark.parametrize(
    'source_filenames, destination_dirnames',
    [
        (['source1.txt'], ['destination1']),
        (['source1.txt'], ['destination1', 'destination2']),
        (['source1.txt', 'source2.txt'], ['destination1']),
        (['source1.txt', 'source2.txt'], ['destination1', 'destination2']),
    ],
)
def test_if_single_or_multi_source_files_have_the_same_size_as_their_copies(
    create_directories,
    create_files,
    source_filenames,
    destination_dirnames,
):
    source_paths = create_files(source_filenames)
    destination_paths = create_directories(destination_dirnames)

    parallel_backups(sources=source_paths, destinations=destination_paths)

    for source_path in source_paths:
        model = Paths(source_path)
        source_file_size = model.total_size
        for destination_path in destination_paths:
            destination_file = (
                destination_path / source_path.stem / source_path.name
            )
            destination_file_size = destination_file.stat().st_size

            assert source_file_size == destination_file_size


@pytest.mark.parametrize(
    'source_dirnames, destination_dirnames',
    [
        (['source1'], ['destination1']),
        (['source1'], ['destination1', 'destination2']),
        (['source1', 'source2'], ['destination1']),
        (['source1', 'source2'], ['destination1', 'destination2']),
    ],
)
def test_if_single_or_multi_source_directories_have_been_copied_to_the_destination(
    create_directories,
    source_dirnames,
    destination_dirnames,
):
    source_paths = create_directories(source_dirnames)
    destination_paths = create_directories(destination_dirnames)

    parallel_backups(sources=source_paths, destinations=destination_paths)

    for destination_path in destination_paths:

        assert destination_path.is_dir()


@pytest.mark.parametrize(
    'source_dirnames, destination_dirnames',
    [
        (['source1'], ['destination1']),
        (['source1'], ['destination1', 'destination2']),
        (['source1', 'source2'], ['destination1']),
        (['source1', 'source2'], ['destination1', 'destination2']),
    ],
)
def test_if_single_or_multi_source_directories_have_the_same_size_as_their_copies(
    create_directories,
    create_subdirectories_recursively,
    source_dirnames,
    destination_dirnames,
):
    source_paths = create_directories(source_dirnames)
    destination_paths = create_directories(destination_dirnames)

    source_structure = {
        'subdir1': {
            'subdir2': {'file1.txt': b'\x00' * (1024 * 1024)},
            'file2.txt': b'\x00' * (1024 * 1024),
        },
        'file3.txt': b'\x00' * (1024 * 1024),
    }

    for source_path in source_paths:
        create_subdirectories_recursively(
            directory_structure=source_structure, parent_path=source_path
        )

    parallel_backups(sources=source_paths, destinations=destination_paths)

    for source_path in source_paths:
        model = Paths(source_path)
        source_dir_size = model.total_size
        for destination_path in destination_paths:
            destination_dir = destination_path / source_path.name
            destination_dir_size = sum(
                f.stat().st_size for f in destination_dir.rglob('*.*')
            )

            assert source_dir_size == destination_dir_size


def test_backup_method_return_filenotfounderror_exception(tmp_path):
    source_path = tmp_path / 'nonexistent.txt'
    destination_path = tmp_path / 'destination'

    with pytest.raises(FileNotFoundError) as error:
        backup(source=source_path, destination=destination_path)

    error_message = f'{source_path.name} does not exist.'

    assert error_message == error.value.args[0]


def test_calculates_size_return_the_expected_size_of_the_source_files(
    capfd,
    create_files,
):
    source_paths = create_files(['source1.txt', 'source2.txt'])
    calculates_size(source_paths)
    captured = capfd.readouterr()

    assert 'Total size: 2.00 MB' in captured.out


def test_calculates_size_return_the_expected_size_of_the_source_dirs(
    capfd, create_directories, create_subdirectories_recursively
):
    source_paths = create_directories(['source1', 'source2'])
    source_structure = {
        'subdir1': {
            'subdir2': {'file1.txt': b'\x00' * (1024 * 1024)},
            'file2.txt': b'\x00' * (1024 * 1024),
        },
        'file3.txt': b'\x00' * (1024 * 1024),
    }
    for source_path in source_paths:
        create_subdirectories_recursively(
            directory_structure=source_structure, parent_path=source_path
        )
    calculates_size(source_paths)
    captured = capfd.readouterr()

    assert 'Total size: 6.00 MB' in captured.out


def test_calculates_size_method_return_filenotfounderror_exception(tmp_path):
    source_path = tmp_path / 'nonexistent.txt'
    source_paths = [source_path]
    with pytest.raises(FileNotFoundError) as error:
        calculates_size(sources=source_paths)

    error_message = f'{source_path.name} does not exist.'

    assert error_message == error.value.args[0]

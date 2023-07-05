import pytest


@pytest.fixture
def create_files(tmp_path):
    def _create_files(filenames):
        paths = []
        for filename in filenames:
            path = tmp_path / filename
            paths.append(path)
            with open(path, 'wb') as f:
                f.write(b'\x00' * (1024 * 1024))
        return paths

    return _create_files


@pytest.fixture
def create_directories(tmp_path):
    def _create_directories(dirnames):
        paths = []
        for dirname in dirnames:
            path = tmp_path / dirname
            path.mkdir(parents=True, exist_ok=True)
            paths.append(path)
        return paths

    return _create_directories


@pytest.fixture
def create_subdirectories_recursively():
    def _create_subdirectories_recursively(directory_structure, parent_path):
        for name, contents in directory_structure.items():
            current_path = parent_path / name
            if isinstance(contents, dict):
                current_path.mkdir(parents=True, exist_ok=True)
                _create_subdirectories_recursively(
                    contents, parent_path=current_path
                )
            else:
                with current_path.open('wb') as f:
                    f.write(contents)

    return _create_subdirectories_recursively

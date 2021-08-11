from pathlib import Path
import json

from package_wrapper.manifest.filehash import (
    file_hash_create,
    file_hash_check,
    FileHashE,
)
from package_wrapper.manifest.filehash import file_hash_create_hash_file


class ManifestE(BaseException):
    """
    Basic exception for manifest related tasks
    """

    def __init__(self, msg):
        super(ManifestE, self).__init__()
        self.msg = msg


class ManifestFile:
    """
    Handle a manifest file that contains a list of artifacts (path to file, optional hash sum)
    """

    def __init__(self, hash_method="sha256"):
        self.database = dict()
        self.hash_method = hash_method

    def add_meta_data(self, keyword: str, content):
        self.database[keyword] = content

    def add_meta_data_file(self, meta_data_path: Path):
        data = json.loads(meta_data_path.read_bytes())
        for key, value in data.items():
            self.add_meta_data(keyword=key, content=value)

    def add_folder(self, path_to_directory: Path):
        """
        Adds all files found in a certain folder to the manifest
        database
        :param path_to_directory:
        :return: True if succeeded, otherwise False
        """

        if not path_to_directory.is_dir():
            raise ManifestE("No such directory")

        files = [
            _file
            for _file in path_to_directory.glob("**/*")
            if path_to_directory.joinpath(_file).is_file()
        ]

        for file in files:
            _abs_path = file.absolute()
            self.add_artifact_to_db(_abs_path, path_to_directory)

        return True

    def add_artifact_to_db(self, path_to_file: Path, base_path: Path):
        if "files" not in self.database.keys():
            self.database["files"] = dict()

        _hash = None
        if path_to_file in self.database.keys():
            raise ManifestE("duplicated file: {path_to_file}")

        try:
            _hash = (
                self.hash_method
                + ":"
                + file_hash_create(file_name=path_to_file, hash_method=self.hash_method)
            )
        except FileHashE as exception:
            raise ManifestE(exception.msg)

        rel_file_path = Path.relative_to(path_to_file, base_path)
        self.database["files"][str(rel_file_path)] = _hash

        return True

    def retrive_contents(self):
        return self.database

    def check_hashes_in_db(self) -> bool:
        _match = True
        for _file in self.database["files"]:
            (_hash_method, _hash_string) = self.database[_file].split(":")
            try:
                _match = file_hash_check(
                    file_name=Path(_file),
                    hash_string=_hash_string,
                    hash_method=_hash_method,
                )
            except FileHashE:
                raise ManifestE(f"error when checking hash for {_file}")

            if not _match:
                break

        return _match

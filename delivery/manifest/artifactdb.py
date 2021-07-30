from pathlib import Path
from delivery.manifest.filehash import file_hash_create, file_hash_check, FileHashE


class ArtifactE(BaseException):
    def __init__(self, msg: str):
        super(ArtifactE, self).__init__()
        self.msg = msg


class ArtifactDB:
    def __init__(self, hash_method: str="sha256"):
        self.database = {}
        self.hash_method = hash_method

    def add_artifact_to_db(self, path_to_file: Path):
        _hash = None
        if path_to_file in self.database.keys():
            raise ArtifactE(f"duplicated file: {path_to_file}")

        try:
            _hash = self.hash_method + ":" + file_hash_create(file_name=path_to_file, hash_method=self.hash_method)
        except FileHashE as exception:
            raise ArtifactE(exception.msg)

        self.database[path_to_file] = {"file hash": _hash}

    def check_hashes_in_db(self) -> bool:
        _match = True
        for _file in self.database:
            (_hash_method, _hash_string) = self.database[_file]["file hash"].split(":")
            try:
                _match = file_hash_check(file_name=Path(_file),
                                         hash_string=_hash_string,
                                         hash_method=_hash_method)
            except FileHashE:
                raise ArtifactE(f"error when checking hash for {_file}")

            if not _match:
                break

        return _match

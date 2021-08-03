from datetime import datetime
from pathlib import Path
import json

from delivery.manifest.artifactdb import ArtifactE, ArtifactDB
from delivery.manifest.filehash import file_hash_create_hash_file


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
        self.contents = ArtifactDB(hash_method=hash_method)
        self._meta = dict()
        self._meta["created (utc)"] = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

    def add_meta_data(self, keyword: str, content):
        self._meta[keyword] = content

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

        try:
            for file in files:
                _abs_path = file.absolute()
                self.add_artifact(_abs_path, path_to_directory)
        except ArtifactE as expression:
            raise ManifestE(expression.msg)

        return True

    def add_artifact(self, path_to_file: Path, path_to_directory: Path):
        """
        Adds as an artifact to the manifest DB
        :param path_to_file:
        :return:
        """
        try:
            self.contents.add_artifact_to_db(path_to_file, path_to_directory)
        except ArtifactE as expression:
            raise ManifestE(expression.msg)

        return True

    def retrive_contents(self):
        contents = self._meta
        contents["contents"] = self.contents.database
        return contents

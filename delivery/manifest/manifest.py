from datetime import datetime
from pathlib import Path
import logging
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

    def __init__(self, hash_method='sha256'):
        self.contents = ArtifactDB(hash_method=hash_method)
        self._meta = dict()
        self._meta['created'] = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Manifest instantiated, hash:')

    def add_folder(self, path_to_directory: Path):
        """
        Adds all files found in a certain folder to the manifest
        database
        :param path_to_directory:
        :return: True if succeeded, otherwise False
        """
        if not path_to_directory.is_dir():
            raise ManifestE("No such directory")

        files = [_file for _file in path_to_directory.glob('**/*') if path_to_directory.joinpath(_file).is_file()]

        try:
            for file in files:
                _abs_path = file.absolute()
                self.add_artifact(_abs_path)
        except ArtifactE as expression:
            raise ManifestE(expression.msg)

        return True

    def add_artifact(self, path_to_file: Path):
        """
        Adds as an artifact based in it's relative path to the manifest DB
        :param path_to_file:
        :return:
        """
        try:
            self.contents.add(path_to_file)
        except ArtifactE as expression:
            raise ManifestE(expression.msg)

        return True

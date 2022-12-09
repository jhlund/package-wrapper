import tarfile
import zipfile
from pathlib import Path


class ArchiveE(Exception):
    def __init__(self, msg: str):
        super(ArchiveE, self).__init__()
        self.msg = msg


class Archive:
    def __init__(self, file_name: Path, archive_type: str):
        self.archive = file_name
        self.archive_type = archive_type

    @staticmethod
    def _validate(file_path: Path):
        if not file_path.exists():
            raise ArchiveE("file: %s not found" % file_path)
        if file_path.name.endswith("tar.gz") or file_path.name.endswith("tar"):
            if not tarfile.is_tarfile(file_path):
                raise ArchiveE("file %s is not a TAR ball" % file_path)
        elif file_path.name.endswith("zip"):
            if not zipfile.is_zipfile(file_path):
                raise ArchiveE("file %s is not a zip file" % file_path)

    def extract(self, out_dir: Path):
        Archive._validate(self.archive)

        if self.archive_type == "tar.gz":
            with tarfile.open(self.archive, "r:gz") as tar_ref:
                
                import os
                
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar_ref, out_dir)
        elif self.archive_type == "tar":
            with tarfile.open(self.archive, "r:") as tar_ref:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar_ref, out_dir)
        elif self.archive_type == "zip":
            with zipfile.ZipFile(self.archive, "r") as zip_ref:
                zip_ref.extractall(out_dir)
        else:
            raise ArchiveE("unsupported file format")

    def compress(self, dir_path: Path):
        if not dir_path.is_dir():
            raise ArchiveE("path: %s is not a directory" % dir_path)

        files = [
            _file
            for _file in dir_path.glob("**/*")
            if dir_path.joinpath(_file).is_file()
        ]

        # handles TAR, TGZ and ZIP
        if self.archive_type == "tar.gz":
            with tarfile.open(self.archive, "w:gz") as tar_ref:
                for file in files:
                    _abs_path = file.absolute()
                    _rel_path = _abs_path.relative_to(dir_path)
                    tar_ref.add(_abs_path, arcname=_rel_path, recursive=True)
        elif self.archive_type == "tar":
            with tarfile.open(self.archive, "w") as tar_ref:
                for file in files:
                    _abs_path = file.absolute()
                    _rel_path = _abs_path.relative_to(dir_path)
                    tar_ref.add(_abs_path, arcname=_rel_path, recursive=True)
        elif self.archive_type == "zip":
            with zipfile.ZipFile(
                self.archive, mode="w", compression=zipfile.ZIP_DEFLATED
            ) as zip_ref:
                for file in files:
                    _abs_path = file.absolute()
                    _rel_path = _abs_path.relative_to(dir_path)
                    zip_ref.write(_abs_path, arcname=_rel_path)

import hashlib
from pathlib import Path
from typing import List, Dict

SHA256 = "SHA256"
HASH_ALGORITHMS = [
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "blake2b",
    "blake2s",
    "md5",
]


class FileHashE(BaseException):
    def __init__(self, msg: str):
        super(FileHashE, self).__init__()
        self.msg = msg


def file_hash_create(file_name: Path, hash_method: str = SHA256) -> str:
    """
    create hash for a given file with a given hash method
    :param file_name, path to file to be hashed
    :param hash_method, string describing the hash method, defaults to SHA256
    """
    if not file_name.exists():
        raise FileHashE("could not find any file named: %s" % file_name)

    _bytes = file_name.read_bytes()
    if hash_method.lower() in HASH_ALGORITHMS:
        # getattr is used to 'capture' the right hashlib function with same name as the hash method.
        _hash_algorithm = getattr(hashlib, hash_method.lower())
        hash_string = _hash_algorithm(_bytes).hexdigest()
    else:
        raise FileHashE("hash method not yet implemented or recognized")

    return hash_string


def file_hash_check(
    file_name: Path, hash_string: str, hash_method: str = SHA256
) -> bool:
    """
    hash the file and compare the hash with hash string passed,
    handle special case where the hash string contains an algorithm
    identifier like "sha256" or "md5"
    :param file_name:
    :param hash_method: string, defaults to SHA256
    :param hash_string: string, may contain : and algorithm
    :return: True if matching, otherwise false, raises if file
            doesn't exist
    """
    if hash_method.lower() not in HASH_ALGORITHMS:
        raise FileHashE("invalid hash method received: %s" % hash_method)

    _str = str(hash_string)
    if _str.find(":") > -1:
        _hash_string_elements = _str.split(":")
        assert _hash_string_elements[0].lower() in HASH_ALGORITHMS
        _method = _hash_string_elements[0].lower()
        _hash = _hash_string_elements[1]
    else:
        _method = hash_method
        _hash = hash_string

    return file_hash_create(file_name, hash_method) == _hash


def file_hash_create_hash_file(
    file_path: Path, file_list: List, hash_method: str = SHA256
) -> bool:
    """
    Creates a hash file on the form:
    METHOD:HASH_STRING PATH_TO_FILE_RELATIVE_TO_CREATED_HASH_FILE
    :param file_path: string, absolute path to hash file
    :param file_list: list of strings, each pointing to a file
    :param hash_method:
    :return: True if succeeded, otherwise False
    """

    if not isinstance(file_list, list):
        raise FileHashE("expecting a list of files")

    if hash_method not in HASH_ALGORITHMS:
        raise FileHashE("invalid method received: %s" % hash_method)

    if len(file_list) < 1:
        raise FileHashE("no files to generate hashes for")

    _hash_list = []

    for item in file_list:
        _hash = file_hash_create(file_name=item, hash_method=hash_method)
        _path = Path(item).relative_to(file_path.parent)
        _hash_list.append(hash_method + ":" + _hash + " " + str(_path))

    file_path.write_text("\n".join(_hash_list))

    return True


def file_hash_check_hash_file(file_path: Path) -> Dict:
    """
    Verify all hashes of the files specified in the hash file
    :param file_path: Path, absolute path to hash file
    :return: dictionary, name of file: True/False
    """
    _path_to_hash_file = file_path
    _path_to_dir = file_path.parent

    # lists all files present in the folder tree starting with file_path
    _directory_contents = [
        _file
        for _file in _path_to_dir.glob("**/*")
        if _path_to_dir.joinpath(_file).is_file()
    ]

    result = {}
    _hash_lines = _path_to_hash_file.read_text().splitlines()
    for line in _hash_lines:

        if line.split()[1] not in _directory_contents:
            raise FileHashE(
                "Unable to locate the file "
                + line.split()[1]
                + " in the compressed archive"
            )

        for file in _directory_contents:
            if line.split()[1] == file:
                result[file] = file_hash_check(
                    _path_to_dir.joinpath(Path(file)), line.split()[0]
                )

    return result

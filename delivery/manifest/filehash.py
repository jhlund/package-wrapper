import hashlib
from pathlib import Path

SHA256 = 'SHA256'
HASH_ALGORITHMS = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'md5']


class FileHashE(BaseException):
    def __init__(self, msg):
        super(FileHashE, self).__init__()
        self.msg = msg


def file_hash_create(file_name: Path, hash_method: str = SHA256) -> str:
    """
    create hash for a given file with a given hash method
    :param file_name, path to file to be hashed
    :param hash_method, string describing the hash method, defaults to SHA256
    """
    if not file_name.exists():
        raise FileHashE('could not find any file named: %s' % file_name)

    _bytes = file_name.read_bytes()
    if hash_method.lower() in HASH_ALGORITHMS:
        # getattr is used to 'capture' the right hashlib function with same name as the hash method.
        _hash_algorithm = getattr(hashlib, hash_method.lower())
        hash_string = _hash_algorithm(_bytes).hexdigest()
    else:
        raise FileHashE('hash method not yet implemented or recognized')

    return hash_string


def file_hash_check(file_name: Path, hash_string: str, hash_method: str = SHA256) -> bool:
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
        raise FileHashE('invalid hash method received: %s' % hash_method)

    _str = str(hash_string)
    if _str.find(':') > -1:
        _hash_string_elements = _str.split(':')
        assert _hash_string_elements[0].lower() in HASH_ALGORITHMS
        _method = _hash_string_elements[0].lower()
        _hash = _hash_string_elements[1]
    else:
        _method = hash_method
        _hash = hash_string

    return file_hash_create(file_name, hash_method) == _hash

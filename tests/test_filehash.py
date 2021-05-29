import pytest
from pathlib import Path
import json

from delivery.manifest.filehash import file_hash_check


@pytest.mark.parametrize('filename, expected_hash, hash_method, json_data',
                         [('SHA256.json',
                           'sha256:4c12882f1ce34f1f0aa5d2f6a902170d35cef128b8eecee5867d5750f5ab5e63',
                           'sha256',
                           {"my_hash": 'is always matching'}),
                          ('SHA1.json',
                           'sha1:c922c69a3ad8c693b7dcc1e4bf75dbffc6074782',
                           'sha1',
                           {"my_hash": 'is always matching'}),
                          ('MD5.json',
                           'sha1:545112744d394dd2b7e52b4f4dc717ed',
                           'md5',
                           {"my_hash": 'is always matching'})
                          ])
def test_file_hash_check_matches(tmpdir, filename, expected_hash, hash_method, json_data):
    """
    create dummy file with a known hash in a temporary directory and provide checksum
    :return:
    """
    _file_name = Path(filename)
    _expected_hash = expected_hash
    _hash_method = hash_method
    _json_data = json_data
    _path = Path(tmpdir).joinpath(_file_name)
    with open(_path, 'w') as file_pointer:
        json.dump(_json_data, file_pointer, indent=3)
    assert file_hash_check(file_name=_path, hash_string=_expected_hash, hash_method=_hash_method)

import pytest
from pathlib import Path
import json

from delivery.manifest.filehash import file_hash_check


@pytest.fixture()
def hash_file(tmpdir):
    _file_name = Path('hashed_file.json')
    _json_data = {"my_hash": 'is always matching'}
    _path = Path(tmpdir).joinpath(_file_name)
    with open(_path, 'w') as fp:
        json.dump(_json_data, fp, indent=3)
    yield _path


@pytest.mark.parametrize('expected_hash, hash_method',
                         [('sha256:4c12882f1ce34f1f0aa5d2f6a902170d35cef128b8eecee5867d5750f5ab5e63',
                           'sha256'),
                          ('sha1:c922c69a3ad8c693b7dcc1e4bf75dbffc6074782',
                           'sha1'),
                          ('sha1:545112744d394dd2b7e52b4f4dc717ed',
                           'md5')
                          ])
class TestHash:

    def test_file_hash_check_matches(self, hash_file, expected_hash, hash_method):
        """
        Check dummy file with a known hash with generated checksum
        :return:
        """
        assert file_hash_check(file_name=hash_file, hash_string=expected_hash, hash_method=hash_method)

    def test_file_hash_check_doesnt_match(self, hash_file, expected_hash, hash_method):
        """
        copy a well known dummy file into temporary directory and provide checksum
        :return:
        """
        _invalid = str(expected_hash).replace('f', 'c')
        assert not file_hash_check(file_name=hash_file, hash_string=_invalid, hash_method=hash_method)

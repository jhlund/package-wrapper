import pytest
from pathlib import Path
import json

from delivery.manifest.filehash import file_hash_check, file_hash_create_hash_file


@pytest.fixture()
def hash_file(tmpdir):
    _file_name = Path("hashed_file.json")
    _json_data = {"my_hash": "is always matching"}
    _path = Path(tmpdir).joinpath(_file_name)
    with open(_path, "w") as file_pointer:
        json.dump(_json_data, file_pointer, indent=3)
    yield _path


@pytest.mark.parametrize(
    "expected_hash, hash_method",
    [
        pytest.param(
            "sha1:c922c69a3ad8c693b7dcc1e4bf75dbffc6074782", "sha1", id="sha1"
        ),
        pytest.param(
            "sha224:749c15eaca51f74b47824be96cc5e7aceca8339cb73e258885d11f2c",
            "sha224",
            id="sha224",
        ),
        pytest.param(
            "sha256:4c12882f1ce34f1f0aa5d2f6a902170d35cef128b8eecee5867d5750f5ab5e63",
            "sha256",
            id="sha256",
        ),
        pytest.param(
            "sha384:26acf5c876e3c7dd19d276b88431d5cdb86f5f757e8a27e420e2f3f43b8f5026bdd3298f1258bf8d5b4c98af243bbddc",
            "sha384",
            id="sha384",
        ),
        pytest.param(
            "sha512:fe493c17f9521b641eaac36edfbab48657938f2337da75bcf5b4e32ec9d3cb4ecaf524031553aff7b17a0ca3da58d3f92e8e404a93eb24fcc93698fa40f631de",
            "sha512",
            id="sha512",
        ),
        pytest.param("md5:545112744d394dd2b7e52b4f4dc717ed", "md5", id="md5"),
    ],
)
class TestHashes:
    def test_file_hash_check_matches(self, hash_file, expected_hash, hash_method):
        """
        Check dummy file with a known hash with generated checksum
        :return:
        """
        assert file_hash_check(
            file_name=hash_file, hash_string=expected_hash, hash_method=hash_method
        )

    def test_file_hash_check_doesnt_match(self, hash_file, expected_hash, hash_method):
        """
        Check dummy file with a known hash with generated checksum against the scrambled hash.
        :return:
        """
        _invalid = str(expected_hash).replace("f", "c")
        assert not file_hash_check(
            file_name=hash_file, hash_string=_invalid, hash_method=hash_method
        )

    def test_hash_file_contents(self, tmpdir, hash_file, expected_hash, hash_method):
        file_path = Path(tmpdir).joinpath(Path("hash_file.json"))
        file_hash_create_hash_file(file_path=file_path, file_list=[hash_file], hash_method=hash_method)
        contents = file_path.read_text()
        assert contents == f"{expected_hash} hashed_file.json"

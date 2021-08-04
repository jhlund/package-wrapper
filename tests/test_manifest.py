import json
import re
import pytest
from pathlib import Path
from delivery.manifest.manifest import ManifestE, ManifestFile

TIME_FORMAT = re.compile(
    r"[0-3][0-9]\/[0-1][0-9]\/[0-9][0-9][0-9][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9]"
)


@pytest.fixture()
def folder_structure(tmpdir):
    base_path = Path(tmpdir)
    Path.mkdir(Path.joinpath(base_path, Path("lvl_one")))
    _file_name = Path("hashed_file.json")
    _json_data = {"my_hash": "is always matching"}
    _path = base_path.joinpath(_file_name)
    with open(_path, "w") as fp:
        json.dump(_json_data, fp, indent=3)
    yield base_path, _path


@pytest.fixture()
def meta_file(tmpdir):
    base_path = Path(tmpdir)
    _file_name = Path("meta_data.json")
    _json_data = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
    }
    _path = base_path.joinpath(_file_name)
    with open(_path, "w") as fp:
        json.dump(_json_data, fp, indent=3)
    yield _path


class TestManifest:
    def test_created_time_format(self):
        manifest = ManifestFile(hash_method="sha256")
        assert re.match(TIME_FORMAT, manifest.database["created (utc)"])

    def test_add_folder(self, folder_structure):
        manifest = ManifestFile(hash_method="sha256")
        dir_path, file_path = folder_structure
        assert manifest.add_folder(dir_path)

    def test_add_folder_raises(self):
        manifest = ManifestFile(hash_method="sha256")
        with pytest.raises(ManifestE):
            manifest.add_folder(Path("nonsens"))

    def test_add_file(self, folder_structure):
        manifest = ManifestFile(hash_method="sha256")
        dir_path, file_path = folder_structure
        assert manifest.add_artifact_to_db(file_path, dir_path)

    def test_create_files_key_when_adding_artifact(self, folder_structure):
        manifest = ManifestFile(hash_method="sha256")
        dir_path, file_path = folder_structure
        assert "files" not in manifest.database
        manifest.add_artifact_to_db(file_path, dir_path)
        assert "files" in manifest.database


class TestMetaData:
    def test_add_meta_data(self):
        manifest = ManifestFile(hash_method="sha256")
        keyword = "test_keyword"
        content = "test_content"
        manifest.add_meta_data(keyword=keyword, content=content)
        assert manifest.database[keyword] == content

    def test_add_meta_data_file(self, meta_file):
        manifest = ManifestFile(hash_method="sha256")
        manifest.add_meta_data_file(meta_data_path=meta_file)
        assert manifest.database["first"] == 1
        assert manifest.database["second"] == 2
        assert manifest.database["third"] == 3
        assert manifest.database["fourth"] == 4

import click
from pathlib import Path
import json
from datetime import datetime

from .version import __version__
from package_wrapper.archiver.archiver import Archive
from package_wrapper.manifest.manifest import ManifestFile
from package_wrapper.manifest.filehash import HASH_ALGORITHMS


def get_compression_method_from_file_name(filename):
    if str(filename).endswith(".tar.gz"):
        compression_method = "tar.gz"
    elif str(filename).endswith(".tar"):
        compression_method = "tar"
    elif str(filename).endswith(".zip"):
        compression_method = "zip"
    else:
        raise click.ClickException(
            "Could not determine compression method. Please specify parameter -a / --archive-type"
        )
    return compression_method


def package(directory, meta_data, output, hash_type, archive_type):
    """
    Given a directory path and optional meta-information in a JSON formatted file.
    Creates a deliverable archive file containing both the files and a manifest
    with meta-data as well as file hashes for each file.

    Internal call
    """
    if not archive_type and not output:
        archive_type = "tar.gz"

    if not archive_type and output:
        archive_type = get_compression_method_from_file_name(output)

    if not output:
        output = directory.parent.joinpath(Path(f"output.{archive_type}"))

    # Create the complete meta-data file
    manifest = ManifestFile(hash_method=hash_type)
    package_metadata = {
        "package created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S (utc)"),
        "version of package-wrapper": __version__,
        "archive type used for packaging": archive_type,
    }
    manifest.add_meta_data(keyword="package-wrapper", content=package_metadata)
    if meta_data:
        manifest.add_meta_data_file(meta_data_path=meta_data)

    # All folder to the manifest
    manifest.add_folder(path_to_directory=directory)
    output_manifest_path = directory.joinpath(Path("manifest.json"))
    with open(output_manifest_path, "w") as file_pointer:
        file_pointer.write(json.dumps(manifest.retrive_contents(), indent=3))

    if output.parent.exists():
        # Create the compressed output file
        archive = Archive(output, archive_type=archive_type)
        archive.compress(dir_path=directory)
    else:
        raise click.ClickException("The specified output folder does not exist")

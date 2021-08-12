import click
from pathlib import Path
import json
from datetime import datetime

from .version import __version__
from .package import package as package_api
from package_wrapper.archiver.archiver import Archive
from package_wrapper.manifest.manifest import ManifestFile
from package_wrapper.manifest.filehash import HASH_ALGORITHMS


@click.command()
@click.option(
    "--directory",
    "-D",
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="path to directory to package",
)
@click.option(
    "--meta-data",
    "-m",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=False,
    help="path to meta-data file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(
        resolve_path=False,
        path_type=Path,
    ),
    help="path to wanted output file (example.tar.gz).\n Always overwrites files if exists",
)
@click.option(
    "--hash-type",
    "-#",
    type=click.Choice(HASH_ALGORITHMS, case_sensitive=False),
    default="sha256",
    help="hash algorithm to use",
)
@click.option(
    "--archive-type",
    "-a",
    type=click.Choice(["tar", "tar.gz", "zip"], case_sensitive=False),
    help="compression algorithm to use. This overrides the -o /--output file name suffix",
)
def package(directory, meta_data, output, hash_type, archive_type):
    """
    Given a directory path and optional meta-information in a JSON formatted file.
    Creates a deliverable archive file containing both the files and a manifest
    with meta-data as well as file hashes for each file.
    """
    package_api(directory, meta_data, output, hash_type, archive_type)


if __name__ == "__main__":
    pass

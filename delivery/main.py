import click
from pathlib import Path
import json

from .version import __version__
from delivery.archiver.archiver import Archive
from delivery.manifest.manifest import ManifestFile
from delivery.manifest.filehash import HASH_ALGORITHMS


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
    "-M",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True, 
    help="path to meta-data file")
@click.option(
    "--output",
    "-o",
    type=click.Path(
        exists=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="path to output folder")
@click.option(
    "--hash-type",
    type=click.Choice(HASH_ALGORITHMS, case_sensitive=False),
    default="sha256",
    help="hash algorithm to use",
)
def package(directory, meta_data, output, hash_type):
    """
    Given a directory path and meta-information, package this into a delivery.
    """
    print(f"directory: {directory}")
    print(f"meta_data: {meta_data}")
    print(f"hash_type: {hash_type}")
    # Create the comeplete meta-data file
    manifest = ManifestFile(hash_method=hash_type)

    manifest.add_meta_data("version of package program", __version__)
    manifest.add_meta_data("Input directory", str(directory))
    manifest.add_meta_data("Hash method used", hash_type)
    manifest.add_meta_data("Output folder", str(output))

    manifest.add_folder(path_to_directory=directory)
    output_manifest_path = directory.joinpath(Path("manifest.json"))
    with open(output_manifest_path, "w") as file_pointer:
        file_pointer.write(json.dumps(manifest.retrive_contents(), indent=3))
    archive = Archive(output.joinpath("output.zip"))
    archive.compress(dir_path=directory)


if __name__ == "__main__":
    pass

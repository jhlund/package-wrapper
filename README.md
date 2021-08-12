# Package wrapper
Often as a developer you are faced with the task of keeping track of specific build artifacts. This can be generated
documentation, compiled code, log-files, and other files that might be impossible to reproduce exactly. To be able to
deliver and keep rack of this kind of files this project strive to create a simple way to package these files together 
with information and hashes. This will allow each delivery to be checked for consistency and also allow it to be tracked
to its source (if for example git commits, build machine etc. are present in the information supplied).

Given a top-folder and an optional meta-data file in JSON format, the call to `pkgwrap` creates file-hashes for each file
contained in the folder structure below the top-folder, stores these in a manifest-file also containg the meta-data and
packages all in an archive (tar.gz-, tar-, or zip-format).

# Installation
Package-wrapper is an installable pip package. It is recommended to create a virtual environment to install the package into.
```
$python3 -m venv venv
$source venv/bin/activate
$pip install .
```
  
# Usage
A directory with the contents to be packaged, and a optional JSON file containing meta-data, is used as input to create a package. The
contents can be any kind of files, and the sub-directory structure will be preserved inside a compressed archive. Inside
the compressed archive there will be a manifest file containing the meta-data, and file hashes of all contained files.

Additional functionality to test such a delivery package against the manifest-file will be available.

Example structure
```
├── package_dir
|    ├── logs
|    │    └── build_log.log
|    ├── docs
|    │    ├── release_documentation
|    │    │   ├── doc1.txt
|    │    │   ├── doc2.pdf
|    │    │   └── doc3.txt
|    │    └── generated_docs
|    │        ├── doc1.txt
|    │        ├── doc2.pfd
|    │        ├── doc3.txt
|    │        └── doc4.json
|    ├── misc
|    │    └── happy_ascii_art.txt
|    │ 
|    └── binaries
|         └── build_DateTimeVersion
|             ├── build_image1.bin
|             ├── build_image2.bin
|             └── build_image3.bin
|
└── meta-data.json
```

Example meta-data file
```
{   
    "built by": "first_name last_name",
    "email": "email(at)example.com",
    "build version": "1.2.3",
    "git commit": "1234567890", 
    "placeholder str": "this is an example meta-data file without contents.",
    "placeholder int": 123,
    "placeholder list": ["list", "of", "strings"],
    "placeholder dict": {"dict": 1, "of": 2.0, "misc": "3"}
}
```

To package this just call:
```
pkgwrap -D package_dir -m meta-data.json
```
This will result in a file called `output.tar.gz` placed in the same directory as the `package_dir`

Generated output
```
└── output.tar.gz
     ├── logs
     │    └── build_log.log
     ├── docs
     │    ├── release_documentation
     │    │   ├── doc1.txt
     │    │   ├── doc2.pdf
     │    │   └── doc3.txt
     │    └── generated_docs
     │        ├── doc1.txt
     │        ├── doc2.pfd
     │        ├── doc3.txt
     │        └── doc4.json
     ├── misc
     │    └── happy_ascii_art.txt
     │ 
     ├── binaries
     |    └── build_DateTimeVersion
     |        ├── build_image1.bin
     |        ├── build_image2.bin
     |        └── build_image3.bin
     └── manifest.json
```

The contents of the manifest file is the following

```
{
   "created": "2021-08-04 15:47:29 (utc)",
   "version of package-wrapper": "0.0.1",
   "archive type used for packaging": "tar.gz",
   "built by": "first_name last_name",
   "email": "email(at)example.com",
   "build version": "1.2.3",
   "git commit": "1234567890",
   "placeholder str": "this is an example meta-data file without contents.",
   "placeholder int": 123,
   "placeholder list": [
      "list",
      "of",
      "strings"
   ],
   "placeholder dict": {
      "dict": 1,
      "of": 2.0,
      "misc": "3"
   },
   "files": {
      "manifest.json": "sha256:db4b56b6fa846465e503b98f8c8c4fb0dc39df1ed7064a8d58c69f16690edd8e",
      "misc/happy_ascii_art.txt": "sha256:4dde1e83eeafa5979f913c3dbb939867cfcf816e43335710703d31aa7e74f99e",
      "docs/generated_docs/doc3.txt": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/generated_docs/doc1.txt": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/generated_docs/doc2.pdf": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/generated_docs/doc4.json": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/release_documentation/doc3.txt": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/release_documentation/doc1.txt": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "docs/release_documentation/doc2.pdf": "sha256:619b0adc73906e85c80904b27536bfe3066c7e309b5918e5ff6d3e7cfa607e41",
      "binaries/build_image3.bin": "sha256:3e60592a46d9341bd5e100b9e666b71d5b705d9e88f3ed577c6ed007f139a924",
      "binaries/build_image1.bin": "sha256:307523623dd9078dc9466900fbb7542e51012bd0fdb609cc7980ac1a85887c73",
      "binaries/build_image2.bin": "sha256:307523623dd9078dc9466900fbb7542e51012bd0fdb609cc7980ac1a85887c73",
      "logs/build_log.log": "sha256:3316ccbafe92793b5d1dddf9e686d67c4e6485c83af9030e7e1be534390f2611"
   }
}
```

# Built in help
```
$ pkgwrap --help
Usage: pkgwrap [OPTIONS]

  Given a directory path and optional meta-information in a JSON formatted
  file. Creates a deliverable archive file containing both the files and a
  manifest with meta-data as well as file hashes for each file.

Options:
  -D, --directory PATH            path to directory to package  [required]
  -m, --meta-data PATH            path to meta-data file
  -o, --output PATH               path to wanted output file (example.tar.gz).
                                  Always overwrites files if exists
  -#, --hash-type [sha1|sha224|sha256|sha384|sha512|blake2b|blake2s|md5]
                                  hash algorithm to use
  -a, --archive-type [tar|tar.gz|zip]
                                  compression algorithm to use. This overrides
                                  the -o /--output file name suffix
  --help                          Show this message and exit.
```

# API usage
To use the package-wrapper as an internal python module import it from the file.
```
from package_wrapper.package import package
```
Then call `package()`

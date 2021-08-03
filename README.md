# Traceable delivery
*This readme is during the development of the project used as a general project documentation*   
Often as a developer you are faced with the task of keeping track of specific build artifacts. This can be generated
documentation, compiled code, log-files, and other files that might be impossible to reproduce exactly. To be able to
deliver and keep rack of this kind of files this project strive to create a simple way to package these files together 
with information and hashes. This will allow each delivery to be checked for consistency and also allow it to be tracked
to its source (if for example git commits, build machine etc. is present in the information supplied).

## General idea
- The program should be controlled by a config file, but have the possibility to overrule this config by direct insertion
of parameters.
  
- The program should be an installable python package (setup.py and all that) with a CLI interface (click is a good
  candidate)
  
- The program shall be developed using a TDD approach.

- The program shall implement an architecture of a simple CLI layer calling internal API functions. This to ease the
testing using callable functions and to make all API functions usable from within the code (something not always)
  possible with CLI functions)
  
## Usage
A directory with the contents to be packaged, and a file containing meta-data is used as input to create a package. The
contents can be any kind of files, and the sub-directory structure will be preserved inside a compressed archive. Inside
the compressed archive there will be a manifest file containing the meta-data, additional information such as
time-stamps, and file hashes of all contained files.

Additional functionality to test such a delivery package against the manifest-file will be available.

Example structure
```
├── Docs
│ ├── release_documentation
│ │   ├── doc1.txt
│ │   ├── doc2.txt
│ │   └── doc3.txt
│ └── generated_docs
│     ├── doc1.json
│     ├── doc2.pfd
│     ├── doc3.txt
│     └── doc4.md
├── Misc
│ └── happy_ascii_art.txt
│ 
└── Binaries
    └── build_DateTimeVersion
        ├── boot_loader.bin
        ├── SPL.bin
        └── imgage.bin
```

## Running the script
install using `pip install .`   
test running it using `package -D examples/example_delivery/ -M examples/meta-data.json -o examples/output/ `

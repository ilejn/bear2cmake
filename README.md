bear2cmake
==========

A simple Python script to help to create CMakeLists.txt for an arbitrary project

Usage
-----

``` shell
bear2cmake.py [options]
    Create CMakeLists.txt based on compile_commands.json (e.g. produced by _bear_)


Options:
  -h, --help            show this help message and exit
  --yaml=YAML_FILENAME, --yaml-file=YAML_FILENAME, --yaml-filename=YAML_FILENAME
                        input file produced by _bear_
  --topdir=TOP_DIRECTORY, --top-dir=TOP_DIRECTORY
  --project=PROJECT_NAME, --project-name=PROJECT_NAME
                        filename with suffix (e.g. '.so')
```

The flow
--------

1. configure your project (if apropriate)
2. run _make_ (or may be other build system) via _bear_ to get compile_commands.json
3. run *bear2cmake --project=myproject > CMakeLists.txt* to get CMakeLists.txt

What You get
------------

CMakeLists.txt with
* one target, which type depends on *project-name* parameter
* *target_sources* aggregates all source files compiled during step(2) from the above paragraph
* *target_include_directories* combines all *-I* parameters
* *target_compile_definitions* combines all *-D* parameters

The Bear
--------

Bear (Build EAR) is a tool to generate compilation database for clang tooling
https://github.com/rizsotto/Bear

Included in all modern Linux distros, *sudo apt install bear* to install in Ubuntu

Disclaimer
----------

Treat generated CMakeLists.txt as a starting point.
Serious work is required to create correct and robust CMakeLists.txt,
while *bear2cmake* does the most trivial and tedious part

#!/usr/bin/python3

import yaml
from optparse import OptionParser
import os.path

known_dirs = {}
includes = []
opts = set()

def process(options):
    yaml_fname = options.yaml_filename
    prefix = os.path.realpath(options.top_directory)

    with open(yaml_fname, 'r') as f:
        y = yaml.load(f, Loader=yaml.CLoader)

    for el in y:
        dir = el['directory']
        if dir not in known_dirs:
            known_dirs[dir] = [el['file']]
        else:
            known_dirs[dir].append(el['file'])

        for arg in el['arguments']:
            if arg.startswith("-I"):
                fname = arg[2:]
                if fname[0] != '/':
                    fname = os.path.realpath(dir + '/' + fname)
                    fname = "${CMAKE_CURRENT_SOURCE_DIR}" +  fname[fname.startswith(prefix) and len(prefix):]
                fname not in includes and includes.append(fname)
            if arg.startswith("-D"):
                opts.add(arg[2:])

    if options.project_name.endswith(".a"):
        project_name = options.project_name[:-2]
        library_type = "STATIC"
        project_type = "library"
    elif options.project_name.endswith(".so"):
        project_name = options.project_name[:-3]
        library_type = "SHARED"
        project_type = "library"
    else:
        project_name = options.project_name
        library_type = ""
        project_type = "executable"


    print("""cmake_minimum_required(VERSION 3.3)
set(PROJECT_NAME %s)
project(${PROJECT_NAME})
add_%s(${PROJECT_NAME} %s)""" % (project_name, project_type, library_type))

    if len(known_dirs):
        print("target_sources(${PROJECT_NAME} PRIVATE")
        for dir in known_dirs:
            for file in known_dirs[dir]:
                dir = dir[dir.startswith(prefix) and len(prefix):]
                print("    ${CMAKE_CURRENT_SOURCE_DIR}" + dir + '/' + file)
        print(")")

    if len(includes):
        print("target_include_directories(${PROJECT_NAME} PRIVATE")

        for incl in includes:
            print("    " + incl)

        print(")")

    if len(opts):
        print("target_compile_definitions(${PROJECT_NAME} PRIVATE")

        for opt in opts:
            print("    " + opt)

        print(")")

usage = """
%prog [options]
    Create CMakeLists.txt based on compile_commands.json (e.g. produced by _bear_)
"""

parser = OptionParser(usage=usage)

parser.add_option("--yaml", "--yaml-file", "--yaml-filename", dest="yaml_filename", default="compile_commands.json",
    help="input file produced by _bear_")
parser.add_option("--topdir", "--top-dir", dest="top_directory", default=".")
parser.add_option("--project", "--project-name", dest="project_name", default="a_cmake_project",
    help="filename with suffix (e.g. '.so')")
# parser.add_option("--per-dir", "--per-directory", dest="per_directory_mode", default=True,
#     help="CMakeLists.txt per directory")

(options, args) = parser.parse_args()


process(options)

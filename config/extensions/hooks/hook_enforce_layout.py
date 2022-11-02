import os.path

from conan import ConanFile
from conan.errors import ConanException


def pre_source(conanfile: ConanFile):
    if not hasattr(conanfile, "layout"):
        raise ConanException("conanfile has no layout() defined, use of `source` command is dangerous!")

    # in-source conanfile.py may use src_folder=.
    if not hasattr(conanfile, "source"):
        return

    conanfile.layout()

    if os.path.realpath(conanfile.source_folder) == os.path.realpath(conanfile.folders.base_source):
        raise ConanException("conanfile layout() should set the src_folder to something other than '.'")

import os.path

from conan import ConanFile

from conan.tools.files import get, patch, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class HelloThirdParty(ConanFile):
    name = "hello"
    version = "1.0"
    user = "temp"
    channel = "test"

    settings = "compiler", "build_type"

    exports_sources = ["hello.patch"]

    def source(self):
        get(self, "https://github.com/conan-io/hello/archive/refs/tags/1.0.0.tar.gz", strip_root=True)
        patch(self, patch_file="hello.patch")

    def layout(self):
        # src_folder is crucial or it will unpack right into the source directory
        cmake_layout(self, src_folder=".temp-source")

        # Here we set everything we want to be overridden in cpp_info in editable

        # source and build are merged, source has priority
        # before merging, source and build paths are prefixed with respective source and build directories

        # includedirs are relative to source, so we define them in source
        # If there are generated sources or we copy source in build - we would need to set these includedirs in build
        self.cpp.source.includedirs = ['.']
        # libdirs are relative to build directory, so they go into build
        self.cpp.build.libdirs = ['lib']

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # This is never called in the editable mode
        copy(self, 'hello.h', src=self.source_folder, dst=os.path.join(self.package_folder, 'include'))
        copy(self, '*', src=os.path.join(self.build_folder, 'bin'), dst=os.path.join(self.package_folder, 'bin'))
        copy(self, '*', src=os.path.join(self.build_folder, 'lib'), dst=os.path.join(self.package_folder, 'lib'))

    def package_info(self):
        # Everything here will be overridden by values from cpp.build/cpp.source in layout
        # includedirs/libdirs are always set in the cpp.build/cpp.source, so those are always overridden
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.libs = ['hello']

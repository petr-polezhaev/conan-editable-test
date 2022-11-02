from conan import ConanFile

from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout


class Foo(ConanFile):
    name = "foo"
    version = "1.0"
    user = "temp"
    channel = "test"

    settings = "compiler", "build_type"

    requires = "hello/1.0@temp/test"

    exports_sources = ["src/**", "CMakeLists.txt", "include/**"]

    def layout(self):
        cmake_layout(self, src_folder=".")

        self.cpp.package.libs = ["foo"]
        self.cpp.package.requires = ["hello::hello"]

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

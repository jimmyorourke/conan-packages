from conans import ConanFile, CMake
import os


class GoogletestConan(ConanFile):
    name = "googletest"
    version = "1.8.1"
    license = "3-Clause BSD License - https://github.com/google/googletest/blob/master/LICENSE"
    url = "https://github.com/google/googletest"
    description = "Google's C++ testing and mocking framework"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True

    def get_install_folder(self):
        return os.path.join(self.source_folder, "install")

    def source(self):
        self.run("git clone https://github.com/google/googletest.git")
        self.run(
            "cd {} && git checkout tags/release-{}".format(GoogletestConan.name, GoogletestConan.version))

    def build(self):
        cmake = CMake(self, generator="Ninja", set_cmake_flags=True)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.get_install_folder()
        cmake.definitions["CMAKE_CXX_STANDARD"] = "17"
        if self.settings.os == "Linux" and self.settings.compiler == "clang":
            cmake.definitions["CMAKE_CXX_FLAGS"] = cmake.definitions["CMAKE_CXX_FLAGS"] + " -stdlib=" + str(self.settings.compiler.libcxx)

        cmake.verbose = True
        self.output.info(cmake.command_line)
        if self.settings.os == "Windows":
            # Use shared (DLL) runtime lib even when Google Test is built as static lib
            cmake.definitions["gtest_force_shared_crt"] = True
        cmake.configure(source_folder="googletest")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*", dst=".", src=self.get_install_folder())

    def package_info(self):
        self.cpp_info.libs = ["gtest", "gmock_main", "gmock"]
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = [lib + "d" for lib in self.cpp_info.libs]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")


from conans import CMake, ConanFile
import os

channel = "testing"
username = "demo"

class CMakeTest(ConanFile):
    name = "CMakeTest"
    requires = "cmake_installer/3.14.3@{}/{}".format(username, channel)

    settings = "os", "arch"

    def test(self):
        base = self.deps_cpp_info.bindirs[0]
        self.run(os.path.join(base, "cmake --version"))

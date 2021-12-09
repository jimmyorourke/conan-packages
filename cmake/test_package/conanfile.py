from conans import CMake, ConanFile
import os

class CMakeTest(ConanFile):
    name = "CMakeTest"
    requires = "cmake/3.14.3"

    settings = "os", "arch"

    def test(self):
        base = self.deps_cpp_info.bindirs[0]
        self.run(os.path.join(base, "cmake --version"))

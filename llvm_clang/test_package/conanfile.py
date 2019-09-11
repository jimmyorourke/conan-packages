from conans import CMake, ConanFile
import os

channel = "testing"
username = "demo"

class LLVMTest(ConanFile):
    name = "llvmTest"
    requires = "llvm_clang/8.0.0@{}/{}".format(username, channel)

    settings = "os"
    options = {"export_toolchain": [True, False]}
    default_options = {"export_toolchain": False}


    def test(self):
        base = self.deps_cpp_info.bindirs[0]
        if self.settings.os == 'Windows':
            self.run(os.path.join(base, "clang.exe --version"))
        else:
            self.run(os.path.join(base, "clang --version"))

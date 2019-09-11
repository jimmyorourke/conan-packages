from conans import ConanFile
import os

channel = "testing"
username = "demo"

class PandocTest(ConanFile):
    name = "pandocTest"
    requires = "pandoc/2.7.2@{}/{}".format(username, channel)

    settings = "os"

    def test(self):
        base = self.deps_cpp_info.bindirs[0]
        self.run(os.path.join(base, "pandoc --version"))

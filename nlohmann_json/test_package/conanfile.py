from conans import ConanFile, CMake
import os

channel = "testing"
username = "demo"

class NlohmannjsonTestConan(ConanFile):
    generators = "cmake"
    requires = "nlohmann_json/3.7.3@{}/{}".format(username, channel)

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        self.run(".%sexample" % os.sep)

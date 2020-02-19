import os

from conans import ConanFile, CMake, tools

channel = "testing"
username = "demo"

class GoogletestTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "googletest/1.8.1@{}/{}".format(username, channel)

    def build(self):
        cmake = CMake(self, generator="Ninja")
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(".%sexample" % os.sep)

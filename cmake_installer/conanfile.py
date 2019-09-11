import os
from typing import Tuple

from conans import ConanFile, tools


class CMakeInstaller(ConanFile):
    name = "cmake_installer"
    version = "3.14.3"
    license = "OSI-approved BSD 3-clause"
    url = "https://cmake.org/"
    settings = "os", "arch"
    build_policy = "missing"
    description = "CMake installer, build, test, and packaging tools."

    @property
    def cmake_folder(self) -> str:
        if self.settings.os == 'Macos':
            return f'cmake-{self.version}-Darwin-x86_64'
        elif self.settings.os == 'Linux':
            return f'cmake-{self.version}-Linux-x86_64'
        elif self.settings.os == 'Windows':
            return f'cmake-{self.version}-win64-x64'
        else:
            raise Exception("CMake is only provided for Macos, Linux, and Windows!")

    @property
    def cmake_download_package(self) -> Tuple[str, str]:
        if self.settings.os == 'Macos':
            return (f'https://github.com/Kitware/CMake/releases/download/v{self.version}/{self.cmake_folder}.tar.gz',
                    '3672bdf0aa492c6f1061f3c2d6ae670c3f6ac1eca56a3d6ed5dbe749e2b5a9c9')
        elif self.settings.os == 'Linux':
            return (f'https://github.com/Kitware/CMake/releases/download/v{self.version}/{self.cmake_folder}.tar.gz',
                    '29faa62fb3a0b6323caa3d9557e1a5f1205614c0d4c5c2a9917f16a74f7eff68')
        elif self.settings.os == 'Windows':
            return (f'https://github.com/Kitware/CMake/releases/download/v{self.version}/{self.cmake_folder}.zip',
                    '53856665d3302aca1684e20eaf423062ab192665a9714a27b10f2d6cd01f3454')
        else:
            raise Exception("CMake is only provided for Macos, Linux and Windows!")

    def build_id(self):
        # only care about architecture on windows
        if self.settings.os != 'Windows':
            self.info_build.settings.arch = 'Any'

    def build(self):
        url, hash = self.cmake_download_package

        self.output.warn(f"Downloading '{url}'...")
        tools.get(url, sha256=hash, keep_permissions=True)

    def package(self):
        if self.settings.os == "Macos":
            self.copy("*", dst="", src=os.path.join(self.cmake_folder, "CMake.app", "Contents"))
        else:
            self.copy("*", dst="", src=self.cmake_folder)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))


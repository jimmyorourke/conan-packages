import os
from typing import Tuple

from conans import ConanFile, tools

class ClangConan(ConanFile):
    name = "llvm_clang"
    version = "8.0.0"
    license = "LLVM"
    url = "https://clang.llvm.org/"
    settings = "os", "arch"
    build_policy = "missing"
    description = "Clang compiler, LLD, libc++, compiler-rt, tools, etc."
    short_paths = True

    # whether to export environment variables in the virtualenv
    # currently only desired on Linux
    options = {"export_toolchain": [True, False]}
    default_options = {"export_toolchain": False}

    @property
    def clang_folder(self) -> str:
        if self.settings.os == 'Macos':
            return f'clang+llvm-{self.version}-x86_64-apple-darwin'
        elif self.settings.os == 'Linux':
            return f'clang+llvm-{self.version}-x86_64-linux-gnu-ubuntu-18.04'
        elif self.settings.os == 'Windows':
            return f'LLVM-{self.version}-win64'
        else:
            raise Exception("Clang is only provided for Macos, Linux, and Windows!")

    @property
    def clang_download_package(self) -> Tuple[str, str]:
        if self.settings.os == 'Macos':
            return (f'http://releases.llvm.org/{self.version}/{self.clang_folder}.tar.xz',
                    '94ebeb70f17b6384e052c47fef24a6d70d3d949ab27b6c83d4ab7b298278ad6f')
        elif self.settings.os == 'Linux':
            return (f'http://releases.llvm.org/{self.version}/{self.clang_folder}.tar.xz',
                    '0f5c314f375ebd5c35b8c1d5e5b161d9efaeff0523bac287f8b4e5b751272f51')
        elif self.settings.os == 'Windows':
            return (f'http://releases.llvm.org/{self.version}/{self.clang_folder}.exe',
                    '56d582eed2d5def6accaedabbe11ae368186600798e2a6a7eb86a727fa7bb20c')
        else:
            raise Exception("Clang is only provided for Macos, Linux and Windows!")

    def build_id(self):
        # only care about architecture on windows
        if self.settings.os != 'Windows':
            self.info_build.settings.arch = 'Any'

    def build(self):
        url, hash = self.clang_download_package

        self.output.warn(f"Downloading '{url}'...")
        temp_install_package = os.path.basename(url)
        tools.download(url, temp_install_package)
        tools.check_sha256(temp_install_package, hash)

        if self.settings.os == 'Windows':
            # An NSIS based installer is shipped for Windows
            # Force it to be silent, and to install to our desired location (/D needs an absolute path)
            install_path = os.path.join(self.build_folder, self.clang_folder)
            self.run(f'{temp_install_package} /S /D={install_path}')
        else:
            tools.unzip(temp_install_package)
        os.unlink(temp_install_package)

    def package(self):
        self.copy('*', src=self.clang_folder, dst='', keep_path=True)

    def package_info(self):
        self.output.info(f"Using Clang {self.version}")

        # Prep for using clang in a conan virtual env. When not using a virtualenv, ${CONAN_BIN_DIRS_LLVM_CLANG} and
        # similar will be available in cmake
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.LLVM_DIR = self.package_folder

        # We aren't ready to use this compiler on all platforms, so don't always let these variables get picked up by
        # CMake
        if self.options.export_toolchain:
            self.env_info.CC = os.path.join(self.package_folder, 'bin', 'clang')
            self.env_info.CXX = os.path.join(self.package_folder, 'bin', 'clang++')
            # https://libcxx.llvm.org/docs/UsingLibcxx.html
            self.env_info.CXXFLAGS = "-stdlib=libc++"
            # Required to find libc++.so
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, 'lib'))
            # Set linker to lld http://lld.llvm.org/
            self.env_info.LDFLAGS='-fuse-ld=lld'

        # Set a helpful custom cmake variable ${CONAN_USER_LLVM_CLANG_CC_INCLUDE_DIR} pointing to the C headers
        self.user_info.CC_INCLUDE_DIR = os.path.join(self.package_folder, 'lib', 'clang', self.version, 'include')
        # Similarly, make it easy for clients to find libc++ at ${CONAN_USER_LLVM_CLANG_LIBCXX_INCLUDE_DIR}
        self.user_info.LIBCXX_INCLUDE_DIR = os.path.join(self.package_folder, 'include', 'c++', 'v1')

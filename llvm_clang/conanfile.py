import os
from typing import Optional, Tuple

from conans import ConanFile, tools

class ClangConan(ConanFile):
    name = "llvm_clang"
    version = "13.0.0"
    license = "LLVM"
    url = "https://clang.llvm.org/"
    settings = "os", "arch"
    build_policy = "missing"
    description = "Clang compiler, LLD, libc++, compiler-rt, tools, etc."
    #short_paths = True

    # whether to export environment variables in the virtualenv
    # Probably only desired on Linux
    options = {"export_toolchain": [True, False]}
    default_options = {"export_toolchain": False}

    @property
    def clang_folder(self) -> str:
        if self.settings.os == 'Macos':
            return f'clang+llvm-{self.version}-x86_64-apple-darwin'
        elif self.settings.os == 'Linux':
            return f'clang+llvm-{self.version}-x86_64-linux-gnu-ubuntu-20.04'
        elif self.settings.os == 'Windows':
            return f'LLVM-{self.version}-win64'
        else:
            raise Exception("Clang is only provided for Macos, Linux, and Windows!")

    @property
    def clang_download_package(self) -> Tuple[str, Optional[str]]:
        if self.settings.os == 'Macos':
            return (f'https://github.com/llvm/llvm-project/releases/download/llvmorg-{self.version}/{self.clang_folder}.tar.xz',
                    None)
        elif self.settings.os == 'Linux':
            return (f'https://github.com/llvm/llvm-project/releases/download/llvmorg-{self.version}/{self.clang_folder}.tar.xz',
                    '2c2fb857af97f41a5032e9ecadf7f78d3eff389a5cd3c9ec620d24f134ceb3c8')
        elif self.settings.os == 'Windows':
            return (f'https://github.com/llvm/llvm-project/releases/download/llvmorg-{self.version}/{self.clang_folder}.exe',
                    None)
        else:
            raise Exception("Clang is only provided for Macos, Linux and Windows!")

    def build_id(self):
        # only care about architecture on windows
        if self.settings.os != 'Windows':
            self.info_build.settings.arch = 'Any'

    def build(self):
        url, hash = self.clang_download_package

        self.output.info(f"Downloading '{url}'...")
        temp_install_package = os.path.basename(url)
        tools.download(url, temp_install_package, sha256=hash)

        if self.settings.os == 'Windows':
            # An NSIS based installer is shipped for Windows
            # Force it to be silent, and to install to our desired location (/D needs an absolute path)
            install_path = os.path.join(self.build_folder, self.clang_folder)
            self.run(f'{temp_install_package} /S /D={install_path}')
        else:
            tools.unzip(temp_install_package)
        #os.unlink(temp_install_package)

    def package(self):
        self.copy('*', src=self.clang_folder, dst='', keep_path=True)

    def package_info(self):
        self.output.info(f"Using Clang {self.version}")

        # Set environment variables for using clang in a conan virtual env. When not using a virtualenv,
        # ${CONAN_BIN_DIRS_LLVM_CLANG} and similar will be available in cmake/
        if self.options.export_toolchain:
            self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
            self.env_info.LLVM_DIR = self.package_folder

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

from conans import ConanFile, tools

import os


class Pandoc(ConanFile):
    name = "pandoc"
    version = "2.7.2"
    license = "https://github.com/jgm/pandoc/blob/master/COPYRIGHT"
    url = "https://pandoc.org/"
    description = "Pandoc - The universal markup converter."
    # We only need different packages for each OS
    settings = "os"
    short_paths = True

    def build(self):
        if self.settings.os == "Windows":
            url = 'https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-windows-x86_64.zip'
            hash = 'bbe8a112829c5ddc60139b708bc188b502491ed38d37b80d7c527431edf129f2'
        elif self.settings.os == "Linux":
            url = 'https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-linux.tar.gz'
            hash = '6741f73e37a900deee56bc2dc71c2893fb28e0961557db36eb029368de5183c2'
        elif self.settings.os == "Macos":
            url = 'https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-macOS.zip'
            hash = 'b42c96829db8356dbbb8ffe81ca23b915188ee6a39a3e07958ba613aa88b6b15'
        else:
            raise Exception("Binary does not exist for these settings")

        tools.get(url, keep_permissions=True, sha256=hash)

    def package(self):
        # remove subdirectories and drop everything into `bin`, making the binary accessible by the default
        # self.cpp_info.bindirs
        self.copy("*", dst="bin", keep_path=False)

    def package_info(self):
        # package() has placed the binary in `bin`
        # Add this location to the conan virtualenv path
        # When not using a conan virtualenv, the binary to be found at ${CONAN_BIN_DIRS_PANDOC}
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

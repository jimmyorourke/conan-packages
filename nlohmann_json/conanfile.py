from conans import ConanFile, CMake, tools

# Notes:
# * This is a header-only library and only needs one package to be published for all platform/compiler.
class NlohmannjsonConan(ConanFile):
    name = "nlohmann_json"
    version = "3.7.3"
    license = "MIT - https://github.com/nlohmann/json/blob/develop/LICENSE.MIT"
    url = "https://github.com/nlohmann/json"
    description = "JSON for Modern C++"
    short_paths = True

    def source(self):
        url = "https://github.com/nlohmann/json/releases/download/v3.7.3/include.zip"
        include_zip_sha256 = "87b5884741427220d3a33df1363ae0e8b898099fbc59f1c451113f6732891014"
        tools.get(url, sha256=include_zip_sha256, destination=".")

    def package(self):
        self.copy(pattern="*", src="include", dst="include")

    def package_id(self):
        self.info.header_only()

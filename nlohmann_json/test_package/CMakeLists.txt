project(PackageTest CXX)
set (CMAKE_CXX_STANDARD 17)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS NO_OUTPUT_DIRS KEEP_RPATHS)

add_executable(example example.cpp)
target_link_libraries(example CONAN_PKG::nlohmann_json)


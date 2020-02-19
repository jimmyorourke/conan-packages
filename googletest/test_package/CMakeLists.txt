project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS NO_OUTPUT_DIRS KEEP_RPATHS)

add_executable(example example.cpp)
target_link_libraries(example PRIVATE CONAN_PKG::googletest)

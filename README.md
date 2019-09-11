# conan-packages
Recipes for Conan packages.

[Conan](https://conan.io/) is a package manager for C and C++. Packages can be third party libraries (as source or pre-built binaries), dev tools, etc.

 
## Building and packaging
To locally build a recipe, from within the recipe directory

```$ conan create . <remote>/<channel>```

where `remote` and `channel` can be whatever you choose, eg. `demo/testing`. These names become more important when uploading prebuilt binary packages to a Conan server.

This command will execute the steps in the rescipe's `conanfile.py`, and publish the package to the local system cache (` ~/.conan/data/`).

## Using packages in C and C++ projects

In your build directory

```$ conan install <package name>/<version>@<remote>/<channel>```

where the package details should match those of the packages previously built.

Alternatively, or if you handle multiple dependencies in your project you can use a [conanfile.txt](https://docs.conan.io/en/latest/reference/conanfile_txt.html) in your project. For example:

```
[requires]
OpenCV/3.2.0@conan/stable

[generators]
cmake
```
Then to install your dependencies:

```$ mkdir build && cd build && conan install ..```

It is recommended to run conan install from a build directory because conan will generate a `conanbuildinfo` file specific to your build configuration and required packages. The `conanbuildinfo` file is what your build system will use to access your conan packages, through exported paths, targets, variables, etc.


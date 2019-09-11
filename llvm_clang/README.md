# llvm-clang
LLVM and Clang Package for Conan

To use the toolchain for your project, in your conan profile file

```
[options]
llvm_clang:export_toolchain=True
[build_requires]
# Should any of the packages in the conanfile need to get rebuilt locally on conan install, these packages are required
# for the build
llvm_clang/8.0.0@demo/testin
```
